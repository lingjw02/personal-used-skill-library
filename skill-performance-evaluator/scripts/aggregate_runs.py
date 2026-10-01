#!/usr/bin/env python3
"""LEVELS 3-5 - Aggregate functional run records into evaluations/performance/failures JSON.

Usage:
  python aggregate_runs.py --runs results/runs --out results [--evals evals/evals.json]
         [--include-simulated] [--baseline-config without_skill] [--seed 0]

Run records ("kind" absent or "functional") are described in references/schemas.md. Key rules:
  * Only execution_mode == "actual" runs enter metrics unless --include-simulated is given.
  * status infra_error / skipped_unsafe runs are EXCLUDED from pass rates but counted and reported.
  * A run passes if `passed` is true, else if all assertions passed. Ungradeable runs are excluded and counted.
  * A metric nobody recorded is reported as {"measured": false}; it is never filled in.
"""
import argparse
from collections import Counter, defaultdict
from pathlib import Path
from _common import (bootstrap_mean_ci, describe, iter_records, load_json, now_iso, rel_change, wilson, write_json)


def cfg_key(r):
    if r.get("configuration", "with_skill") == "without_skill":
        return "without_skill"
    v = r.get("skill_version")
    return f"with_skill@{v}" if v else "with_skill"


def outcome(r, include_sim):
    status = r.get("status", "completed")
    if status == "infra_error":
        return None, "infra_error"
    if status == "skipped_unsafe":
        return None, "skipped_unsafe"
    mode = r.get("execution_mode", "actual")
    if mode != "actual" and not include_sim:
        return None, f"mode_{mode}"
    passed = r.get("passed")
    asserts = r.get("assertions") or []
    if passed is None and asserts:
        passed = all(bool(x.get("passed")) for x in asserts)
    if passed is None and status in ("error", "timeout"):
        passed = False
    if passed is None:
        return None, "ungraded"
    return bool(passed), None


def assertion_counts(r):
    a = r.get("assertions") or []
    return sum(1 for x in a if x.get("passed")), len(a)


def metric_vals(runs, name):
    return [r.get("metrics", {}).get(name) for r in runs]


