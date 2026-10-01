#!/usr/bin/env python3
"""Validate a .planning/ directory produced by the AI Project Architect skill.

Checks structure and logic (it cannot check factual claims - that is the planner's Audit 1):
  * required files / phase folders / SPEC headings / STATE sections
  * requirement IDs unique, priorities valid
  * every MUST requirement is covered by >=1 task; no task is an orphan or targets OUT_OF_SCOPE
  * task field completeness, dependency resolution, cycles, forward-phase dependencies
  * status consistency (READY/COMPLETE vs dependencies, phase COMPLETE vs tasks, decisions vs tasks)
  * parallel-group safety (no inter-dependency, no shared files)
  * unresolved {{placeholders}}

Usage:
  validate_plan.py [PLAN_DIR] [--report] [--emit-matrix] [--json] [--strict]
                   [--allow-missing RISKS,DECISIONS]
Exit code: 0 = no errors (and no warnings with --strict), 1 = errors, 2 = usage problem.
"""
import argparse, json, re, sys
from collections import defaultdict, deque
from pathlib import Path

STATUSES = {"NOT_STARTED", "READY", "IN_PROGRESS", "BLOCKED", "COMPLETE", "FAILED"}
PRIORITIES = {"MUST", "SHOULD", "COULD", "OUT_OF_SCOPE", "DROPPED"}
DEC_STATUSES = {"DECIDED", "ASSUMED", "REQUIRES USER DECISION", "SUPERSEDED"}
REQUIRED_FILES = ["PROJECT", "REQUIREMENTS", "ARCHITECTURE", "ROADMAP", "STATE", "DECISIONS", "RISKS", "EXECUTION"]
TASK_FIELDS = ["purpose", "files / components", "requirements", "dependencies", "implementation details",
               "expected output", "acceptance criteria", "validation command", "failure conditions",
               "verification", "status"]
SPEC_HEADINGS = ["objective", "why this phase exists", "entry criteria", "dependencies", "deliverables",
                 "acceptance criteria", "verification", "checkpoint", "exit criteria", "risks", "rollback"]
STATE_SECTIONS = ["current phase", "current task", "completed tasks", "blocked tasks", "recent changes",
                  "known issues", "active decisions", "pending decisions", "test status", "next action"]

RE_REQ = re.compile(r"\bREQ-[A-Z]+-\d{3}\b")
RE_TASK = re.compile(r"\bTASK-\d+\.\d+\b")
RE_TEST = re.compile(r"\bTEST-\d+\.\d+-[A-Za-z0-9]+\b")
RE_DEC = re.compile(r"\bDEC-\d+\b")
RE_FIELD = re.compile(r"^\s*[-*]\s+\*\*(.+?):\*\*\s*(.*)$")
RE_TASK_HEAD = re.compile(r"^###\s+(TASK-(\d+)\.(\d+))\s*(?:[—–-]+\s*(.*))?$", re.M)
RE_PHASE_DIR = re.compile(r"^phase-(\d{2,})-(.+)$")
RE_STATUS_LINE = re.compile(r"^\*\*Status:\*\*\s*([A-Za-z_ ]+?)\s*(?:<!--.*)?$", re.M)
PLACEHOLDER_CMDS = {"tbd", "todo", "n/a", "na", "none", "run tests", "run the tests", "test", "tests"}


class Plan:
    def __init__(self, root):
        self.root = root
        self.issues = []  # (level, where, message)
        self.reqs = {}    # id -> dict
        self.tasks = {}   # id -> dict
        self.phases = {}  # num -> dict
        self.decisions = {}

    def err(self, where, msg): self.issues.append(("ERROR", where, msg))
    def warn(self, where, msg): self.issues.append(("WARN", where, msg))


def read(path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)  # ignore HTML comments (format examples)


