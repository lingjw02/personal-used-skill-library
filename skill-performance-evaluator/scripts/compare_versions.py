#!/usr/bin/env python3
"""LEVEL 6 - Regression / version comparison. Produces results/regression.json.

Usage:
  # two results dirs (each produced by aggregate_runs.py)
  python compare_versions.py --a results_v1 --b results_v2 --out results_v2/regression.json
  # two versions inside ONE results dir (runs carry skill_version)
  python compare_versions.py --a results --key-a with_skill@1.0.0 --b results --key-b with_skill@1.1.0 --out results/regression.json

Per eval, A->B is classified improved / regressed / unchanged / insufficient_data. A change is "observed"
when |delta pass rate| >= --min-delta; it is "supported" only if Fisher's exact test p < --alpha.
Observed-but-unsupported changes are reported as such: with few runs most real changes are unsupported.
No overall winner is declared.
"""
import argparse, sys
from pathlib import Path
from _common import fisher_exact, load_json, now_iso, rel_change, write_json


def pick_key(perf, requested, label):
    keys = [k for k in perf["configurations"] if k != "without_skill"]
    if requested:
        if requested not in perf["configurations"]:
            sys.exit(f"error: key '{requested}' not in {label}; available: {list(perf['configurations'])}")
        return requested
    if len(keys) != 1:
        sys.exit(f"error: {label} has skill configurations {keys}; pass --key-a/--key-b")
    return keys[0]


def load(d, key):
    d = Path(d)
    perf = load_json(d / "performance.json")
    ev = load_json(d / "evaluations.json")
    if not perf or not ev:
        sys.exit(f"error: {d} lacks performance.json/evaluations.json (run aggregate_runs.py first)")
    k = pick_key(perf, key, str(d))
    return {"dir": str(d), "key": k, "perf": perf["configurations"][k], "evals": {e["eval_id"]: e["configs"].get(k) for e in ev["evals"] if e["configs"].get(k)},
            "meta": load_json(d / "metadata.json", {}) or {}, "env": load_json(d / "environment.json", {}) or {},
            "trig": (load_json(d / "trigger-report.json", {}) or {}).get("by_version", {}),
            "fails": [f for f in (load_json(d / "failures.json", {}) or {}).get("failures", []) if f["configuration"] == k]}


