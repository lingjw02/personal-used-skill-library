#!/usr/bin/env python3
"""Shared helpers for the Skill Performance Evaluator (stdlib only, YAML optional)."""
import hashlib, json, math, os, random, re, statistics
from datetime import datetime, timezone
from pathlib import Path

Z95 = 1.959963984540054
IGNORE_DIRS = {"__pycache__", ".git", "node_modules", ".venv", ".DS_Store"}
NON_RUN_FILES = {"grading.json", "timing.json", "metrics.json"}


# ---------- IO ----------
def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def iter_records(runs_dir):
    """Yield run records from *.json (one record or a list) and *.jsonl files, recursively.
    Unreadable files yield {"_load_error": ...} so callers can surface them instead of hiding them."""
    root = Path(runs_dir)
    if not root.exists():
        return
    for p in sorted(root.rglob("*")):
        if p.suffix == ".json" and p.name not in NON_RUN_FILES:
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception as e:
                yield {"_load_error": f"{p}: {e}"}
                continue
            for r in (data if isinstance(data, list) else [data]):
                if isinstance(r, dict):
                    r.setdefault("_source", str(p))
                    yield r
        elif p.suffix == ".jsonl":
            for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
                if line.strip():
                    try:
                        r = json.loads(line)
                        r.setdefault("_source", f"{p}:{i + 1}")
                        yield r
                    except Exception as e:
                        yield {"_load_error": f"{p}:{i + 1}: {e}"}


def parse_frontmatter(text):
    """Return (dict, error). Uses PyYAML if available, else a minimal parser."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return None, "No YAML frontmatter block found at top of SKILL.md"
    body = m.group(1)
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(body)
        if not isinstance(data, dict):
            return None, "Frontmatter is not a YAML mapping"
        return data, None
    except ImportError:
        pass
    except Exception as e:
        return None, f"Invalid YAML frontmatter: {e}"
    data, key = {}, None
    for line in body.splitlines():
        if re.match(r"^[A-Za-z0-9_-]+\s*:", line):
            k, _, v = line.partition(":")
            key, v = k.strip(), v.strip()
            data[key] = "" if v in (">", "|", ">-", "|-") else v.strip("'\"")
        elif key and line.startswith((" ", "\t")):
            data[key] = (str(data.get(key, "")) + " " + line.strip()).strip()
    return data, None


def hash_dir(root):
    h = hashlib.sha256()
    files = []
    root = Path(root)
    for dp, dns, fns in os.walk(root):
        dns[:] = sorted(d for d in dns if d not in IGNORE_DIRS)
        for fn in sorted(fns):
            if fn in IGNORE_DIRS or fn.endswith(".pyc"):
                continue
            p = Path(dp) / fn
            rel = p.relative_to(root).as_posix()
            data = p.read_bytes()
            h.update(rel.encode() + b"\0" + hashlib.sha256(data).digest())
            files.append({"path": rel, "bytes": len(data)})
    return h.hexdigest(), files


# ---------- stats ----------
def wilson(k, n, z=Z95):
    """Wilson score interval for a proportion. Returns [lo, hi] or None when n == 0."""
    if n <= 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def describe(values):
    v = [x for x in values if isinstance(x, (int, float)) and not isinstance(x, bool)]
    if not v:
        return {"measured": False, "n": 0}
    return {"measured": True, "n": len(v), "mean": round(statistics.fmean(v), 4),
            "median": round(statistics.median(v), 4), "min": min(v), "max": max(v),
            "stddev": round(statistics.stdev(v), 4) if len(v) > 1 else None}


def rel_change(new, old):
    if new is None or old is None or old == 0:
        return None
    return round((new - old) / old, 4)


def fisher_exact(k1, n1, k2, n2):
    """Two-sided Fisher exact p-value comparing pass counts k1/n1 vs k2/n2."""
    if n1 <= 0 or n2 <= 0:
        return None
    K, N = k1 + k2, n1 + n2

    def pmf(x):
        return math.comb(n1, x) * math.comb(n2, K - x) / math.comb(N, K)

    lo, hi = max(0, K - n2), min(n1, K)
    p_obs = pmf(k1)
    return round(min(1.0, sum(pmf(x) for x in range(lo, hi + 1) if pmf(x) <= p_obs * (1 + 1e-9))), 6)


def bootstrap_mean_ci(diffs, iters=5000, seed=0, min_n=5):
    """Percentile bootstrap CI for the mean of paired per-eval differences. None if too few evals."""
    if len(diffs) < min_n:
        return None
    rng = random.Random(seed)
    n = len(diffs)
    means = sorted(sum(rng.choice(diffs) for _ in range(n)) / n for _ in range(iters))
    return [round(means[int(0.025 * iters)], 4), round(means[int(0.975 * iters) - 1], 4)]