def section(text, heading):
    """Body of '## heading' up to the next heading of same or higher level."""
    m = re.search(rf"^(#+)\s*{re.escape(heading)}\b.*$", text, re.I | re.M)
    if not m:
        return None
    level = len(m.group(1))
    rest = text[m.end():]
    n = re.search(rf"^#{{1,{level}}}\s", rest, re.M)
    return rest[:n.start()] if n else rest


def headings(text):
    return [h.strip().lower() for h in re.findall(r"^#{1,4}\s+(.*)$", text, re.M)]


def has_heading(text, name):
    return any(h.startswith(name) or name in h for h in headings(text))


# ----------------------------------------------------------------------------- parsing

def parse_requirements(p):
    text = read(p.root / "REQUIREMENTS.md")
    if text is None:
        return
    cut = re.search(r"^#+\s*Traceability Matrix", text, re.I | re.M)
    if cut:
        text = text[:cut.start()]  # matrix rows repeat IDs; do not parse them as requirements
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or not re.fullmatch(r"REQ-[A-Z]+-\d{3}", cells[0]):
            continue
        rid = cells[0]
        prio = next((c for c in cells[1:] if c in PRIORITIES), None)
        if rid in p.reqs:
            p.err("REQUIREMENTS.md", f"duplicate requirement ID {rid}")
        if prio is None:
            p.err("REQUIREMENTS.md", f"{rid}: no valid Priority cell (one of {sorted(PRIORITIES)})")
            prio = "MUST"
        verif = cells[-1] if len(cells) >= 5 else ""
        p.reqs[rid] = {"id": rid, "text": cells[1] if len(cells) > 1 else "", "priority": prio, "verification": verif}
    if not p.reqs:
        p.err("REQUIREMENTS.md", "no requirement rows found (expected table rows starting with '| REQ-')")


def parse_decisions(p):
    text = read(p.root / "DECISIONS.md")
    if text is None:
        return
    for m in re.finditer(r"^##+\s+(DEC-\d+)\s*[—–-]?\s*(.*)$", text, re.M):
        body = text[m.end(): m.end() + 600]
        sm = RE_STATUS_LINE.search(body)
        status = sm.group(1).strip().upper() if sm else None
        if m.group(1) in p.decisions:
            p.err("DECISIONS.md", f"duplicate decision ID {m.group(1)}")
        if status not in DEC_STATUSES:
            p.err("DECISIONS.md", f"{m.group(1)}: missing/invalid **Status:** (use {sorted(DEC_STATUSES)})")
        p.decisions[m.group(1)] = status


def parse_tasks_file(p, path, phase_num, rel):
    text = read(path)
    if text is None:
        return
    heads = list(RE_TASK_HEAD.finditer(text))
    for i, h in enumerate(heads):
        body = text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        fields, cur = {}, None
        for line in body.splitlines():
            fm = RE_FIELD.match(line)
            if fm:
                cur = fm.group(1).strip().lower()
                fields[cur] = fm.group(2).strip()
            elif cur and line.strip() and not line.startswith("#"):
                fields[cur] += " " + line.strip()
        tid = h.group(1)
        t = {"id": tid, "title": (h.group(4) or "").strip(), "phase": int(h.group(2)), "fields": fields,
             "file": rel}
        if tid in p.tasks:
            p.err(rel, f"duplicate task ID {tid}")
        if t["phase"] != phase_num:
            p.err(rel, f"{tid} belongs to phase {t['phase']} but lives in phase {phase_num}")
        p.tasks[tid] = t