def load_evals(path):
    data = load_json(path, {}) if path else {}
    out = {}
    for e in (data.get("evals", []) if isinstance(data, dict) else []):
        out[str(e.get("id"))] = {
            "prompt": e.get("prompt"), "category": e.get("category"), "difficulty": e.get("difficulty"),
            "tags": e.get("tags"), "expected_behavior": e.get("expected_behavior") or e.get("expected_output"),
            "positive_or_negative": e.get("positive_or_negative")}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--evals"); ap.add_argument("--include-simulated", action="store_true")
    ap.add_argument("--baseline-config", default="without_skill"); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--benchmark-version", default=None, help="skill version to export in skill-creator benchmark.json format")
    a = ap.parse_args()
    out = Path(a.out)
    evals_meta = load_evals(a.evals)

    records, load_errors = [], []
    for r in iter_records(a.runs):
        if "_load_error" in r:
            load_errors.append(r["_load_error"])
        elif r.get("kind", "functional") == "functional":
            if "eval_id" not in r:
                load_errors.append(f"{r.get('_source')}: record missing eval_id")
                continue
            r["eval_id"] = str(r["eval_id"]); r["_cfg"] = cfg_key(r)
            records.append(r)

    graded = defaultdict(list)                      # cfg -> [(record, passed)]
    excluded = defaultdict(Counter)                 # cfg -> reason -> n
    for r in records:
        p, why = outcome(r, a.include_simulated)
        if p is None:
            excluded[r["_cfg"]][why] += 1
        else:
            graded[r["_cfg"]].append((r, p))

    cfgs = sorted({r["_cfg"] for r in records})
    warnings = []
    if not records:
        warnings.append("No functional run records found: nothing measured.")

    # ---- per eval ----
    by_eval = defaultdict(lambda: defaultdict(list))
    for c, items in graded.items():
        for r, p in items:
            by_eval[r["eval_id"]][c].append((r, p))
    eval_rows = []
    for eid in sorted(by_eval, key=lambda x: (len(x), x)):
        row = {"eval_id": eid, **evals_meta.get(eid, {}), "configs": {}}
        for c, items in by_eval[eid].items():
            k, n = sum(1 for _, p in items if p), len(items)
            ap_, at_ = zip(*[assertion_counts(r) for r, _ in items])
            row["configs"][c] = {
                "n_runs": n, "n_passed": k, "pass_rate": round(k / n, 4), "pass_rate_ci95_wilson": wilson(k, n),
                "flaky": 0 < k < n, "assertion_pass_rate": round(sum(ap_) / sum(at_), 4) if sum(at_) else None,
                "time_seconds": describe(metric_vals([r for r, _ in items], "duration_s")),
                "tokens": describe(metric_vals([r for r, _ in items], "tokens")),
                "tool_calls": describe(metric_vals([r for r, _ in items], "tool_calls")),
                "run_numbers": sorted(r.get("run", 0) for r, _ in items)}
        eval_rows.append(row)
    write_json(out / "evaluations.json", {"schema_version": 1, "generated_at": now_iso(), "evals": eval_rows})

    # ---- per configuration ----
    perf = {}
    for c in cfgs:
        items = graded.get(c, [])
        n = len(items); k = sum(1 for _, p in items if p)
        per_eval = defaultdict(list)
        for r, p in items:
            per_eval[r["eval_id"]].append(p)
        multi = {e: v for e, v in per_eval.items() if len(v) >= 2}
        cons = ({"measured": True, "evals_with_2plus_runs": len(multi),
                 "all_pass": sum(1 for v in multi.values() if all(v)),
                 "all_fail": sum(1 for v in multi.values() if not any(v)),
                 "flaky": sum(1 for v in multi.values() if any(v) and not all(v))}
                if multi else {"measured": False, "reason": "no eval has 2+ graded runs in this configuration"})
        ap_, at_ = (sum(assertion_counts(r)[0] for r, _ in items), sum(assertion_counts(r)[1] for r, _ in items))
        art = [r.get("artifacts_ok") for r, _ in items if r.get("artifacts_ok") is not None]
        runs_only = [r for r, _ in items]
        errs = [r.get("metrics", {}).get("errors") for r in runs_only]
        perf[c] = {
            "n_runs_graded": n, "n_evals": len(per_eval), "n_passed": k,
            "pass_rate": round(k / n, 4) if n else None, "failure_rate": round(1 - k / n, 4) if n else None,
            "pass_rate_ci95_wilson": wilson(k, n),
            "eval_level_mean_pass_rate": round(sum(sum(v) / len(v) for v in per_eval.values()) / len(per_eval), 4) if per_eval else None,
            "min_runs_per_eval": min((len(v) for v in per_eval.values()), default=0),
            "consistency": cons,
            "assertion_pass_rate": round(ap_ / at_, 4) if at_ else None,
            "time_seconds": describe(metric_vals(runs_only, "duration_s")),
            "tokens": describe(metric_vals(runs_only, "tokens")),
            "tool_calls": describe(metric_vals(runs_only, "tool_calls")),
            "errors_per_run": describe(errs),
            "artifact_success": ({"measured": True, "n": len(art), "passed": sum(1 for x in art if x), "rate": round(sum(1 for x in art if x) / len(art), 4)}
                                 if art else {"measured": False, "reason": "no run recorded artifacts_ok"}),
            "execution_modes": dict(Counter(r.get("execution_mode", "actual") for r, _ in items)),
            "excluded_runs": dict(excluded.get(c, {})),
        }
        if n and perf[c]["min_runs_per_eval"] < 3:
            warnings.append(f"{c}: fewer than 3 graded runs for at least one eval; reliability/variance is not assessable for those evals.")
        if len(per_eval) < 10:
            warnings.append(f"{c}: only {len(per_eval)} distinct eval(s); coverage is narrow and any eval-level interval is wide or absent.")
        for why, cnt in excluded.get(c, {}).items():
            if why.startswith("mode_"):
                warnings.append(f"{c}: {cnt} run(s) excluded because execution_mode={why[5:]} (not actual execution). Use --include-simulated to include them, clearly labelled.")

    # ---- deltas vs baseline (paired evals only) ----
    deltas, base = {}, a.baseline_config
    if base not in perf:
        if perf:
            warnings.append(f"No baseline ('{base}') runs graded: skill lift and cost deltas are not measured.")
    else:
        for c in cfgs:
            if c == base:
                continue
            paired = sorted(set(per for per in by_eval if base in by_eval[per] and c in by_eval[per]))
            if not paired:
                deltas[c] = {"measured": False, "reason": "no eval has graded runs in both configurations"}
                continue
            def pooled(cfg):
                rr = [x for e in paired for x in by_eval[e][cfg]]
                return rr, sum(1 for _, p in rr if p), len(rr)
            rb, kb, nb = pooled(base); rs, ks, ns = pooled(c)
            diffs = [sum(p for _, p in by_eval[e][c]) / len(by_eval[e][c]) - sum(p for _, p in by_eval[e][base]) / len(by_eval[e][base]) for e in paired]
            mean_of = lambda rr, nm: (lambda d: d.get("mean") if d["measured"] else None)(describe(metric_vals([r for r, _ in rr], nm)))
            tb, ts = mean_of(rb, "duration_s"), mean_of(rs, "duration_s")
            kb_, ks_ = mean_of(rb, "tokens"), mean_of(rs, "tokens")
            cb, cs = mean_of(rb, "tool_calls"), mean_of(rs, "tool_calls")
            lift = round((ks / ns - kb / nb) * 100, 2)
            deltas[c] = {
                "measured": True, "paired_evals": paired, "baseline_runs": nb, "skill_runs": ns,
                "baseline_pass_rate": round(kb / nb, 4), "skill_pass_rate": round(ks / ns, 4),
                "skill_lift_pp": lift,
                "eval_level_mean_lift_pp": round(sum(diffs) / len(diffs) * 100, 2),
                "eval_level_lift_ci95_bootstrap_pp": ([round(x * 100, 2) for x in ci] if (ci := bootstrap_mean_ci(diffs, seed=a.seed)) else None),
                "ci_note": "Bootstrap over paired evals; resamples eval difficulty only, not run noise. Null when fewer than 5 paired evals.",
                "time_seconds": {"baseline_mean": tb, "skill_mean": ts, "relative_change": rel_change(ts, tb)},
                "tokens": {"baseline_mean": kb_, "skill_mean": ks_, "relative_change": rel_change(ks_, kb_)},
                "tool_calls": {"baseline_mean": cb, "skill_mean": cs, "relative_change": rel_change(cs, cb)},
                "evals_only_one_side": sorted(set(by_eval) - set(paired)),
            }
            if len(paired) < 5:
                warnings.append(f"{c}: only {len(paired)} paired eval(s); the skill-lift bootstrap CI is not computed.")
    write_json(out / "performance.json", {"schema_version": 1, "generated_at": now_iso(),
        "baseline_config": base, "include_simulated": a.include_simulated, "configurations": perf, "deltas_vs_baseline": deltas,
        "load_errors": load_errors, "warnings": sorted(set(warnings)),
        "interpretation_note": "Metrics are descriptive. No overall winner is declared; weigh quality change against cost change."})

    # ---- failures (preserve human diagnosis on re-run) ----
    fpath = out / "failures.json"
    old = {(f["eval_id"], f["configuration"], f["run"]): f for f in (load_json(fpath, {}) or {}).get("failures", [])}
    fails = []
    for c, items in graded.items():
        for r, p in items:
            if p:
                continue
            key = (r["eval_id"], c, r.get("run"))
            failed_a = [{"text": x.get("text"), "evidence": x.get("evidence"), "method": x.get("method")}
                        for x in (r.get("assertions") or []) if not x.get("passed")]
            rec = {"eval_id": r["eval_id"], "configuration": c, "run": r.get("run"), "prompt": r.get("prompt") or evals_meta.get(r["eval_id"], {}).get("prompt"),
                   "expected_behavior": evals_meta.get(r["eval_id"], {}).get("expected_behavior"),
                   "actual_behavior": r.get("actual_summary"), "failed_assertions": failed_a,
                   "status": r.get("status", "completed"), "failure_category": (r.get("failure") or {}).get("category"),
                   "evidence": (r.get("failure") or {}).get("evidence") or [x["evidence"] for x in failed_a if x.get("evidence")],
                   "source_record": r.get("_source"),
                   "diagnosis": {"likely_cause": None, "cause_confidence": None, "suggested_modification": None}}
            if key in old and old[key].get("diagnosis"):
                rec["diagnosis"] = old[key]["diagnosis"]
                rec["failure_category"] = old[key].get("failure_category") or rec["failure_category"]
            fails.append(rec)
    write_json(fpath, {"schema_version": 1, "generated_at": now_iso(),
                       "note": "diagnosis fields are filled by the analyst (null = not yet diagnosed). cause_confidence in {Confirmed cause, Likely cause, Possible cause}.",
                       "failures": fails})

    # ---- skill-creator compatible benchmark.json (optional, for eval-viewer reuse) ----
    skill_keys = [c for c in cfgs if c != "without_skill"]
    if a.benchmark_version:
        skill_keys = [c for c in skill_keys if c.endswith("@" + a.benchmark_version)]
    if len(skill_keys) >= 1 and graded:
        sk = skill_keys[0]
        runs_out, summ = [], {}
        for conf_name, ck in (("with_skill", sk), ("without_skill", "without_skill")):
            vals = defaultdict(list)
            for r, p in graded.get(ck, []):
                pa, ta = assertion_counts(r)
                pr = (pa / ta) if ta else (1.0 if p else 0.0)
                m = r.get("metrics", {})
                runs_out.append({"eval_id": r["eval_id"], "eval_name": r["eval_id"], "configuration": conf_name,
                    "run_number": r.get("run", 1), "result": {"pass_rate": round(pr, 4), "passed": pa, "failed": ta - pa, "total": ta,
                    "time_seconds": m.get("duration_s"), "tokens": m.get("tokens"), "tool_calls": m.get("tool_calls"), "errors": m.get("errors", 0)},
                    "expectations": [{"text": x.get("text"), "passed": bool(x.get("passed")), "evidence": x.get("evidence", "")} for x in (r.get("assertions") or [])],
                    "notes": []})
                vals["pass_rate"].append(pr)
                for nm, src in (("time_seconds", "duration_s"), ("tokens", "tokens")):
                    if m.get(src) is not None:
                        vals[nm].append(m[src])
            def st(v):
                d = describe(v)
                return {"mean": d.get("mean"), "stddev": d.get("stddev") or 0.0, "min": d.get("min"), "max": d.get("max")} if d["measured"] else {"mean": None, "stddev": None, "min": None, "max": None}
            summ[conf_name] = {k: st(v) for k, v in vals.items()} if vals else {}
        delta = {}
        if summ.get("with_skill") and summ.get("without_skill"):
            for k in ("pass_rate", "time_seconds", "tokens"):
                x, y = summ["with_skill"].get(k, {}).get("mean"), summ["without_skill"].get(k, {}).get("mean")
                if x is not None and y is not None:
                    delta[k] = f"{x - y:+.2f}" if k == "pass_rate" else f"{x - y:+.1f}"
        write_json(out / "benchmark.json", {"metadata": {"skill_name": None, "skill_path": None, "executor_model": None, "analyzer_model": None,
                   "timestamp": now_iso(), "evals_run": sorted(by_eval), "runs_per_configuration": max((perf[c]["min_runs_per_eval"] for c in perf), default=0),
                   "_note": "pass_rate here is the per-run ASSERTION pass rate (skill-creator convention), not task pass rate."},
                   "runs": runs_out, "run_summary": {**summ, "delta": delta}, "notes": []})

    # ---- console summary ----
    for c, p in perf.items():
        ci = p["pass_rate_ci95_wilson"]
        print(f"{c}: pass {p['n_passed']}/{p['n_runs_graded']}" + (f" = {p['pass_rate']:.1%} (95% CI {ci[0]:.1%}-{ci[1]:.1%})" if ci else "") + f"; excluded={p['excluded_runs']}")
    for c, d in deltas.items():
        if d.get("measured"):
            print(f"lift {c} vs {base}: {d['skill_lift_pp']:+.1f} pp over {len(d['paired_evals'])} paired eval(s)")
    for w in sorted(set(warnings)):
        print("warning:", w)
    for e in load_errors:
        print("load error:", e)


if __name__ == "__main__":
    main()
