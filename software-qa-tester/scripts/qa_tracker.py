#!/usr/bin/env python3
"""QA run tracker: feature inventory, bugs, evidence rules, coverage, report, secret scan.

State lives in <dir>/qa_state.json (default dir: qa-run, or $QA_RUN_DIR); every change is appended to
<dir>/qa_log.jsonl. The tool exists to make dishonest reporting hard:
  * PASSED needs evidence (a file, or 'obs:<text>' for terminal observations)
  * FAILED needs a recorded bug; a feature with an open bug cannot be PASSED
  * a Confirmed bug needs file evidence, steps, expected/actual, >=2 reproductions, and fix guidance
  * 'fixed' is only a claim until `retest` passes with evidence
  * destructive features in production/unknown environments need explicit confirmation to start
  * reports are redacted for secrets

Commands: init add-feature set list next add-bug update-bug mark-fixed retest note
          regression status report scan
Run `qa_tracker.py <command> --help` for options.
"""
import argparse, csv, datetime, json, os, re, sys
from pathlib import Path

FEATURE_STATES = ["DISCOVERED", "TESTING", "PASSED", "FAILED", "BLOCKED", "UNCONFIRMED", "SKIPPED"]
EXECUTED = {"PASSED", "FAILED", "UNCONFIRMED"}
PRIORITIES = ["Critical", "High", "Medium", "Low"]
RISK = ["auth-security", "data-loss", "core-business", "crud", "payments", "navigation", "forms",
        "search-filter", "error-handling", "secondary", "cosmetic"]
SEVERITIES = ["Critical", "High", "Medium", "Low", "Informational"]
CONFIDENCE = ["Confirmed", "Probable", "Unconfirmed"]
BUG_STATUS = ["OPEN", "FIXED_PENDING_RETEST", "VERIFIED_FIXED", "REOPENED", "INVALID", "WONTFIX"]
OPEN_STATUS = {"OPEN", "REOPENED", "FIXED_PENDING_RETEST"}
CATEGORIES = ["data-loss", "blocking", "core-workflow", "integration", "error-handling", "secondary", "cosmetic"]
KINDS = ["functional", "ui", "ux", "performance", "configuration", "environment", "security", "data",
         "accessibility"]
ENVS = ["production", "staging", "test", "local", "unknown"]
NOTE_TYPES = ["feature-request", "expected-behavior", "observation", "ux-suggestion"]