def parse_phases(p):
    pd = p.root / "phases"
    if not pd.is_dir():
        p.err("phases/", "missing phases/ directory")
        return
    for d in sorted(x for x in pd.iterdir() if x.is_dir()):
        m = RE_PHASE_DIR.match(d.name)
        if not m:
            p.warn(f"phases/{d.name}", "directory does not match 'phase-NN-name'; ignored")
            continue
        n = int(m.group(1))
        spec = d / "SPEC.md"
        rel = f"phases/{d.name}"
        info = {"num": n, "dir": d.name, "status": None}
        if not spec.exists():
            p.err(rel, "missing SPEC.md")
        else:
            st = read(spec) or ""
            for h in SPEC_HEADINGS:
                if not has_heading(st, h):
                    p.err(f"{rel}/SPEC.md", f"missing required section '{h}'")
            sm = RE_STATUS_LINE.search(st)
            info["status"] = sm.group(1).strip().upper() if sm else None
            if info["status"] not in STATUSES:
                p.err(f"{rel}/SPEC.md", f"missing/invalid **Status:** ({info['status']!r})")
            cp = section(st, "Checkpoint") or ""
            if len(cp.strip()) < 15:
                p.err(f"{rel}/SPEC.md", "Checkpoint section is empty - needs objective verification")
        tasks = d / "TASKS.md"
        if tasks.exists():
            parse_tasks_file(p, tasks, n, f"{rel}/TASKS.md")
        elif n > 0:
            p.err(rel, "missing TASKS.md")
        info["has_handoff"] = (d / "HANDOFF.md").exists()
        info["handoff_text"] = read(d / "HANDOFF.md") or ""
        p.phases[n] = info
    nums = sorted(p.phases)
    if nums and nums != list(range(nums[0], nums[0] + len(nums))):
        p.warn("phases/", f"phase numbers are not contiguous: {nums}")


# ----------------------------------------------------------------------------- checks

def check_files(p, allow):
    for name in REQUIRED_FILES:
        if name in allow:
            continue
        if not (p.root / f"{name}.md").exists():
            p.err(f"{name}.md", "required plan file is missing")
    st = read(p.root / "STATE.md")
    if st:
        for s in STATE_SECTIONS:
            if not has_heading(st, s):
                p.err("STATE.md", f"missing section '{s}'")
        na = section(st, "Next Action") or ""
        if "{{" not in na and not re.search(r"\b(TASK-\d+\.\d+|UDR-\d+|PHASE-\d+|DEC-\d+)\b", na):
            p.warn("STATE.md", "Next Action should name a task/phase/decision ID")
        done = section(st, "Completed Tasks") or ""
        for tid in set(RE_TASK.findall(done)):
            t = p.tasks.get(tid)
            if t is None:
                p.err("STATE.md", f"Completed Tasks lists unknown {tid}")
            elif t["fields"].get("status", "").upper() != "COMPLETE":
                p.warn("STATE.md", f"{tid} listed as completed but task status is {t['fields'].get('status')!r}")


def field(t, name):
    return t["fields"].get(name, "").strip()


