#!/usr/bin/env python3
"""Convert skill-creator's run_eval.py JSON output into trigger run records for trigger_metrics.py.

Usage:
  python import_trigger_eval.py <run_eval_output.json> --runs results/runs --skill-version 1.0.0 [--prefix t]

run_eval.py reports per-query aggregates ({"query","should_trigger","triggers","runs"}). This importer
expands each into `runs` individual records (triggers x True, remainder x False) with
observation_method="cli_stream". CAVEAT: run_eval.py counts a failed/timed-out query as "not triggered",
which biases recall downward; if you saw 'Warning: query failed' lines, treat recall as a lower bound.
"""
import argparse, json, sys
from pathlib import Path
from _common import write_json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input"); ap.add_argument("--runs", required=True)
    ap.add_argument("--skill-version", default=None); ap.add_argument("--prefix", default="t")
    a = ap.parse_args()
    data = json.loads(Path(a.input).read_text(encoding="utf-8"))
    results = data["results"] if isinstance(data, dict) else data
    n = 0
    for i, r in enumerate(results, 1):
        eid = f"{a.prefix}{i:02d}"
        for j in range(int(r["runs"])):
            write_json(Path(a.runs) / f"trigger_{eid}_{a.skill_version or 'target'}_r{j + 1}.json", {
                "kind": "trigger", "eval_id": eid, "run": j + 1, "prompt": r["query"],
                "expected_trigger": bool(r["should_trigger"]), "triggered": j < int(r["triggers"]),
                "observation_method": "cli_stream", "skill_version": a.skill_version,
                "note": "expanded from per-query aggregate; run order within a query is not meaningful"})
            n += 1
    print(f"wrote {n} trigger records for {len(results)} queries")


if __name__ == "__main__":
    main()
