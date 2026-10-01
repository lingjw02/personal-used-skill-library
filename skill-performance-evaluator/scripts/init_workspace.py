#!/usr/bin/env python3
"""Create an evaluation workspace for a target skill and record reproducibility metadata.

Usage:
  python init_workspace.py <target-skill-dir> --out <workspace> [--model M] [--agent A]
         [--agent-version V] [--harness H] [--tools "bash,browser"] [--suite-version 1]

Creates <workspace>/{results/runs, evals/} and writes results/metadata.json and
results/environment.json. Values you do not pass are recorded as null, never guessed.
"""
import argparse, platform, shutil, sys
from pathlib import Path
from _common import hash_dir, load_json, now_iso, parse_frontmatter, write_json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model"); ap.add_argument("--agent"); ap.add_argument("--agent-version")
    ap.add_argument("--harness"); ap.add_argument("--tools", default=None)
    ap.add_argument("--suite-version", default="1")
    ap.add_argument("--runs-per-eval", type=int, default=None)
    ap.add_argument("--notes", default=None)
    a = ap.parse_args()

    target = Path(a.target).resolve()
    skill_md = target / "SKILL.md"
    if not skill_md.exists():
        sys.exit(f"error: {skill_md} not found")
    fm, err = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    fm = fm or {}
    digest, files = hash_dir(target)
    meta_block = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    ver = fm.get("version") or meta_block.get("version")
    version, source = (str(ver), "frontmatter") if ver else (f"sha256:{digest[:12]}", "content-hash (no version declared)")

    ws = Path(a.out)
    (ws / "results" / "runs").mkdir(parents=True, exist_ok=True)
    (ws / "evals").mkdir(parents=True, exist_ok=True)
    tgt_evals = target / "evals" / "evals.json"
    copied = None
    if tgt_evals.exists() and not (ws / "evals" / "evals.json").exists():
        shutil.copy(tgt_evals, ws / "evals" / "evals.json")
        copied = "evals/evals.json (snapshot copied from target skill)"

    write_json(ws / "results" / "metadata.json", {
        "schema_version": 1, "created_at": now_iso(),
        "skill_name": fm.get("name"), "skill_version": version, "version_source": source,
        "frontmatter_error": err, "frontmatter": fm, "target_path": str(target),
        "content_sha256": digest, "files": files,
        "suite_version": a.suite_version, "evals_source": copied,
    })
    write_json(ws / "results" / "environment.json", {
        "schema_version": 1, "evaluation_date": now_iso(),
        "model": a.model, "agent": a.agent, "agent_version": a.agent_version, "harness": a.harness,
        "os": platform.platform(), "machine": platform.machine(), "python": platform.python_version(),
        "available_tools": [t.strip() for t in a.tools.split(",")] if a.tools else None,
        "runs_per_eval_planned": a.runs_per_eval, "suite_version": a.suite_version, "notes": a.notes,
        "_note": "null means 'not recorded'. Fill in model/agent/harness before reporting; the evaluator must not guess them.",
    })
    print(f"workspace: {ws}\nskill: {fm.get('name')} {version} ({source})")
    missing = [k for k in ("model", "agent", "harness") if getattr(a, k) is None]
    if missing:
        print(f"warning: not recorded: {', '.join(missing)} (edit results/environment.json)")


if __name__ == "__main__":
    main()
