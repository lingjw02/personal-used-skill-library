#!/usr/bin/env python3
"""LEVEL 2 - Compute trigger confusion matrix and metrics from trigger run records.

Usage: python trigger_metrics.py --runs results/runs --out results/trigger-report.json

Consumes records with "kind": "trigger" (see references/schemas.md):
  {"kind":"trigger","eval_id":"t01","run":1,"expected_trigger":true,"triggered":true|false|null,
   "observation_method":"cli_stream|transcript_skill_read|self_report|not_observable",
   "skill_version":"1.0.0","prompt":"..."}
triggered=null means the harness could not observe triggering; those records are excluded from the
confusion matrix and counted separately. Nothing is imputed.
"""
import argparse
from collections import Counter, defaultdict
from _common import iter_records, now_iso, wilson, write_json


def metric(num, den, label, kind="proportion"):
    if den == 0:
        return {"measured": False, "reason": f"denominator is 0 ({label})"}
    out = {"measured": True, "value": round(num / den, 4), "denominator": den}
    if kind == "proportion":
        out["ci95_wilson"] = wilson(num, den)
    return out


def analyse(rows):
    obs = [r for r in rows if r.get("triggered") is not None]
    tp = sum(1 for r in obs if r["expected_trigger"] and r["triggered"])
    fn = sum(1 for r in obs if r["expected_trigger"] and not r["triggered"])
    fp = sum(1 for r in obs if not r["expected_trigger"] and r["triggered"])
    tn = sum(1 for r in obs if not r["expected_trigger"] and not r["triggered"])
    f1 = metric(2 * tp, 2 * tp + fp + fn, "2TP+FP+FN", kind="ratio")
    methods = Counter(r.get("observation_method", "unspecified") for r in rows)
    per_case = defaultdict(list)
    for r in obs:
        per_case[r["eval_id"]].append(r)
    cases = []
    for cid, rs in sorted(per_case.items()):
        t = sum(1 for r in rs if r["triggered"])
        exp = rs[0]["expected_trigger"]
        cases.append({"eval_id": cid, "expected_trigger": exp, "runs": len(rs), "triggered_count": t,
                      "trigger_rate": round(t / len(rs), 4), "consistent": t in (0, len(rs)),
                      "prompt": rs[0].get("prompt")})
    lim = []
    if methods and set(methods) <= {"self_report"}:
        lim.append("All trigger observations are agent self-reports; they were not independently verified (weak evidence).")
    if len(obs) < len(rows):
        lim.append(f"{len(rows) - len(obs)} record(s) had no observable trigger signal and are excluded (not imputed).")
    if not any(r["expected_trigger"] for r in obs):
        lim.append("No positive cases observed: recall and F1 are not meaningful.")
    if not any(not r["expected_trigger"] for r in obs):
        lim.append("No negative cases observed: precision and specificity are not meaningful.")
    if any(c["runs"] > 1 for c in cases):
        lim.append("Run-level CIs treat repeated runs of the same prompt as independent; they are approximate.")
    if len({c["eval_id"] for c in cases}) < 10:
        lim.append("Fewer than 10 distinct trigger prompts: rates are unstable; read the Wilson intervals, not the point values.")
    return {
        "n_records": len(rows), "observable_records": len(obs), "unobservable_records": len(rows) - len(obs),
        "observation_methods": dict(methods),
        "confusion": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
        "metrics": {
            "precision": metric(tp, tp + fp, "TP+FP"), "recall": metric(tp, tp + fn, "TP+FN"),
            "specificity": metric(tn, tn + fp, "TN+FP"), "f1": f1,
            "accuracy": metric(tp + tn, len(obs), "observable records"),
        },
        "per_case": cases,
        "missed_positive_cases": [c["eval_id"] for c in cases if c["expected_trigger"] and c["trigger_rate"] < 1],
        "false_trigger_cases": [c["eval_id"] for c in cases if not c["expected_trigger"] and c["trigger_rate"] > 0],
        "inconsistent_cases": [c["eval_id"] for c in cases if not c["consistent"]],
        "limitations": lim,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows, errors = [], []
    for r in iter_records(a.runs):
        if "_load_error" in r:
            errors.append(r["_load_error"])
        elif r.get("kind") == "trigger":
            if "expected_trigger" not in r or "eval_id" not in r:
                errors.append(f"{r.get('_source')}: trigger record missing eval_id/expected_trigger")
            else:
                r["eval_id"] = str(r["eval_id"])
                rows.append(r)
    groups = defaultdict(list)
    for r in rows:
        groups[str(r.get("skill_version") or "target")].append(r)
    report = {"schema_version": 1, "generated_at": now_iso(), "load_errors": errors,
              "by_version": {v: analyse(rs) for v, rs in sorted(groups.items())}}
    if not rows:
        report["note"] = "Not measured: no trigger records found."
    write_json(a.out, report)
    for v, g in report["by_version"].items():
        m = g["metrics"]
        fmt = lambda x: f"{x['value']:.3f}" if x.get("measured") else "n/m"
        print(f"{v}: TP={g['confusion']['tp']} FP={g['confusion']['fp']} TN={g['confusion']['tn']} FN={g['confusion']['fn']} "
              f"precision={fmt(m['precision'])} recall={fmt(m['recall'])} f1={fmt(m['f1'])}")
    if not rows:
        print("Not measured: no trigger records found.")


if __name__ == "__main__":
    main()
