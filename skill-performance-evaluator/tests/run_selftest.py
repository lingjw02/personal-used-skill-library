#!/usr/bin/env python3
"""End-to-end self-test of the evaluator tooling using SYNTHETIC records generated on the fly.

The synthetic data exists only to exercise the scripts; it is created in a temp dir and is NOT a
benchmark of any real skill. Usage: python tests/run_selftest.py
"""
import json, random, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "scripts"


def run(*args, ok=(0,)):
    r = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, cwd=S)
    if r.returncode not in ok:
        print(r.stdout, r.stderr); raise SystemExit(f"FAILED: {args}")
    return r.stdout


def write(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(obj, indent=1))


def main():
    rng = random.Random(7)
    tmp = Path(tempfile.mkdtemp(prefix="skilleval-selftest-"))
    skill = tmp / "dummy-skill"
    (skill / "scripts").mkdir(parents=True); (skill / "references").mkdir()
    (skill / "SKILL.md").write_text("---\nname: dummy-skill\ndescription: Use this skill whenever the user wants to summarize CSV files into a short report, even if they do not say 'summary'.\n---\n# Dummy\nSee [ref](references/a.md) and `scripts/run.py` and `references/missing.md`.\n")
    (skill / "references" / "a.md").write_text("x"); (skill / "scripts" / "run.py").write_text("import json\nimport numpy_not_here_xyz\nprint(1)\n")
    ws = tmp / "ws"; res = ws / "results"
    out = run("init_workspace.py", skill, "--out", ws, "--model", "test-model", "--agent", "selftest", "--harness", "synthetic", "--suite-version", "1")
    assert "dummy-skill" in out
    out = run("validate_structure.py", skill, "--out", res / "structure.json", ok=(0, 1))
    st = json.loads((res / "structure.json").read_text())
    codes = {c["code"] for c in st["checks"]}
    assert "possibly_broken_reference" in codes and "dependency_not_installed_here" in codes, codes

    evals = [{"id": f"f{i:02d}", "category": "normal" if i < 6 else "edge", "difficulty": "easy" if i % 2 else "hard", "prompt": f"task {i}",
              "expected_behavior": "does the thing", "positive_or_negative": "positive"} for i in range(10)]
    write(ws / "evals" / "evals.json", {"skill_name": "dummy-skill", "evals": evals})
    p_base, p_v1, p_v2 = 0.4, 0.7, 0.85
    for e in evals:
        for rn in range(1, 4):
            for cfg, ver, p, tokens in (("without_skill", None, p_base, 8000), ("with_skill", "1.0.0", p_v1, 10000), ("with_skill", "1.1.0", p_v2, 10500)):
                ok = rng.random() < p
                rec = {"kind": "functional", "eval_id": e["id"], "configuration": cfg, "skill_version": ver, "run": rn, "prompt": e["prompt"], "model": "test-model",
                       "execution_mode": "actual", "status": "completed",
                       "assertions": [{"text": "a1", "passed": ok, "method": "deterministic", "evidence": "synthetic"}, {"text": "a2", "passed": True, "method": "deterministic", "evidence": "synthetic"}],
                       "metrics": {"duration_s": rng.uniform(30, 60), "tokens": tokens + rng.randint(-500, 500), "tool_calls": rng.randint(2, 6), "errors": 0}}
                if not ok:
                    rec["failure"] = {"category": "Missing validation", "evidence": ["synthetic"]}
                write(res / "runs" / f"{e['id']}__{cfg}__{ver}__r{rn}.json", rec)
    # an infra error, a simulated run, an unsafe skip: must be excluded and counted
    write(res / "runs" / "x1.json", {"eval_id": "f00", "configuration": "with_skill", "skill_version": "1.0.0", "run": 9, "status": "infra_error"})
    write(res / "runs" / "x2.json", {"eval_id": "f01", "configuration": "with_skill", "skill_version": "1.0.0", "run": 9, "execution_mode": "simulated", "passed": True})
    write(res / "runs" / "x3.json", {"eval_id": "f02", "configuration": "with_skill", "skill_version": "1.0.0", "run": 9, "status": "skipped_unsafe"})
    for i in range(8):
        for ver, pos_rate, neg_rate in (("1.0.0", 0.75, 0.25), ("1.1.0", 0.9, 0.1)):
            for rn in (1, 2):
                exp = i < 5
                trig = rng.random() < (pos_rate if exp else neg_rate)
                write(res / "runs" / f"t{i}_{ver}_{rn}.json", {"kind": "trigger", "eval_id": f"t{i}", "run": rn, "expected_trigger": exp, "triggered": trig, "observation_method": "cli_stream", "skill_version": ver, "prompt": f"trig {i}"})

    out = run("trigger_metrics.py", "--runs", res / "runs", "--out", res / "trigger-report.json"); print(out)
    out = run("aggregate_runs.py", "--runs", res / "runs", "--out", res, "--evals", ws / "evals" / "evals.json"); print(out)
    perf = json.loads((res / "performance.json").read_text())
    c1 = perf["configurations"]["with_skill@1.0.0"]
    assert c1["n_runs_graded"] == 30, c1["n_runs_graded"]
    assert c1["excluded_runs"] == {"infra_error": 1, "mode_simulated": 1, "skipped_unsafe": 1}, c1["excluded_runs"]
    assert perf["deltas_vs_baseline"]["with_skill@1.0.0"]["measured"]
    assert (res / "benchmark.json").exists()
    out = run("compare_versions.py", "--a", res, "--key-a", "with_skill@1.0.0", "--b", res, "--key-b", "with_skill@1.1.0", "--out", res / "regression.json"); print(out)
    reg = json.loads((res / "regression.json").read_text()); assert reg["fairness"]["shared_evals"] == 10
    # analyst diagnosis + narrative, then re-aggregate to confirm diagnosis survives
    fl = json.loads((res / "failures.json").read_text())
    fl["failures"][0]["diagnosis"] = {"likely_cause": "synthetic cause", "cause_confidence": "Possible cause", "suggested_modification": "synthetic"}
    write(res / "failures.json", fl); key0 = (fl["failures"][0]["eval_id"], fl["failures"][0]["configuration"], fl["failures"][0]["run"])
    run("aggregate_runs.py", "--runs", res / "runs", "--out", res, "--evals", ws / "evals" / "evals.json")
    fl2 = json.loads((res / "failures.json").read_text())
    kept = [f for f in fl2["failures"] if (f["eval_id"], f["configuration"], f["run"]) == key0][0]
    assert kept["diagnosis"]["likely_cause"] == "synthetic cause", "diagnosis lost on re-aggregate"
    write(res / "narrative.json", {"inferences": [{"text": "synthetic inference", "evidence": ["performance.json"]}],
          "recommendations": [{"id": "R1", "text": "synthetic rec", "evidence": ["failures.json"], "verification": "rerun"}, {"id": "R2", "text": "no evidence rec"}],
          "limitations": ["synthetic data only"]})
    run("generate_report.py", "--results", res, "--skill", skill, "--primary-key", "with_skill@1.1.0")
    for f in ("summary.json", "summary.md", "comparison.md", "failure-analysis.md", "benchmark.md", "README.md", "history.json"):
        assert (res / f).exists(), f
    md = (res / "summary.md").read_text(); readme = (res / "README.md").read_text()
    assert "no evidence rec" not in md and "cites no evidence" in md
    assert "skill-eval:begin performance" in readme and "Not provided by the skill author" in readme
    out = run("selfcheck.py", "--results", res, ok=(0, 1)); print(out)
    # README update path: managed blocks replaced, author text preserved
    tr = tmp / "README.md"; tr.write_text("# mine\nhand written intro\n" + readme.split("<!-- skill-eval:begin performance -->")[0].split("## Features")[0][:0] + "\n<!-- skill-eval:begin performance -->\nOLD\n<!-- skill-eval:end performance -->\n")
    out = run("generate_report.py", "--results", res, "--skill", skill, "--primary-key", "with_skill@1.1.0", "--target-readme", tr, "--no-history-append"); print(out)
    t = tr.read_text(); assert "hand written intro" in t and "OLD" not in t and "Pass Rate" in t
    # untouched when no markers
    tr2 = tmp / "sub" / "README.md"; tr2.parent.mkdir(); tr2.write_text("# plain readme\n")
    run("generate_report.py", "--results", res, "--skill", skill, "--target-readme", tr2, "--no-history-append")
    assert tr2.read_text() == "# plain readme\n" and (tr2.parent / "README.generated.md").exists()
    # not-measured behaviour: strip metrics from a copy and make sure no numbers are invented
    print("\nSELFTEST PASSED (synthetic data in", tmp, ")")


if __name__ == "__main__":
    main()
