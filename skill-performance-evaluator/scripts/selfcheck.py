#!/usr/bin/env python3
"""Three-pass self-validation of an evaluation before it is reported.

Usage: python selfcheck.py --results results [--runs results/runs] [--docs results/summary.md results/README.md]

PASS 1 FACT/EVIDENCE  - metrics recompute from raw run records; every % / pp / s / k number in the docs traces to JSON.
PASS 2 LOGIC          - baseline and skill used the same evals, prompts, model; recommendations cite evidence.
PASS 3 RISK           - stochastic effects, missing environment info, unmeasured metrics, weak trigger evidence.
Exit code 1 if any error-level finding (the report must be corrected before it is delivered).
"""
import argparse, re, sys
from collections import defaultdict
from pathlib import Path
from _common import iter_records, load_json, now_iso, write_json
from aggregate_runs import cfg_key, outcome

MARKETING = re.compile(r"\b(high[- ]quality|excellent|outstanding|best[- ]in[- ]class|robust|world[- ]class|impressive|flawless|superior)\b", re.I)
NUM = re.compile(r"(?<![\w.])([+-]?\d+(?:\.\d+)?)\s*(%|pp\b|s\b|k\b)")
RANGE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\u2013(\d+(?:\.\d+)?)%")
CONSTANTS = {0.0, 95.0, 100.0}
TOL = 0.051  # values are printed to 1 decimal; allow display rounding only


def numbers_in(obj, acc):
    if isinstance(obj, bool) or obj is None:
        return
    if isinstance(obj, (int, float)):
        acc.add(float(obj))
    elif isinstance(obj, dict):
        for v in obj.values(): numbers_in(v, acc)
    elif isinstance(obj, list):
        for v in obj: numbers_in(v, acc)


def allowed_numbers(res):
    """Return (raw, pct, kilo) sets of numbers present in the results JSON, in the units reports print."""
    raw = set()
    for p in res.glob("*.json"):
        if p.name == "selfcheck.json":
            continue
        numbers_in(load_json(p), raw)
    return raw, {x * 100 for x in raw}, {x / 1000 for x in raw}