def check_tasks(p):
    for tid, t in p.tasks.items():
        w = f"{t['file']}:{tid}"
        for f in TASK_FIELDS:
            v = field(t, f)
            if f not in t["fields"]:
                p.err(w, f"missing field '{f}'")
            elif not v:
                p.err(w, f"field '{f}' is empty")
        # requirements
        rids = set(RE_REQ.findall(field(t, "requirements")))
        t["reqs"] = rids
        if not rids:
            p.err(w, "task references no REQ-ID (orphan task: it has no reason to exist)")
        for r in rids:
            if r not in p.reqs:
                p.err(w, f"references unknown requirement {r}")
            elif p.reqs[r]["priority"] in ("OUT_OF_SCOPE", "DROPPED"):
                p.err(w, f"{r} is {p.reqs[r]['priority']} - scope creep")
        # dependencies
        dv = field(t, "dependencies")
        deps = set(RE_TASK.findall(dv))
        t["deps"] = deps
        if not deps and dv and dv.strip(" .`*").lower() not in ("none", "n/a", "-", "—") and "{{" not in dv:
            p.err(w, f"dependencies not parseable (use TASK-IDs or 'none'): {dv[:60]!r}")
        for d in deps:
            if d == tid:
                p.err(w, "depends on itself")
            elif d not in p.tasks:
                p.err(w, f"depends on unknown task {d}")
            elif p.tasks[d]["phase"] > t["phase"]:
                p.err(w, f"forward dependency on later-phase task {d}")
        # status
        status = field(t, "status").upper()
        t["status"] = status
        if status and status not in STATUSES and "{{" not in status:
            p.err(w, f"invalid status {status!r}")
        # validation command quality
        vc = field(t, "validation command").strip("` ").lower()
        if vc in PLACEHOLDER_CMDS:
            p.warn(w, "validation command is a placeholder - use the repo's real command or 'MANUAL:' steps")
        if "MANUAL" not in field(t, "validation command").upper() and len(vc) < 4 and "validation command" in t["fields"]:
            p.warn(w, "validation command looks too short to be runnable")
        if not RE_TEST.search(field(t, "verification")):
            p.warn(w, "verification has no TEST-<phase>.<task>-<letter> ID")
        # decisions
        for dec in RE_DEC.findall(field(t, "decisions") + " " + field(t, "implementation details")):
            ds = p.decisions.get(dec)
            if dec not in p.decisions:
                p.err(w, f"references unknown decision {dec}")
            elif ds == "REQUIRES USER DECISION" and status in ("READY", "IN_PROGRESS", "COMPLETE"):
                p.err(w, f"status {status} but {dec} still REQUIRES USER DECISION (should be BLOCKED)")
            elif ds == "ASSUMED":
                p.warn(w, f"relies on ASSUMED decision {dec} - executor must not treat it as confirmed")
    # dependency-status consistency (second pass, all tasks parsed)
    for tid, t in p.tasks.items():
        w = f"{t['file']}:{tid}"
        incomplete = [d for d in t["deps"] if d in p.tasks and p.tasks[d].get("status") != "COMPLETE"]
        if t.get("status") in ("READY", "IN_PROGRESS", "COMPLETE") and incomplete:
            p.err(w, f"status {t['status']} but dependencies not COMPLETE: {sorted(incomplete)}")