SECRET_PATTERNS = [
    ("authorization header", re.compile(r"(?i)(authorization\s*[:=]\s*(?:bearer|basic)\s+)[A-Za-z0-9._~+/=-]{6,}")),
    ("credential assignment", re.compile(r"(?i)\b((?:password|passwd|pwd|secret|token|api[_-]?key|apikey|access[_-]?key)"
                                          r"[\"']?\s*[:=]\s*[\"']?)[^\s\"',;&]{3,}")),
    ("JWT", re.compile(r"()\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
    ("AWS key id", re.compile(r"()\bAKIA[0-9A-Z]{16}\b")),
    ("API key (sk-/ghp_/xox)", re.compile(r"()\b(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9-]{10,})")),
    ("password in URL", re.compile(r"(://[^/\s:@]+:)[^/\s@]{3,}(?=@)")),
    ("private key", re.compile(r"()-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]


# ------------------------------------------------------------------ helpers
def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def redact(text):
    n = 0
    for _, rx in SECRET_PATTERNS:
        text, k = rx.subn(lambda m: m.group(1) + "[REDACTED]", text)
        n += k
    return text, n


def run_dir(a):
    return Path(a.dir or os.environ.get("QA_RUN_DIR") or "qa-run")


def load(d):
    p = d / "qa_state.json"
    if not p.exists():
        die(f"no QA run in {d}. Run: qa_tracker.py --dir {d} init --app NAME --env ENV")
    return json.loads(p.read_text(encoding="utf-8"))


def save(d, st):
    tmp = d / "qa_state.json.tmp"
    tmp.write_text(json.dumps(st, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(d / "qa_state.json")


def log(d, action, **kw):
    line = json.dumps({"ts": now(), "action": action, **kw}, ensure_ascii=False)
    line, _ = redact(line)
    with (d / "qa_log.jsonl").open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def pick(value, options, what):
    for o in options:
        if o.lower() == str(value).lower():
            return o
    die(f"invalid {what} {value!r}; choose from {options}")


def evidence(d, items, require_file=False):
    out = []
    for e in items or []:
        if e.startswith("obs:"):
            txt = e[4:].strip()
            if not txt:
                die("empty 'obs:' evidence")
            out.append({"type": "obs", "value": txt})
            continue
        p = Path(e)
        if not p.exists() and (d / e).exists():
            p = d / e
        if not p.exists():
            die(f"evidence file not found: {e}")
        try:
            rel = p.resolve().relative_to(d.resolve())
        except ValueError:
            rel = p
        out.append({"type": "file", "value": str(rel)})
    if require_file and not any(x["type"] == "file" for x in out):
        die("this action needs at least one evidence FILE (screenshot/log/output saved under the run dir)")
    return out


def split_ids(s):
    return [x.strip() for x in re.split(r"[,;\s]+", s or "") if x.strip()]


def cell(s):
    s = redact("" if s is None else str(s))[0]
    return s.replace("|", "\\|").replace("\n", "<br>")


def risk_rank(f):
    return RISK.index(f["risk"]) if f["risk"] in RISK else len(RISK)


def pri_rank(f):
    return PRIORITIES.index(f["priority"]) if f["priority"] in PRIORITIES else len(PRIORITIES)


def sev_rank(b):
    return SEVERITIES.index(b["severity"])


# ------------------------------------------------------------------ commands
def cmd_init(a):
    d = run_dir(a)
    if (d / "qa_state.json").exists() and not a.force:
        die(f"{d}/qa_state.json already exists (use --force to overwrite)")
    (d / "evidence").mkdir(parents=True, exist_ok=True)
    st = {"app": a.app, "env": pick(a.env, ENVS, "env"), "tier": a.tier, "created": now(),
          "notes_for_report": a.notes or "", "features": {}, "bugs": {}, "notes": [], "next_bug": 1,
          "next_note": 1}
    save(d, st)
    log(d, "init", app=a.app, env=st["env"], tier=a.tier)
    print(f"Initialized QA run in {d} (env={st['env']}, tier={a.tier}).")
    if st["env"] in ("production", "unknown"):
        print("NOTE: production/unknown environment - destructive features require --confirm-destructive to start.")


def add_feature_record(st, rec):
    fid = rec["id"]
    if fid in st["features"]:
        die(f"feature {fid} already exists")
    st["features"][fid] = {
        "id": fid, "module": rec.get("module", ""), "page": rec.get("page", ""), "function": rec.get("function", ""),
        "priority": pick(rec.get("priority") or "Medium", PRIORITIES, "priority"),
        "risk": pick(rec.get("risk") or "secondary", RISK, "risk"),
        "destructive": str(rec.get("destructive", "")).lower() in ("1", "true", "yes", "y"),
        "related": split_ids(rec.get("related", "")), "state": "DISCOVERED", "note": "", "evidence": [],
        "bugs": [], "confirmed_destructive": ""}


def cmd_add_feature(a):
    d = run_dir(a); st = load(d)
    recs = []
    if a.csv:
        with open(a.csv, newline="", encoding="utf-8") as f:
            recs = list(csv.DictReader(f))
        if not recs:
            die("empty CSV")
    else:
        if not (a.id and a.function):
            die("need --id and --function (or --csv)")
        recs = [{"id": a.id, "module": a.module, "page": a.page, "function": a.function, "priority": a.priority,
                 "risk": a.risk, "destructive": a.destructive, "related": a.related}]
    for r in recs:
        if not r.get("id"):
            die("every feature needs an id")
        add_feature_record(st, r)
        log(d, "add-feature", id=r["id"], function=r.get("function"))
    save(d, st)
    print(f"Added {len(recs)} feature(s). Total: {len(st['features'])}")


def cmd_set(a):
    d = run_dir(a); st = load(d)
    f = st["features"].get(a.id) or die(f"unknown feature {a.id}")
    new = pick(a.state, FEATURE_STATES, "state")
    ev = evidence(d, a.evidence)
    if new == "TESTING" and f["destructive"] and st["env"] in ("production", "unknown"):
        if not a.confirm_destructive:
            die(f"{a.id} is destructive and env is {st['env']}. Get explicit user confirmation, then pass "
                f"--confirm-destructive '<who/when>'")
        f["confirmed_destructive"] = a.confirm_destructive
    if new == "PASSED":
        if not a.note:
            die("PASSED requires --note describing what you observed")
        if not ev:
            die("PASSED requires --evidence (file path, or 'obs:<observation>')")
        openb = [b for b in f["bugs"] if st["bugs"][b]["status"] in OPEN_STATUS and st["bugs"][b]["severity"] != "Informational"]
        if openb:
            die(f"{a.id} has open bug(s) {openb}; it cannot be PASSED (mark FAILED, or retest/close the bugs first)")
    if new == "FAILED":
        bugs = split_ids(a.bug)
        if not bugs:
            die("FAILED requires --bug BUG-xxx (record the bug first with add-bug)")
        for b in bugs:
            if b not in st["bugs"]:
                die(f"unknown bug {b}")
            if b not in f["bugs"]:
                f["bugs"].append(b)
            if a.id not in st["bugs"][b]["features"]:
                st["bugs"][b]["features"].append(a.id)
    if new in ("BLOCKED", "SKIPPED", "UNCONFIRMED") and not a.note:
        die(f"{new} requires --note with the reason")
    if a.bug and new not in ("FAILED",):
        for b in split_ids(a.bug):
            if b in st["bugs"] and b not in f["bugs"]:
                f["bugs"].append(b)
    old = f["state"]
    f["state"] = new
    if a.note:
        f["note"] = a.note
    f["evidence"] += ev
    save(d, st)
    log(d, "set", id=a.id, old=old, new=new, note=a.note, evidence=[e["value"] for e in ev])
    print(f"{a.id}: {old} -> {new}")


def cmd_list(a):
    st = load(run_dir(a))
    rows = [f for f in st["features"].values()
            if (not a.state or f["state"] == a.state.upper()) and (not a.priority or f["priority"].lower() == a.priority.lower())]
    rows.sort(key=lambda f: f["id"])
    for f in rows:
        flag = " [destructive]" if f["destructive"] else ""
        print(f"{f['id']:8} {f['state']:12} {f['priority']:8} {f['risk']:14} {f['module']} / {f['page']} / {f['function']}{flag}")
    print(f"({len(rows)} features)")


def cmd_next(a):
    st = load(run_dir(a))
    todo = [f for f in st["features"].values() if f["state"] in ("DISCOVERED", "TESTING")]
    todo.sort(key=lambda f: (f["state"] != "TESTING", risk_rank(f), pri_rank(f), f["id"]))
    if not todo:
        print("Nothing left to test (no DISCOVERED/TESTING features).")
        return
    for f in todo[: a.n]:
        flag = "  ** destructive: check environment/permission first **" if f["destructive"] else ""
        print(f"{f['id']:8} [{f['state']}] {f['priority']}/{f['risk']}: {f['module']} / {f['page']} / {f['function']}{flag}")


def parse_repro(s):
    m = re.fullmatch(r"\s*(\d+)\s*/\s*(\d+)\s*", s or "")
    if not m:
        die("--repro must look like '3/3' (reproduced/attempted)")
    n, t = int(m.group(1)), int(m.group(2))
    if t == 0 or n > t:
        die("--repro must satisfy 0 <= reproduced <= attempted, attempted >= 1")
    return n, t


def validate_bug(st, d, b):
    for fid in b["features"]:
        if fid not in st["features"]:
            die(f"unknown feature {fid} in --features")
    if b["suspected_area"] and not b["suspected_basis"]:
        die("--suspected-area needs --suspected-basis (the evidence for the hypothesis); omit both if you have none")
    if b["confidence"] == "Confirmed":
        miss = []
        if not [x for x in b["evidence"] if x["type"] == "file"]:
            miss.append("evidence file")
        if not b["steps"]:
            miss.append("steps")
        for k in ("expected", "actual", "recommendation", "risk", "verification"):
            if not b[k]:
                miss.append(k)
        n, _ = parse_repro(b["repro"])
        if n < 2:
            miss.append("reproduction >= 2 times (else use Probable)")
        if miss:
            die("a Confirmed bug requires: " + ", ".join(miss))


def bug_args_to_dict(a):
    return {"title": a.title, "features": split_ids(a.features), "severity": pick(a.severity, SEVERITIES, "severity") if a.severity else None,
            "confidence": pick(a.confidence, CONFIDENCE, "confidence") if a.confidence else None,
            "kind": pick(a.kind, KINDS, "kind") if a.kind else None,
            "category": pick(a.category, CATEGORIES, "category") if a.category else None,
            "preconditions": a.precondition, "steps": a.step, "expected": a.expected, "actual": a.actual,
            "repro": a.repro, "suspected_area": a.suspected_area, "suspected_basis": a.suspected_basis,
            "recommendation": a.recommendation, "impl_area": a.impl_area, "risk": a.risk,
            "verification": a.verification, "context": a.context}


def cmd_add_bug(a):
    d = run_dir(a); st = load(d)
    for req in ("title", "features", "severity", "confidence", "kind", "category", "expected", "actual"):
        if not getattr(a, req):
            die(f"--{req} is required")
    raw = bug_args_to_dict(a)
    b = {**raw, "id": f"BUG-{st['next_bug']:03d}", "status": "OPEN", "created": now(),
         "evidence": evidence(d, a.evidence), "repro": a.repro or "1/1",
         "impl_area": a.impl_area or "Not identified", "history": []}
    parse_repro(b["repro"])
    validate_bug(st, d, b)
    st["next_bug"] += 1
    st["bugs"][b["id"]] = b
    for fid in b["features"]:
        st["features"][fid]["bugs"].append(b["id"])
    save(d, st)
    log(d, "add-bug", id=b["id"], title=b["title"], severity=b["severity"], confidence=b["confidence"])
    print(f"{b['id']} recorded ({b['severity']}/{b['confidence']}). Next: set the feature FAILED with --bug {b['id']}.")


def cmd_update_bug(a):
    d = run_dir(a); st = load(d)
    b = st["bugs"].get(a.id) or die(f"unknown bug {a.id}")
    upd = {k: v for k, v in bug_args_to_dict(a).items() if v not in (None, [], "")}
    if "features" in upd:
        for fid in upd["features"]:
            if fid not in st["features"]:
                die(f"unknown feature {fid}")
            if a.id not in st["features"][fid]["bugs"]:
                st["features"][fid]["bugs"].append(a.id)
    cand = {**b, **upd}
    if a.evidence:
        cand["evidence"] = b["evidence"] + evidence(d, a.evidence)
    if a.repro:
        parse_repro(a.repro)
    validate_bug(st, d, cand)
    b.update(cand)
    save(d, st)
    log(d, "update-bug", id=a.id, fields=sorted(upd) + (["evidence"] if a.evidence else []))
    print(f"{a.id} updated.")


def cmd_mark_fixed(a):
    d = run_dir(a); st = load(d)
    b = st["bugs"].get(a.id) or die(f"unknown bug {a.id}")
    if b["status"] not in ("OPEN", "REOPENED"):
        die(f"{a.id} is {b['status']}; only OPEN/REOPENED bugs can be marked fixed")
    b["status"] = "FIXED_PENDING_RETEST"
    b["history"].append({"ts": now(), "event": "claimed fixed (UNVERIFIED)", "note": a.note or ""})
    save(d, st)
    log(d, "mark-fixed", id=a.id, note=a.note)
    print(f"{a.id}: FIXED_PENDING_RETEST. This is a developer claim, not a result. Run: regression {a.id}, then retest.")


def cmd_retest(a):
    d = run_dir(a); st = load(d)
    b = st["bugs"].get(a.id) or die(f"unknown bug {a.id}")
    if b["status"] in ("INVALID", "WONTFIX", "VERIFIED_FIXED"):
        die(f"{a.id} is {b['status']}; nothing to retest")
    ev = evidence(d, a.evidence)
    if not ev:
        die("retest requires --evidence of the re-run (file, or 'obs:<observation>')")
    if not a.note:
        die("retest requires --note (what exactly was re-run and observed)")
    res = a.result.lower()
    if res not in ("pass", "fail"):
        die("--result must be pass or fail")
    b["status"] = "VERIFIED_FIXED" if res == "pass" else "REOPENED"
    b["history"].append({"ts": now(), "event": f"retest {res.upper()}", "note": a.note,
                         "evidence": [e["value"] for e in ev]})
    save(d, st)
    log(d, "retest", id=a.id, result=res, note=a.note)
    print(f"{a.id}: {b['status']}")
    if res == "pass":
        print(f"Reminder: run `regression {a.id}`, re-test the listed items, and re-set the linked features' states.")
    else:
        print("Linked features should be FAILED again: re-set them with --bug.")


def cmd_note(a):
    d = run_dir(a); st = load(d)
    n = {"id": f"NOTE-{st['next_note']:03d}", "type": pick(a.type, NOTE_TYPES, "type"), "text": a.text,
         "feature": a.feature or "", "ts": now()}
    st["next_note"] += 1
    st["notes"].append(n)
    save(d, st)
    log(d, "note", id=n["id"], type=n["type"])
    print(f"{n['id']} recorded (not a defect).")


def cmd_regression(a):
    d = run_dir(a); st = load(d)
    b = st["bugs"].get(a.id) or die(f"unknown bug {a.id}")
    feats = [st["features"][x] for x in b["features"] if x in st["features"]]
    mods = {(f["module"]) for f in feats}
    pages = {(f["module"], f["page"]) for f in feats}
    lines = [f"# Regression checklist for {a.id} - {b['title']}", "",
             "1. Original failing case", f"   - [ ] Re-run exactly: {len(b['steps'])} recorded step(s); compare Expected vs Actual"]
    for i, s in enumerate(b["steps"], 1):
        lines.append(f"     {i}. {s}")
    lines += ["", "2. Directly affected features"] + [f"   - [ ] {f['id']} {f['function']}" for f in feats]
    seen = {f["id"] for f in feats}
    related = sorted({r for f in feats for r in f["related"]} - seen)
    nb = [f for f in st["features"].values() if f["id"] not in seen and (f["module"], f["page"]) in pages]
    lines += ["", "3. Neighboring pages/features (same page)"] + [f"   - [ ] {f['id']} {f['function']}" for f in nb]
    seen |= {f["id"] for f in nb}
    rel = [st["features"][r] for r in related if r in st["features"] and r not in seen]
    lines += ["", "4. Dependent workflows (declared related)"] + [f"   - [ ] {f['id']} {f['function']}" for f in rel]
    seen |= {f["id"] for f in rel}
    crit = [f for f in st["features"].values() if f["priority"] == "Critical" and f["id"] not in seen and f["state"] == "PASSED"]
    lines += ["", "5. Previously-passing Critical functionality"] + [f"   - [ ] {f['id']} {f['function']}" for f in crit]
    out = "\n".join(lines)
    print(out)
    if a.save:
        p = d / f"regression-{a.id}.md"
        p.write_text(out + "\n", encoding="utf-8")
        print(f"\nSaved {p}")


def counts(st):
    c = {s: 0 for s in FEATURE_STATES}
    for f in st["features"].values():
        c[f["state"]] += 1
    tot = len(st["features"])
    ex = sum(c[s] for s in EXECUTED)
    return c, tot, ex


def cmd_status(a):
    d = run_dir(a); st = load(d)
    c, tot, ex = counts(st)
    print(f"App: {st['app']}   env: {st['env']}   tier: {st['tier']}")
    print(f"Features: {tot}   executed: {ex} ({(100 * ex // tot) if tot else 0}%)")
    print("  " + "  ".join(f"{k}={v}" for k, v in c.items()))
    gaps = [f for f in st["features"].values() if f["state"] in ("DISCOVERED", "TESTING") and f["priority"] in ("Critical", "High")]
    if gaps:
        print("Untested Critical/High features: " + ", ".join(f["id"] for f in sorted(gaps, key=lambda f: f["id"])))
    ob = [b for b in st["bugs"].values() if b["status"] in OPEN_STATUS]
    bysev = {s: sum(1 for b in ob if b["severity"] == s) for s in SEVERITIES}
    print(f"Open bugs: {len(ob)}  " + "  ".join(f"{k}={v}" for k, v in bysev.items() if v))
    pending = [b["id"] for b in st["bugs"].values() if b["status"] == "FIXED_PENDING_RETEST"]
    if pending:
        print("Fix claimed but NOT verified: " + ", ".join(pending))
    for f in st["features"].values():
        for r in f["related"]:
            if r not in st["features"]:
                print(f"WARN: {f['id']} lists unknown related feature {r}")
        if f["state"] == "PASSED" and not f["evidence"]:
            print(f"WARN: {f['id']} PASSED without evidence")
        if f["state"] == "FAILED" and not [b for b in f["bugs"] if st["bugs"][b]["status"] in OPEN_STATUS | {"VERIFIED_FIXED"}]:
            print(f"WARN: {f['id']} FAILED but no live bug link")


def feat_issues(st, f):
    return ", ".join(f["bugs"]) if f["bugs"] else "-"


def cmd_report(a):
    d = run_dir(a); st = load(d)
    c, tot, ex = counts(st)
    bugs = sorted(st["bugs"].values(), key=lambda b: (sev_rank(b), b["id"]))
    out = [f"# QA Report - {st['app']}", "",
           f"- **Environment:** {st['env']}   **Capability tier:** {st['tier']}   **Run started:** {st['created']}   **Report generated:** {now()}"]
    if st.get("notes_for_report"):
        out.append(f"- **Context:** {st['notes_for_report']}")
    out += ["", "## Executive Summary", ""]
    sp = d / "summary.md"
    if sp.exists():
        out += [sp.read_text(encoding="utf-8").strip(), ""]
    else:
        out += ["_Narrative not written. Create `summary.md` in the run directory and regenerate._", ""]
        print("WARN: no summary.md - executive-summary narrative missing", file=sys.stderr)
    out += [f"**Coverage (from tracker):** {ex}/{tot} features executed ({(100 * ex // tot) if tot else 0}%). "
            + ", ".join(f"{k} {v}" for k, v in c.items() if v) + ".", ""]
    ob = [b for b in bugs if b["status"] in OPEN_STATUS]
    out.append("**Open defects:** " + (", ".join(f"{sum(1 for b in ob if b['severity'] == s)} {s}" for s in SEVERITIES
                                                  if any(b['severity'] == s for b in ob)) or "none") + ".")
    crit = [b for b in ob if b["severity"] == "Critical"]
    out.append("**Critical blockers:** " + (", ".join(f"{b['id']} ({b['title']})" for b in crit) or "none recorded") + ".")
    unt = [f for f in st["features"].values() if f["state"] in ("DISCOVERED", "TESTING", "BLOCKED", "SKIPPED")]
    out.append(f"**Untested/blocked areas:** {len(unt)} feature(s) - see Coverage Gaps.")
    pend = [b["id"] for b in st["bugs"].values() if b["status"] == "FIXED_PENDING_RETEST"]
    if pend:
        out.append("**Fix claimed, not verified:** " + ", ".join(pend) + ".")
    out += ["", "## Feature Coverage", "", "| Feature | Tested | Result | Issues |", "|---|---:|---|---|"]
    for f in sorted(st["features"].values(), key=lambda f: f["id"]):
        tested = "Yes" if f["state"] in EXECUTED else "No"
        out.append(f"| {cell(f['id'] + ' ' + f['module'] + ' / ' + f['page'] + ' / ' + f['function'])} | {tested} | {f['state']} | {cell(feat_issues(st, f))} |")
    out += ["", "## Bug Report", ""]
    if bugs:
        out += ["| ID | Severity | Feature | Status | Reproduction |", "|---|---|---|---|---|"]
        for b in bugs:
            out.append(f"| {b['id']} | {b['severity']} | {cell(', '.join(b['features']))} | {b['status']} | {b['repro']} ({b['confidence']}) |")
    else:
        out.append("_No bugs recorded._")
    out += ["", "## Detailed Findings", ""]
    for b in bugs:
        out += [f"### {b['id']} - {cell(b['title'])}", "",
                f"- **Severity:** {b['severity']}   **Confidence:** {b['confidence']}   **Kind:** {b['kind']}   **Status:** {b['status']}",
                f"- **Affected features:** {', '.join(b['features'])}",
                f"- **Problem:** {redact(b['title'])[0]}"]
        if b["preconditions"]:
            out.append("- **Preconditions:** " + "; ".join(redact(x)[0] for x in b["preconditions"]))
        out.append("- **Steps:**")
        out += [f"  {i}. {redact(s)[0]}" for i, s in enumerate(b["steps"], 1)] or ["  _none recorded_"]
        out += [f"- **Expected:** {redact(b['expected'])[0]}", f"- **Actual:** {redact(b['actual'])[0]}",
                f"- **Reproduction rate:** {b['repro']}"]
        if b["context"]:
            out.append(f"- **Observed context (console/network/log):** {redact(b['context'])[0]}")
        out.append("- **Evidence:** " + ("; ".join(f"`{e['value']}`" if e["type"] == "file" else f"(observation) {redact(e['value'])[0]}" for e in b["evidence"]) or "none"))
        if b["suspected_area"]:
            out.append(f"- **Suspected area (HYPOTHESIS, not fact):** {redact(b['suspected_area'])[0]} - basis: {redact(b['suspected_basis'])[0]}")
        if b["recommendation"]:
            out += [f"- **Recommended modification:** {redact(b['recommendation'])[0]}",
                    f"- **Implementation area:** {redact(b['impl_area'])[0]}",
                    f"- **Risk of the change:** {redact(b['risk'])[0]}",
                    f"- **Verification test:** {redact(b['verification'])[0]}"]
        else:
            out.append("- **Recommended modification:** _not provided (finding is not Confirmed)_")
        for h in b["history"]:
            out.append(f"- _History {h['ts']}:_ {redact(h['event'])[0]} {redact(h.get('note', ''))[0]}")
        out.append("")
    if not bugs:
        out.append("_None._\n")
    out += ["## Observations (not defects)", ""]
    if st["notes"]:
        out += [f"- **{n['id']}** ({n['type']}{', ' + n['feature'] if n['feature'] else ''}): {redact(n['text'])[0]}" for n in st["notes"]]
    else:
        out.append("_None._")
    out += ["", "## Coverage Gaps", ""]
    gap = [f for f in st["features"].values() if f["state"] in ("DISCOVERED", "TESTING", "BLOCKED", "SKIPPED", "UNCONFIRMED")]
    if gap:
        out += ["| Feature | State | Reason / note |", "|---|---|---|"]
        for f in sorted(gap, key=lambda f: f["id"]):
            reason = f["note"] or ("not yet tested" if f["state"] in ("DISCOVERED", "TESTING") else "")
            out.append(f"| {cell(f['id'] + ' ' + f['function'])} | {f['state']} | {cell(reason)} |")
    else:
        out.append("_No gaps: every discovered feature has a PASSED/FAILED result._")
    out += ["", "## Recommended Development Order", "",
            "_Engineering work ordered by risk (not a ranking of the product)._", ""]
    cand = [b for b in bugs if b["status"] in OPEN_STATUS and b["confidence"] != "Unconfirmed"]
    cand.sort(key=lambda b: (CATEGORIES.index(b["category"]), sev_rank(b), b["id"]))
    for i, b in enumerate(cand, 1):
        out.append(f"{i}. **[{b['category']}]** {b['id']} ({b['severity']}) - {cell(b['title'])}")
    if not cand:
        out.append("_No open Confirmed/Probable defects._")
    unc = [b for b in bugs if b["status"] in OPEN_STATUS and b["confidence"] == "Unconfirmed"]
    if unc:
        out += ["", "Needs further investigation (Unconfirmed): " + ", ".join(b["id"] for b in unc)]
    text, n = redact("\n".join(out) + "\n")
    p = Path(a.out) if a.out else d / "report.md"
    p.write_text(text, encoding="utf-8")
    print(f"Report written to {p}" + (f" ({n} secret-like value(s) redacted)" if n else ""))


def cmd_scan(a):
    d = run_dir(a)
    targets = [Path(x) for x in a.paths] or [d]
    hits = 0
    for t in targets:
        files = [t] if t.is_file() else sorted(p for p in t.rglob("*") if p.is_file())
        for p in files:
            if p.stat().st_size > 5_000_000:
                continue
            try:
                lines = p.read_text(encoding="utf-8").splitlines()
            except (UnicodeDecodeError, OSError):
                continue
            for i, line in enumerate(lines, 1):
                for name, rx in SECRET_PATTERNS:
                    if rx.search(line):
                        hits += 1
                        print(f"{p}:{i}: possible {name} (value not shown)")
    if hits:
        print(f"{hits} possible secret(s). Redact them before sharing. Screenshots cannot be scanned: review them by eye.")
        sys.exit(1)
    print("No secret-like patterns found in text files. (Screenshots/binaries are not scanned.)")


# ------------------------------------------------------------------ CLI
def build():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", help="run directory (default: $QA_RUN_DIR or qa-run)")
    sp = ap.add_subparsers(dest="cmd", required=True)

    p = sp.add_parser("init"); p.add_argument("--app", required=True); p.add_argument("--env", required=True, help="|".join(ENVS))
    p.add_argument("--tier", default="?", help="A (computer use) | B (browser automation) | C (terminal only)")
    p.add_argument("--notes"); p.add_argument("--force", action="store_true"); p.set_defaults(fn=cmd_init)

    p = sp.add_parser("add-feature", help="add one feature, or many with --csv")
    p.add_argument("--id"); p.add_argument("--module", default=""); p.add_argument("--page", default="")
    p.add_argument("--function"); p.add_argument("--priority", default="Medium", help="|".join(PRIORITIES))
    p.add_argument("--risk", default="secondary", help="|".join(RISK))
    p.add_argument("--destructive", action="store_true", help="deletes/overwrites data or has real-world side effects")
    p.add_argument("--related", default="", help="comma-separated feature IDs that depend on / are affected by this one")
    p.add_argument("--csv", help="columns: id,module,page,function,priority,risk,destructive,related"); p.set_defaults(fn=cmd_add_feature)

    p = sp.add_parser("set", help="change a feature's state"); p.add_argument("id"); p.add_argument("state", help="|".join(FEATURE_STATES))
    p.add_argument("--note"); p.add_argument("--evidence", action="append", help="file path or 'obs:<text>' (repeatable)")
    p.add_argument("--bug", help="BUG id(s) (required for FAILED)"); p.add_argument("--confirm-destructive", help="who confirmed, when"); p.set_defaults(fn=cmd_set)

    p = sp.add_parser("list"); p.add_argument("--state"); p.add_argument("--priority"); p.set_defaults(fn=cmd_list)
    p = sp.add_parser("next", help="suggest what to test next (risk-ordered)"); p.add_argument("--n", type=int, default=5); p.set_defaults(fn=cmd_next)

    def bugflags(p, update=False):
        p.add_argument("--title"); p.add_argument("--features", help="comma-separated feature IDs")
        p.add_argument("--severity", help="|".join(SEVERITIES)); p.add_argument("--confidence", help="|".join(CONFIDENCE))
        p.add_argument("--kind", help="|".join(KINDS)); p.add_argument("--category", help="engineering-order class: " + "|".join(CATEGORIES))
        p.add_argument("--precondition", action="append", default=[]); p.add_argument("--step", action="append", default=[], help="repeat per step, in order")
        p.add_argument("--expected"); p.add_argument("--actual"); p.add_argument("--repro", help="reproduced/attempted, e.g. 3/3")
        p.add_argument("--evidence", action="append", help="file path or 'obs:<text>' (repeatable)")
        p.add_argument("--context", help="console/network/log excerpt (short, redacted)")
        p.add_argument("--suspected-area"); p.add_argument("--suspected-basis", help="evidence supporting the suspected area")
        p.add_argument("--recommendation"); p.add_argument("--impl-area"); p.add_argument("--risk"); p.add_argument("--verification")

    p = sp.add_parser("add-bug"); bugflags(p); p.set_defaults(fn=cmd_add_bug)
    p = sp.add_parser("update-bug"); p.add_argument("id"); bugflags(p, True); p.set_defaults(fn=cmd_update_bug)
    p = sp.add_parser("mark-fixed", help="record a developer's CLAIM that a bug is fixed (unverified)"); p.add_argument("id"); p.add_argument("--note"); p.set_defaults(fn=cmd_mark_fixed)
    p = sp.add_parser("retest", help="record the result of re-running a bug's case in the running app")
    p.add_argument("id"); p.add_argument("--result", required=True, help="pass|fail"); p.add_argument("--note"); p.add_argument("--evidence", action="append"); p.set_defaults(fn=cmd_retest)
    p = sp.add_parser("note", help="record a non-defect observation"); p.add_argument("--type", required=True, help="|".join(NOTE_TYPES))
    p.add_argument("--text", required=True); p.add_argument("--feature"); p.set_defaults(fn=cmd_note)
    p = sp.add_parser("regression", help="print the regression checklist for a bug"); p.add_argument("id"); p.add_argument("--save", action="store_true"); p.set_defaults(fn=cmd_regression)
    p = sp.add_parser("status"); p.set_defaults(fn=cmd_status)
    p = sp.add_parser("report"); p.add_argument("--out"); p.set_defaults(fn=cmd_report)
    p = sp.add_parser("scan", help="scan text files for secret-like values"); p.add_argument("paths", nargs="*"); p.set_defaults(fn=cmd_scan)
    return ap


if __name__ == "__main__":
    args = build().parse_args()
    args.fn(args)