def traceable(v, unit, sets):
    raw, pct, kilo = sets
    v = abs(v)
    pool = {"%": pct | raw, "pp": raw | pct, "s": raw, "k": kilo}[unit]
    return v in CONSTANTS or any(abs(v - a) <= TOL for a in pool)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True); ap.add_argument("--runs"); ap.add_argument("--docs", nargs="*")
    a = ap.parse_args()
    res = Path(a.results); runs_dir = a.runs or str(res / "runs")
    docs = [Path(p) for p in (a.docs if a.docs else [res / "summary.md", res / "README.md"]) if Path(p).exists()]
    passes = {k: [] for k in ("fact", "logic", "risk")}
    F = lambda p, lvl, code, msg: passes[p].append({"level": lvl, "code": code, "message": msg})

    perf, narr = load_json(res / "performance.json"), load_json(res / "narrative.json", {}) or {}
    env, meta = load_json(res / "environment.json", {}) or {}, load_json(res / "metadata.json", {}) or {}
    if not perf:
        F("fact", "error", "no_performance_json", "performance.json missing; no measured metrics to validate")

    # ---- raw records ----
    recs = [r for r in iter_records(runs_dir) if "_load_error" not in r and r.get("kind", "functional") == "functional" and "eval_id" in r]
    inc_sim = bool(perf and perf.get("include_simulated"))
    graded = defaultdict(list)
    for r in recs:
        r["eval_id"] = str(r["eval_id"]); c = cfg_key(r)
        p, why = outcome(r, inc_sim)
        if p is not None:
            graded[c].append((r, p))

    # PASS 1
    if perf:
        for c, d in perf["configurations"].items():
            n, k = len(graded.get(c, [])), sum(1 for _, p in graded.get(c, []) if p)
            if (n, k) != (d["n_runs_graded"], d["n_passed"]):
                F("fact", "error", "recompute_mismatch", f"{c}: performance.json says {d['n_passed']}/{d['n_runs_graded']} but raw records give {k}/{n} (re-run aggregate_runs.py)")
            for m, f in (("time_seconds", "duration_s"), ("tokens", "tokens"), ("tool_calls", "tool_calls")):
                vals = [r.get("metrics", {}).get(f) for r, _ in graded.get(c, []) if isinstance(r.get("metrics", {}).get(f), (int, float))]
                if bool(vals) != bool(d[m]["measured"]):
                    F("fact", "error", "measured_flag_mismatch", f"{c}: {m} measured={d[m]['measured']} but raw records have {len(vals)} value(s)")
        if "without_skill" in perf["configurations"] and len(perf["configurations"]) > 1 and not any(d.get("measured") for d in perf.get("deltas_vs_baseline", {}).values()):
            F("fact", "warn", "no_delta", "baseline present but no paired delta could be computed")
    sets = allowed_numbers(res) if perf else (set(), set(), set())
    for dpath in docs:
        text = dpath.read_text(encoding="utf-8")
        for m in MARKETING.finditer(text):
            F("fact", "warn", "marketing_language", f"{dpath.name}: '{m.group(0)}' is evaluative language; replace with a measured statement")
        unsourced = set()
        for m in NUM.finditer(text):
            if not traceable(float(m.group(1)), m.group(2).rstrip(), sets):
                unsourced.add(m.group(0))
        for m in RANGE.finditer(text):
            for g in (m.group(1), m.group(2)):
                if not traceable(float(g), "%", sets):
                    unsourced.add(g + "%")
        for tok_ in sorted(unsourced)[:15]:
            F("fact", "warn", "unsourced_number", f"{dpath.name}: '{tok_}' not traceable to any results JSON (hand-typed or stale number?)")
    for e in narr.get("recommendations", []):
        if not e.get("evidence"):
            F("fact", "error", "recommendation_without_evidence", f"recommendation {e.get('id', '?')} cites no evidence")
    for x in narr.get("inferences", []):
        if not x.get("evidence"):
            F("fact", "warn", "inference_without_evidence", f"inference '{x.get('text', '')[:60]}' cites no evidence")

    # PASS 2
    if "without_skill" in graded:
        base_by = defaultdict(list)
        for r, _ in graded["without_skill"]: base_by[r["eval_id"]].append(r)
        for c, items in graded.items():
            if c == "without_skill": continue
            sk_by = defaultdict(list)
            for r, _ in items: sk_by[r["eval_id"]].append(r)
            for e in sorted(set(base_by) ^ set(sk_by)):
                F("logic", "warn", "unpaired_eval", f"{c}: eval {e} has graded runs in only one of baseline/skill; it is excluded from the delta")
            for e in set(base_by) & set(sk_by):
                pb = {r.get("prompt") for r in base_by[e] if r.get("prompt")}; ps = {r.get("prompt") for r in sk_by[e] if r.get("prompt")}
                if pb and ps and pb != ps:
                    F("logic", "error", "prompt_mismatch", f"eval {e}: baseline and skill used different prompts; the comparison is unfair")
                if len(base_by[e]) != len(sk_by[e]):
                    F("logic", "warn", "run_count_mismatch", f"eval {e}: {len(base_by[e])} baseline vs {len(sk_by[e])} skill runs")
            mods = {(r.get("model") or "unrecorded") for r, _ in items + graded["without_skill"]}
            if len(mods) > 1:
                F("logic", "error" if "unrecorded" not in mods else "warn", "model_mismatch", f"baseline/skill runs used models {sorted(mods)}; differences may not be caused by the skill")
    else:
        F("logic", "warn", "no_baseline", "no baseline runs: causal 'skill improves X' claims are not supported")
    for c, items in graded.items():
        modes = {r.get("execution_mode", "actual") for r, _ in items}
        if len(modes) > 1:
            F("logic", "warn", "mixed_execution_modes", f"{c}: graded runs mix execution modes {sorted(modes)}")
    reg = load_json(res / "regression.json")
    if reg:
        for w in reg.get("warnings", []):
            F("logic", "warn", "regression_fairness", w)
        if reg.get("fairness", {}).get("same_suite_version") is False:
            F("logic", "error", "suite_mismatch", "regression compares different test suite versions")
    for dpath in docs:
        t = dpath.read_text(encoding="utf-8")
        if re.search(r"\b(proves?|caused? by the skill|guarantees?)\b", t, re.I):
            F("logic", "warn", "causal_language", f"{dpath.name}: strong causal wording found; check the evidence supports it")
        for line in t.splitlines():
            if re.search(r"\b(winner|better overall|superior)\b", line, re.I) and not re.search(r"\b(no|not|without|never|avoid)\b[^.]{0,40}\b(winner|declar)", line, re.I):
                F("logic", "warn", "single_winner_language", f"{dpath.name}: possible overall-winner wording: '{line.strip()[:80]}'")
                break

    # PASS 3
    for k in ("model", "agent", "harness"):
        if not env.get(k):
            F("risk", "warn", f"env_{k}_missing", f"environment.json has no {k}; reproducibility information is incomplete")
    if perf:
        for c, d in perf["configurations"].items():
            if 0 < d["min_runs_per_eval"] < 3:
                F("risk", "warn", "few_runs", f"{c}: min runs per eval is {d['min_runs_per_eval']}; stochastic variation not assessed")
            for m in ("time_seconds", "tokens", "tool_calls"):
                if not d[m]["measured"]:
                    F("risk", "info", "metric_not_measured", f"{c}: {m} not recorded (must be reported as Not measured)")
            if d["excluded_runs"]:
                F("risk", "info", "excluded_runs", f"{c}: excluded runs {d['excluded_runs']} are disclosed, not hidden")
    tr = load_json(res / "trigger-report.json")
    if tr:
        for v, g in tr["by_version"].items():
            for l in g["limitations"]:
                F("risk", "info", "trigger_limitation", f"{v}: {l}")
    else:
        F("risk", "info", "no_trigger_data", "trigger behaviour not measured")
    if not narr.get("limitations"):
        F("risk", "info", "no_limitations_text", "narrative.json lists no analyst-written limitations; confirm none apply")
    if not (res / "structure.json").exists():
        F("risk", "info", "no_structure_check", "structure validation output missing")

    summary = {}
    for p, items in passes.items():
        e = sum(1 for i in items if i["level"] == "error"); w = sum(1 for i in items if i["level"] == "warn")
        summary[p] = {"status": "fail" if e else "pass_with_warnings" if w else "pass", "errors": e, "warnings": w, "findings": items}
    overall = "fail" if any(v["status"] == "fail" for v in summary.values()) else "pass_with_warnings" if any(v["status"] != "pass" for v in summary.values()) else "pass"
    write_json(res / "selfcheck.json", {"schema_version": 1, "generated_at": now_iso(), "overall": overall, "passes": summary})
    for p, v in summary.items():
        print(f"PASS {p.upper():5}: {v['status']} ({v['errors']} errors, {v['warnings']} warnings)")
        for i in v["findings"]:
            if i["level"] != "info": print(f"   [{i['level']}] {i['code']}: {i['message']}")
    print("overall:", overall)
    sys.exit(1 if overall == "fail" else 0)


if __name__ == "__main__":
    main()