def trig_for(side):
    ver = side["key"].split("@", 1)[1] if "@" in side["key"] else None
    t = side["trig"].get(ver) or (next(iter(side["trig"].values())) if len(side["trig"]) == 1 else None)
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True); ap.add_argument("--b", required=True)
    ap.add_argument("--key-a"); ap.add_argument("--key-b"); ap.add_argument("--out", required=True)
    ap.add_argument("--min-delta", type=float, default=0.2); ap.add_argument("--alpha", type=float, default=0.05)
    a = ap.parse_args()
    A, B = load(a.a, a.key_a), load(a.b, a.key_b)

    warnings = []
    sa, sb = A["meta"].get("suite_version"), B["meta"].get("suite_version")
    ma, mb = A["env"].get("model"), B["env"].get("model")
    fair = {"same_suite_version": (sa == sb) if sa and sb else None, "same_model": (ma == mb) if ma and mb else None,
            "suite_versions": [sa, sb], "models": [ma, mb]}
    if fair["same_suite_version"] is False:
        warnings.append(f"Test suite versions differ ({sa} vs {sb}): differences may reflect the suite, not the skill.")
    if fair["same_model"] is False:
        warnings.append(f"Models differ ({ma} vs {mb}): differences may reflect the model, not the skill.")
    if fair["same_suite_version"] is None or fair["same_model"] is None:
        warnings.append("Suite version or model not recorded for at least one side; comparison fairness cannot be verified.")
    shared = sorted(set(A["evals"]) & set(B["evals"]))
    only_a, only_b = sorted(set(A["evals"]) - set(B["evals"])), sorted(set(B["evals"]) - set(A["evals"]))
    if only_a or only_b:
        warnings.append(f"Eval sets differ (only in A: {only_a}; only in B: {only_b}); aggregate comparison uses shared evals only where stated.")

    rows, imp, reg, same, insuf, newf, remf = [], [], [], [], [], [], []
    for e in shared:
        x, y = A["evals"][e], B["evals"][e]
        if x["n_runs"] == 0 or y["n_runs"] == 0:
            cls, supported, p, d = "insufficient_data", None, None, None
        else:
            d = round(y["pass_rate"] - x["pass_rate"], 4)
            p = fisher_exact(x["n_passed"], x["n_runs"], y["n_passed"], y["n_runs"])
            supported = (p is not None and p < a.alpha)
            cls = "improved" if d >= a.min_delta else "regressed" if d <= -a.min_delta else "unchanged"
        rows.append({"eval_id": e, "a": {"passed": x["n_passed"], "runs": x["n_runs"], "pass_rate": x["pass_rate"]},
                     "b": {"passed": y["n_passed"], "runs": y["n_runs"], "pass_rate": y["pass_rate"]},
                     "delta_pass_rate": d, "classification": cls, "statistically_supported": supported, "fisher_p": p})
        {"improved": imp, "regressed": reg, "unchanged": same, "insufficient_data": insuf}[cls].append(e)
        if x["pass_rate"] == 1 and y["pass_rate"] < 1:
            newf.append(e)
        if x["pass_rate"] < 1 and y["pass_rate"] == 1:
            remf.append(e)

    def cats(side):
        return sorted({f.get("failure_category") for f in side["fails"] if f.get("failure_category")})
    ca, cb = cats(A), cats(B)

    pa, pb = A["perf"], B["perf"]
    agg = {"pass_rate": {"a": pa["pass_rate"], "b": pb["pass_rate"],
                         "delta_pp": round((pb["pass_rate"] - pa["pass_rate"]) * 100, 2) if pa["pass_rate"] is not None and pb["pass_rate"] is not None else None,
                         "a_ci95": pa["pass_rate_ci95_wilson"], "b_ci95": pb["pass_rate_ci95_wilson"],
                         "fisher_p_run_level_approx": fisher_exact(pa["n_passed"], pa["n_runs_graded"], pb["n_passed"], pb["n_runs_graded"]),
                         "note": "Run-level Fisher p treats runs as independent; evals are not, so it is approximate. Prefer the per-eval table."}}
    for m in ("time_seconds", "tokens", "tool_calls"):
        va, vb = (pa[m].get("mean") if pa[m]["measured"] else None), (pb[m].get("mean") if pb[m]["measured"] else None)
        agg[m] = {"a_mean": va, "b_mean": vb, "relative_change": rel_change(vb, va), "measured": va is not None and vb is not None}
    ta, tb = trig_for(A), trig_for(B)
    trig = {}
    for m in ("precision", "recall", "f1"):
        va = ta["metrics"][m].get("value") if ta and ta["metrics"][m].get("measured") else None
        vb = tb["metrics"][m].get("value") if tb and tb["metrics"][m].get("measured") else None
        trig[m] = {"a": va, "b": vb, "delta_pp": round((vb - va) * 100, 2) if va is not None and vb is not None else None}
    if not (ta and tb):
        warnings.append("Trigger metrics not available for both sides: trigger-behaviour change not measured.")

    nr = len(reg)
    result = {"schema_version": 1, "generated_at": now_iso(),
              "a": {"dir": A["dir"], "key": A["key"], "skill_version": A["meta"].get("skill_version")},
              "b": {"dir": B["dir"], "key": B["key"], "skill_version": B["meta"].get("skill_version")},
              "thresholds": {"min_delta": a.min_delta, "alpha": a.alpha},
              "fairness": {**fair, "shared_evals": len(shared), "only_in_a": only_a, "only_in_b": only_b},
              "aggregate": agg, "trigger": trig, "per_eval": rows,
              "improvements": imp, "regressions": reg, "unchanged": same, "insufficient_data": insuf,
              "new_failures": newf, "removed_failures": remf,
              "failure_categories": {"a": ca, "b": cb, "new_in_b": sorted(set(cb) - set(ca)), "removed_in_b": sorted(set(ca) - set(cb)), "persisting": sorted(set(ca) & set(cb))},
              "regression_rate": round(nr / len(shared), 4) if shared else None,
              "warnings": warnings,
              "note": "No overall winner is declared. 'improved/regressed' = observed change >= min_delta; consult statistically_supported before treating it as real."}
    write_json(a.out, result)
    print(f"A={A['key']} B={B['key']} shared evals={len(shared)}")
    print(f"improved={imp} regressed={reg} unchanged={len(same)} new_failures={newf} removed_failures={remf}")
    sup = [r['eval_id'] for r in rows if r['statistically_supported'] and r['classification'] in ('improved', 'regressed')]
    print(f"statistically supported changes (p<{a.alpha}): {sup or 'none'}")
    for w in warnings:
        print("warning:", w)


if __name__ == "__main__":
    main()
