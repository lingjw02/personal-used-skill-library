#!/usr/bin/env python3
"""LEVEL 1 - Structure validation of a target skill. Static inspection only.

Usage: python validate_structure.py <target-skill-dir> [--out results/structure.json]

Every finding is labelled error|warn|info. This script performs STATIC INSPECTION; it never executes
the target's scripts (it only parses them), so a clean result says nothing about runtime behaviour.
"""
import argparse, ast, importlib.util, json, os, re, shutil, subprocess, sys
from pathlib import Path
from _common import IGNORE_DIRS, load_json, parse_frontmatter, write_json

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KNOWN_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility", "version"}
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
TICK = re.compile(r"`((?:references|scripts|assets|examples|evals|tests|agents|templates)/[^`\s]+)`")
BARE = re.compile(r"(?<![\w/.\-])((?:references|scripts|assets|examples|evals|tests|agents)/[\w./\-]+\.\w+)")
SKIP_CHARS = set("*<>{}$|")


def clean(ref):
    ref = ref.split("#")[0].strip().rstrip(".,:;)'\"")
    return ref


def extract_refs(text):
    refs = {}
    for m in LINK.finditer(text):
        r = clean(m.group(1))
        if r and not re.match(r"^(https?:|mailto:|#)", r):
            refs.setdefault(r, "link")
    for rx, kind in ((TICK, "inline"), (BARE, "inline")):
        for m in rx.finditer(text):
            refs.setdefault(clean(m.group(1)), kind)
    return {r: k for r, k in refs.items() if r and not (set(r) & SKIP_CHARS)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    root = Path(a.target).resolve()
    checks = []

    def add(level, code, msg, path=None):
        checks.append({"level": level, "code": code, "message": msg, "path": path})

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        add("error", "missing_skill_md", "SKILL.md not found")
        return finish(root, checks, a.out)
    text = skill_md.read_text(encoding="utf-8")

    # frontmatter
    fm, err = parse_frontmatter(text)
    if err:
        add("error", "frontmatter_invalid", err, "SKILL.md")
        fm = {}
    name, desc = fm.get("name"), fm.get("description")
    if not name:
        add("error", "missing_name", "Frontmatter has no 'name'", "SKILL.md")
    else:
        if not isinstance(name, str) or not NAME_RE.match(name):
            add("error", "invalid_name", f"name '{name}' should be lowercase letters/digits/hyphens", "SKILL.md")
        if isinstance(name, str) and len(name) > 64:
            add("warn", "name_too_long", f"name is {len(name)} chars (limit commonly 64)", "SKILL.md")
        if isinstance(name, str) and root.name != name:
            add("info", "name_dir_mismatch", f"directory '{root.name}' differs from name '{name}' (may be fine if the folder was renamed for evaluation)", "SKILL.md")
    if not desc:
        add("error", "missing_description", "Frontmatter has no 'description' (primary trigger signal)", "SKILL.md")
    else:
        d = str(desc)
        if len(d) > 1024:
            add("warn", "description_too_long", f"description is {len(d)} chars (limit commonly 1024)", "SKILL.md")
        if len(d) < 60:
            add("warn", "description_short", f"description is only {len(d)} chars; may under-specify triggers", "SKILL.md")
        if re.search(r"(?i)\b(use (this )?(skill )?when|whenever|trigger)", d) is None:
            add("info", "description_no_trigger_cue", "description has no explicit 'use when' style trigger cue (hypothesis to check in trigger evaluation, not a defect by itself)", "SKILL.md")
    for k in fm:
        if k not in KNOWN_KEYS:
            add("info", "nonstandard_frontmatter_key", f"frontmatter key '{k}' is not in the commonly documented set {sorted(KNOWN_KEYS)}", "SKILL.md")

    lines = text.count("\n") + 1
    if lines > 500:
        add("warn", "skill_md_long", f"SKILL.md has {lines} lines (>500 hurts progressive disclosure)", "SKILL.md")

    # nested SKILL.md
    for p in root.rglob("SKILL.md"):
        if p != skill_md and not (set(p.relative_to(root).parts) & IGNORE_DIRS) and "evals" not in p.relative_to(root).parts[:1]:
            add("warn", "nested_skill_md", "nested SKILL.md (some platforms accept exactly one per skill)", p.relative_to(root).as_posix())

    # references from SKILL.md and README.md
    docs = {"SKILL.md": text}
    if (root / "README.md").exists():
        docs["README.md"] = (root / "README.md").read_text(encoding="utf-8", errors="replace")
    referenced = set()
    for docname, body in docs.items():
        for ref, kind in extract_refs(body).items():
            if docname == "SKILL.md":
                referenced.add(ref)
            target = (root / ref)
            if not target.exists():
                if docname == "SKILL.md":
                    add("error" if kind == "link" else "warn",
                        "broken_reference" if kind == "link" else "possibly_broken_reference",
                        f"{docname} references '{ref}' which does not exist" + ("" if kind == "link" else " (may be a placeholder inside an example)"), docname)
                else:
                    add("warn", "documentation_inconsistency", f"README.md references '{ref}' which does not exist", docname)

    # scripts
    scripts_dir = root / "scripts"
    local_mods = {p.stem for p in scripts_dir.glob("*.py")} | {p.name for p in scripts_dir.iterdir() if p.is_dir()} if scripts_dir.exists() else set()
    stdlib = getattr(sys, "stdlib_module_names", set())
    third_party = {}
    if scripts_dir.exists():
        for p in sorted(scripts_dir.rglob("*")):
            if p.is_dir() or set(p.parts) & IGNORE_DIRS:
                continue
            rel = p.relative_to(root).as_posix()
            if p.stat().st_size == 0:
                add("warn", "empty_script", "script file is empty", rel)
                continue
            head = p.read_text(encoding="utf-8", errors="replace")
            has_shebang = head.startswith("#!")
            if p.suffix == ".py":
                try:
                    tree = ast.parse(head)
                except SyntaxError as e:
                    add("error", "python_syntax_error", f"line {e.lineno}: {e.msg}", rel)
                    continue
                for n in ast.walk(tree):
                    mods = [n.module] if isinstance(n, ast.ImportFrom) and n.module and n.level == 0 else \
                           [x.name for x in n.names] if isinstance(n, ast.Import) else []
                    for m in mods:
                        top = m.split(".")[0]
                        if top and top not in stdlib and top not in local_mods:
                            third_party.setdefault(top, set()).add(rel)
            elif p.suffix == ".sh" and shutil.which("bash"):
                r = subprocess.run(["bash", "-n", str(p)], capture_output=True, text=True)
                if r.returncode != 0:
                    add("error", "shell_syntax_error", r.stderr.strip()[:200], rel)
            if has_shebang and not os.access(p, os.X_OK):
                add("info", "not_executable", "has shebang but no executable bit (fine if invoked via interpreter; packaging may drop modes)", rel)
            if p.suffix in (".py", ".sh") and not has_shebang and rel not in referenced:
                pass
    for mod, files in sorted(third_party.items()):
        if importlib.util.find_spec(mod) is None:
            add("warn", "dependency_not_installed_here", f"third-party module '{mod}' imported by {sorted(files)} is not installed in this environment (the skill may declare/install it elsewhere)", sorted(files)[0])
        else:
            add("info", "third_party_dependency", f"imports '{mod}' (available here)", sorted(files)[0])
    if third_party and not any((root / f).exists() for f in ("requirements.txt", "pyproject.toml", "package.json")) and "compatibility" not in fm:
        add("info", "dependencies_undeclared", f"third-party imports {sorted(third_party)} but no requirements file or 'compatibility' note", None)

    # orphans (collapsed when numerous, e.g. vendored schema folders)
    unref = []
    for sub in ("references", "scripts", "assets"):
        d = root / sub
        if d.exists():
            for p in d.rglob("*"):
                if p.is_file() and not (set(p.parts) & IGNORE_DIRS) and not p.name.startswith("_"):
                    rel = p.relative_to(root).as_posix()
                    if rel not in referenced and not any(r.endswith(rel) or rel.endswith(r) for r in referenced) \
                            and not any(rel.startswith(r.rstrip("/") + "/") for r in referenced):
                        unref.append(rel)
    if len(unref) > 8:
        add("info", "unreferenced_files", f"{len(unref)} files not referenced from SKILL.md (agent may never discover them); first 5: {unref[:5]}", None)
    else:
        for rel in unref:
            add("info", "unreferenced_file", "file not referenced from SKILL.md (agent may never discover it)", rel)

    # existing evals
    ev = root / "evals" / "evals.json"
    if ev.exists():
        try:
            data = json.loads(ev.read_text(encoding="utf-8"))
            n = len(data.get("evals", [])) if isinstance(data, dict) else 0
            add("info", "evals_present", f"evals/evals.json parses; {n} eval(s) declared", "evals/evals.json")
            for e in data.get("evals", []):
                for f in e.get("files", []) or []:
                    if not (root / f).exists():
                        add("warn", "eval_file_missing", f"eval {e.get('id')} references missing input file '{f}'", "evals/evals.json")
        except Exception as e:
            add("error", "evals_invalid_json", str(e), "evals/evals.json")
    else:
        add("info", "no_evals", "target ships no evals/evals.json; a suite must be designed (label criteria 'Inferred criterion')", None)

    finish(root, checks, a.out)


def finish(root, checks, out):
    s = {lv: sum(1 for c in checks if c["level"] == lv) for lv in ("error", "warn", "info")}
    result = {"schema_version": 1, "method": "static inspection", "target": str(root),
              "summary": s, "passed": s["error"] == 0, "checks": checks}
    if out:
        write_json(out, result)
    for c in checks:
        print(f"[{c['level'].upper():5}] {c['code']}: {c['message']}" + (f"  ({c['path']})" if c['path'] else ""))
    print(f"\nerrors={s['error']} warnings={s['warn']} info={s['info']}  (static inspection only)")
    sys.exit(0 if s["error"] == 0 else 1)


if __name__ == "__main__":
    main()