def check_cycles(p):
    indeg = {t: 0 for t in p.tasks}
    out = defaultdict(list)
    for tid, t in p.tasks.items():
        for d in t.get("deps", ()):
            if d in p.tasks and d != tid:
                out[d].append(tid)
                indeg[tid] += 1
    q = deque(k for k, v in indeg.items() if v == 0)
    seen = 0
    order = []
    while q:
        n = q.popleft()
        order.append(n)
        seen += 1
        for m in out[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    p.order = order
    if seen != len(p.tasks):
        stuck = sorted(k for k, v in indeg.items() if v > 0)
        p.err("dependency graph", f"circular dependency among: {', '.join(stuck[:12])}")


def check_coverage(p):
    cover = defaultdict(set)
    for tid, t in p.tasks.items():
        for r in t.get("reqs", ()):
            cover[r].add(tid)
    p.cover = cover
    for rid, r in p.reqs.items():
        if r["priority"] == "MUST":
            if not cover[rid]:
                p.err("coverage", f"MUST requirement {rid} has no implementing task")
            if r["verification"].strip(" -—").lower() in ("", "n/a", "none"):
                p.warn("REQUIREMENTS.md", f"{rid} (MUST) has no verification method")
        elif r["priority"] == "SHOULD" and not cover[rid]:
            p.warn("coverage", f"SHOULD requirement {rid} is not scheduled in any task (deferred?)")


def check_phases(p):
    by_phase = defaultdict(list)
    for t in p.tasks.values():
        by_phase[t["phase"]].append(t)
    for n, info in p.phases.items():
        w = f"phases/{info['dir']}"
        ts = by_phase.get(n, [])
        if n > 0 and not ts and (p.root / w / "TASKS.md").exists():
            p.err(w, "TASKS.md contains no parsable tasks")
        sts = {t.get("status") for t in ts}
        if info["status"] == "COMPLETE":
            bad = sorted(t["id"] for t in ts if t.get("status") != "COMPLETE")
            if bad:
                p.err(w, f"phase marked COMPLETE but tasks not COMPLETE: {bad[:8]}")
            if n > 0:
                m = re.search(r"PHASE STATUS:\s*(\S.*)", info["handoff_text"])
                if not m or "COMPLETE" not in m.group(1).upper():
                    p.err(w, "phase COMPLETE but HANDOFF.md has no 'PHASE STATUS: COMPLETE'")
        elif info["status"] == "NOT_STARTED" and sts & {"IN_PROGRESS", "COMPLETE"}:
            p.warn(w, "phase NOT_STARTED but it has IN_PROGRESS/COMPLETE tasks")
        # parallel groups
        groups = defaultdict(list)
        for t in ts:
            g = field(t, "parallel group").strip("` ")
            if g and g.lower() not in ("none", "-", "—", "n/a") and "{{" not in g:
                groups[g].append(t)
        for g, members in groups.items():
            ids = {m["id"] for m in members}
            for m in members:
                clash = ids & m.get("deps", set())
                if clash:
                    p.err(f"{w}:{m['id']}", f"parallel group {g} contains its own dependency {sorted(clash)}")
            files = defaultdict(list)
            for m in members:
                for f in re.findall(r"(?:CREATE|MODIFY)\s+`?([^\s`,;()]+)`?", field(m, "files / components")):
                    files[f].append(m["id"])
            for f, who in files.items():
                if len(who) > 1:
                    p.warn(w, f"parallel group {g}: {', '.join(who)} both touch {f}")
    # roadmap consistency
    rm = read(p.root / "ROADMAP.md")
    if rm:
        blocks = {}
        for m in re.finditer(r"^###\s+PHASE-(\d+)\b.*$", rm, re.M):
            sm = RE_STATUS_LINE.search(rm[m.end(): m.end() + 300])
            blocks[int(m.group(1))] = sm.group(1).strip().upper() if sm else None
        for n, info in p.phases.items():
            if n not in blocks:
                p.err("ROADMAP.md", f"PHASE-{n:02d} has a folder but no roadmap block")
            elif blocks[n] != info["status"]:
                p.warn("ROADMAP.md", f"PHASE-{n:02d} status {blocks[n]!r} differs from SPEC.md {info['status']!r}")
            if blocks.get(n) and blocks[n] not in STATUSES:
                p.err("ROADMAP.md", f"PHASE-{n:02d} invalid status {blocks[n]!r}")
        for n in blocks:
            if n not in p.phases:
                p.err("ROADMAP.md", f"PHASE-{n:02d} in roadmap but no phase folder")


def check_placeholders(p):
    for f in sorted(p.root.rglob("*.md")):
        if f.name == "HANDOFF.md":
            continue
        text = read(f) or ""
        n = len(re.findall(r"\{\{[^}]*\}\}", text))
        if n:
            p.warn(str(f.relative_to(p.root)), f"{n} unresolved {{{{placeholder}}}}(s)")


# ----------------------------------------------------------------------------- reports

def critical_path(p):
    depth, prev = {}, {}
    for tid in getattr(p, "order", []):
        best, bp = 0, None
        for d in p.tasks[tid].get("deps", ()):
            if d in depth and depth[d] > best:
                best, bp = depth[d], d
        depth[tid], prev[tid] = best + 1, bp
    if not depth:
        return []
    end = max(depth, key=depth.get)
    path = []
    while end:
        path.append(end)
        end = prev[end]
    return path[::-1]


def levels(p):
    lv = {}
    for tid in getattr(p, "order", []):
        deps = [d for d in p.tasks[tid].get("deps", ()) if d in lv and p.tasks[d]["phase"] == p.tasks[tid]["phase"]]
        lv[tid] = 1 + max((lv[d] for d in deps), default=-1)
    out = defaultdict(lambda: defaultdict(list))
    for tid, l in lv.items():
        out[p.tasks[tid]["phase"]][l].append(tid)
    return out


def matrix(p):
    rows = ["| Requirement | Priority | Tasks | Tests | Phase checkpoint(s) |", "|---|---|---|---|---|"]
    for rid, r in sorted(p.reqs.items()):
        ts = sorted(getattr(p, "cover", {}).get(rid, ()), key=lambda x: tuple(map(int, x[5:].split("."))))
        tests = sorted({x for t in ts for x in RE_TEST.findall(field(p.tasks[t], "verification"))})
        phs = sorted({p.tasks[t]["phase"] for t in ts})
        cell = lambda xs: ", ".join(xs) if xs else "—"
        rows.append(f"| {rid} | {r['priority']} | {cell(ts)} | {cell(tests)} | "
                    f"{cell([f'PHASE-{n:02d} CHECKPOINT' for n in phs])} |")
    return "\n".join(rows)


def stats(p):
    st = defaultdict(int)
    for t in p.tasks.values():
        st[t.get("status", "?")] += 1
    return {"requirements": len(p.reqs), "tasks": len(p.tasks), "phases": len(p.phases),
            "task_status": dict(st),
            "must_covered": sum(1 for r, v in p.reqs.items() if v["priority"] == "MUST" and p.cover.get(r)),
            "must_total": sum(1 for v in p.reqs.values() if v["priority"] == "MUST")}


# ----------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan_dir", nargs="?", default=".planning")
    ap.add_argument("--report", action="store_true", help="print critical path and parallel levels")
    ap.add_argument("--emit-matrix", action="store_true", help="print the traceability matrix only")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument("--allow-missing", default="", help="comma list of plan files that may be absent (small plans)")
    a = ap.parse_args()

    root = Path(a.plan_dir)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    allow = {x.strip().upper() for x in a.allow_missing.split(",") if x.strip()}

    p = Plan(root)
    parse_requirements(p)
    parse_decisions(p)
    parse_phases(p)
    check_files(p, allow)
    check_tasks(p)
    check_cycles(p)
    check_coverage(p)
    check_phases(p)
    check_placeholders(p)
    # STATE check needs tasks parsed; re-run its task-dependent part is already inside check_files order,
    # so make sure tasks existed: parse_phases ran before check_files.

    if a.emit_matrix:
        print(matrix(p))
        return 0

    errors = [i for i in p.issues if i[0] == "ERROR"]
    warns = [i for i in p.issues if i[0] == "WARN"]
    s = stats(p)

    if a.json:
        out = {"errors": [{"where": w, "message": m} for _, w, m in errors],
               "warnings": [{"where": w, "message": m} for _, w, m in warns], "stats": s}
        if a.report:
            out["critical_path"] = critical_path(p)
            out["levels"] = {str(k): {str(l): v for l, v in d.items()} for k, d in levels(p).items()}
        print(json.dumps(out, indent=2))
    else:
        for lvl, w, m in p.issues:
            print(f"[{lvl}] {w}: {m}")
        print(f"\n{s['phases']} phases, {s['tasks']} tasks, {s['requirements']} requirements "
              f"(MUST covered {s['must_covered']}/{s['must_total']}); task status: {s['task_status']}")
        print(f"RESULT: {len(errors)} error(s), {len(warns)} warning(s)")
        if a.report:
            cp = critical_path(p)
            print(f"\nCritical path ({len(cp)} tasks): " + " -> ".join(cp))
            for n, d in sorted(levels(p).items()):
                print(f"\nPHASE-{n:02d} parallel levels:")
                for l in sorted(d):
                    print(f"  wave {l + 1}: {', '.join(sorted(d[l]))}")
    return 1 if errors or (a.strict and warns) else 0


if __name__ == "__main__":
    sys.exit(main())
