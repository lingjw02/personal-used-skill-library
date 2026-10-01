#!/usr/bin/env python3
"""Scaffold a .planning/ directory from the skill templates.

Usage:
  python init_plan.py --root <project-root> --project "Name" \
      --phases "discovery,foundation,core,features,hardening,release" [--force]

Creates .planning/{PROJECT,REQUIREMENTS,ARCHITECTURE,ROADMAP,STATE,DECISIONS,RISKS,EXECUTION}.md
and phases/phase-NN-<slug>/{SPEC.md[,TASKS.md,HANDOFF.md]}. Phase 00 gets SPEC.md only.
Existing files are never overwritten unless --force. Remaining {{placeholders}} are for the
planner to fill in; validate_plan.py warns about any that are left.
"""
import argparse, datetime, re, sys
from pathlib import Path

TOP = ["PROJECT", "REQUIREMENTS", "ARCHITECTURE", "ROADMAP", "STATE", "DECISIONS", "RISKS", "EXECUTION"]
TPL = Path(__file__).resolve().parent.parent / "assets" / "templates"


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "phase"


def title(slug):
    return slug.replace("-", " ").title()


def write(path, text, force):
    if path.exists() and not force:
        print(f"skip (exists): {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote: {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--project", required=True)
    ap.add_argument("--phases", required=True, help="comma-separated phase names; first is phase 00")
    ap.add_argument("--plan-dir", default=".planning")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    names = [slugify(x) for x in a.phases.split(",") if x.strip()]
    if not names:
        sys.exit("no phases given")
    plan = Path(a.root) / a.plan_dir
    base = {"PROJECT_NAME": a.project, "DATE": datetime.date.today().isoformat()}

    def sub(text, extra=None):
        m = {**base, **(extra or {})}
        return re.sub(r"\{\{([A-Z_]+)\}\}", lambda g: m.get(g.group(1), g.group(0)), text)

    tree = ["PROJECT"] + [
        f"{'└──' if i == len(names) - 1 else '├──'} PHASE-{i:02d} — {title(n)}" for i, n in enumerate(names)
    ]
    blocks = []
    for i, n in enumerate(names):
        prev = f"PHASE-{i-1:02d}" if i else "none"
        blocks.append(
            f"### PHASE-{i:02d} — {title(n)}\n**Status:** {'READY' if i == 0 else 'NOT_STARTED'}\n"
            f"- Dependencies: {prev}\n- Deliverables: {{{{deliverables}}}}\n"
            f"- Critical tasks: {{{{critical tasks}}}}\n- Checkpoint: {{{{one line}}}}\n"
        )
    extra_roadmap = {"PHASE_TREE": "\n".join(tree), "PHASE_BLOCKS": "\n".join(blocks)}

    for name in TOP:
        text = (TPL / f"{name}.md").read_text(encoding="utf-8")
        write(plan / f"{name}.md", sub(text, extra_roadmap if name == "ROADMAP" else None), a.force)

    for i, n in enumerate(names):
        d = plan / "phases" / f"phase-{i:02d}-{n}"
        ex = {"PHASE_NUM": str(i), "PHASE_NUM_PADDED": f"{i:02d}", "PHASE_NAME": title(n), "PHASE_SLUG": n,
              "PHASE_STATUS": "READY" if i == 0 else "NOT_STARTED"}
        files = ["SPEC"] + ([] if i == 0 else ["TASKS", "HANDOFF"])
        for f in files:
            t = (TPL / f"phase-{f}.md").read_text(encoding="utf-8")
            write(d / f"{f}.md", sub(t, ex), a.force)
    print(f"\nScaffolded {len(names)} phases in {plan}. Now fill in the plan, then run validate_plan.py.")


if __name__ == "__main__":
    main()
