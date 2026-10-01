#!/usr/bin/env python3
"""Generate summary.json, summary.md, comparison.md, failure-analysis.md, benchmark.md and README.md
from the measured JSON in <results>/. JSON is the source of truth: every number printed here is read
from it; unavailable values are printed as "Not measured".

Usage:
  python generate_report.py --results results [--skill <target-skill-dir>] [--target-readme <path>]
         [--readme-meta readme-meta.json] [--narrative results/narrative.json] [--primary-key KEY]
         [--no-history-append]

README handling: evaluation-derived sections are wrapped in <!-- skill-eval:begin NAME --> markers so
re-running updates only those blocks and preserves author-written text. If --target-readme exists and
has no markers, it is NOT modified; README.generated.md is written beside it.
"""
import argparse, re, sys
from pathlib import Path
from _common import load_json, now_iso, parse_frontmatter, write_json

NM = "Not measured"
MANAGED = ["evaluation-methodology", "test-coverage", "performance", "baseline-comparison", "version-comparison",
           "failure-analysis", "evaluation-results", "limitations", "reproducibility", "evaluation-history"]

METRIC_DEFS = [
    ("Pass Rate", "graded runs that passed / graded runs. A run passes when every assertion passed (or `passed` was set true by the grader)."),
    ("Failure Rate", "1 - Pass Rate."),
    ("Skill Lift", "skill-assisted pass rate - baseline pass rate, in percentage points (pp), over evals present in both configurations."),
    ("Trigger Precision", "TP / (TP + FP): of the prompts where the skill triggered, the share that should have triggered."),
    ("Trigger Recall", "TP / (TP + FN): of the prompts that should trigger the skill, the share that did."),
    ("F1", "2TP / (2TP + FP + FN): harmonic mean of precision and recall."),
    ("Reliability", "per-eval consistency across repeated runs: share of evals (with 2+ runs) that always pass / always fail / are flaky."),
    ("Average / Median Runtime", "mean / median wall-clock `duration_s` over graded runs that recorded it."),
    ("Token Usage", "mean `tokens` over graded runs that recorded it."),
    ("Tool Calls", "mean `tool_calls` over graded runs that recorded it."),
    ("Error Count", "mean `errors` per graded run, as recorded by the harness."),
    ("Artifact Success Rate", "runs with `artifacts_ok` true / runs where `artifacts_ok` was recorded."),
    ("Regression Rate", "evals classified `regressed` between versions / shared evals."),
    ("95% CI (Wilson)", "Wilson score interval for a proportion; run-level and approximate when runs of one eval are repeated."),
]


# ---------- formatting ----------
def pct(x, d=1): return NM if x is None else f"{x * 100:.{d}f}%"
def pp(x): return "—" if x is None else f"{x:+.1f} pp"
def relp(x): return "—" if x is None else f"{x * 100:+.1f}%"
def secs(x): return NM if x is None else f"{x:.1f}s"
def cnt(x): return NM if x is None else f"{x:.1f}"
def tok(x): return NM if x is None else (f"{x / 1000:.1f}k" if x >= 1000 else f"{x:.0f}")
def cis(c): return "n/a" if not c else f"{c[0] * 100:.1f}–{c[1] * 100:.1f}%"
def mean_of(stat): return stat.get("mean") if isinstance(stat, dict) and stat.get("measured") else None
def kv(d):
    return ", ".join(f"{k}: {v}" for k, v in d.items()) if d else "none"


def table(header, rows):
    return ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]


class Ctx:
    def __init__(s, d, primary):
        s.d = Path(d)
        L = lambda n, dflt=None: load_json(s.d / n, dflt)
        s.meta, s.env = L("metadata.json", {}) or {}, L("environment.json", {}) or {}
        s.perf, s.evals = L("performance.json"), L("evaluations.json")
        s.trig, s.reg = L("trigger-report.json"), L("regression.json")
        s.fails = (L("failures.json", {}) or {}).get("failures", [])
        s.struct, s.selfc, s.narr = L("structure.json"), L("selfcheck.json"), L("narrative.json", {}) or {}
        cfgs = (s.perf or {}).get("configurations", {})
        ver = s.meta.get("skill_version")
        s.skey = primary or (f"with_skill@{ver}" if f"with_skill@{ver}" in cfgs else next((k for k in cfgs if k != "without_skill"), None))
        s.cfg = cfgs.get(s.skey); s.base = cfgs.get("without_skill")
        s.delta = ((s.perf or {}).get("deltas_vs_baseline", {}) or {}).get(s.skey) if s.perf else None
        ver_key = s.skey.split("@", 1)[1] if s.skey and "@" in s.skey else None
        bv = (s.trig or {}).get("by_version", {})
        s.tg = bv.get(ver_key) or (next(iter(bv.values())) if len(bv) == 1 else None)
        s.name = s.meta.get("skill_name") or "unknown-skill"


# ---------- shared blocks ----------
def perf_rows(c):
    sk, bs, dl = c.cfg, c.base, c.delta if (c.delta and c.delta.get("measured")) else None
    rows = []
    if not sk:
        return None
    if dl:
        rows.append(["Pass Rate", pct(dl["baseline_pass_rate"]), pct(dl["skill_pass_rate"]), pp(dl["skill_lift_pp"])])
    else:
        rows.append(["Pass Rate", "N/A (no paired baseline)" if not bs else NM, pct(sk["pass_rate"]), "—"])
    for m, nm in (("precision", "Trigger Precision"), ("recall", "Trigger Recall"), ("f1", "Trigger F1")):
        x = c.tg["metrics"][m] if c.tg else None
        rows.append([nm, "N/A", pct(x["value"]) if x and x.get("measured") else NM, "—"])
    for m, nm, f in (("time_seconds", "Avg Runtime", secs), ("tokens", "Avg Tokens", tok), ("tool_calls", "Avg Tool Calls", cnt)):
        if dl and dl[m]["baseline_mean"] is not None and dl[m]["skill_mean"] is not None:
            rows.append([nm, f(dl[m]["baseline_mean"]), f(dl[m]["skill_mean"]), relp(dl[m]["relative_change"])])
        else:
            rows.append([nm, f(mean_of(bs[m])) if bs else "N/A", f(mean_of(sk[m])), "—"])
    a_s, a_b = sk["artifact_success"], (bs or {}).get("artifact_success", {})
    rows.append(["Artifact Success Rate", pct(a_b.get("rate")) if a_b.get("measured") else (NM if bs else "N/A"),
                 pct(a_s.get("rate")) if a_s.get("measured") else NM,
                 pp((a_s["rate"] - a_b["rate"]) * 100) if a_s.get("measured") and a_b.get("measured") else "—"])
    rows.append(["Errors per run", cnt(mean_of(bs["errors_per_run"])) if bs else "N/A", cnt(mean_of(sk["errors_per_run"])), "—"])
    return rows


def perf_block(c, h="###"):
    L = []
    rows = perf_rows(c)
    if not rows:
        return ["Not measured: no graded functional runs.", ""]
    L += table(["Metric", "Baseline", "With Skill", "Delta"], rows) + [""]
    if c.delta and c.delta.get("measured"):
        L.append(f"Baseline/skill columns cover {len(c.delta['paired_evals'])} paired eval(s) ({c.delta['baseline_runs']} baseline runs, {c.delta['skill_runs']} skill runs). Deltas: pass rate in percentage points, other metrics as relative change.")
        ci = c.delta.get("eval_level_lift_ci95_bootstrap_pp")
        L.append(f"Eval-level skill lift {c.delta['eval_level_mean_lift_pp']:+.1f} pp, 95% bootstrap CI " + (f"[{ci[0]:+.1f}, {ci[1]:+.1f}] pp" if ci else "not computed (fewer than 5 paired evals)") + ".")
    sk = c.cfg
    L.append(f"With skill (`{c.skey}`): {sk['n_passed']}/{sk['n_runs_graded']} graded runs passed, pass rate {pct(sk['pass_rate'])}, 95% Wilson CI {cis(sk['pass_rate_ci95_wilson'])}.")
    if c.base:
        b = c.base
        L.append(f"Baseline: {b['n_passed']}/{b['n_runs_graded']} graded runs passed, pass rate {pct(b['pass_rate'])}, 95% Wilson CI {cis(b['pass_rate_ci95_wilson'])}.")
    L.append("")
    return L


def tradeoff_line(c):
    d = c.delta
    if not (d and d.get("measured")):
        return "MEASURED: no paired baseline comparison available."
    parts = [f"pass rate {d['skill_lift_pp']:+.1f} pp"]
    for m, nm in (("tokens", "tokens"), ("time_seconds", "runtime"), ("tool_calls", "tool calls")):
        parts.append(f"{nm} {relp(d[m]['relative_change'])}" if d[m]["relative_change"] is not None else f"{nm} {NM.lower()}")
    return "MEASURED (skill vs baseline): " + "; ".join(parts) + "."


def reliability_block(c):
    sk = c.cfg
    if not sk:
        return ["Not measured."]
    cons = sk["consistency"]
    if not cons.get("measured"):
        return [f"Not measured: {cons.get('reason')}. A single run is not evidence of reliability."]
    n = cons["evals_with_2plus_runs"]
    L = [f"MEASURED: of {n} eval(s) with 2+ graded runs, {cons['all_pass']} always passed, {cons['all_fail']} always failed, {cons['flaky']} were flaky (mixed results).",
         f"Min runs per eval: {sk['min_runs_per_eval']}."]
    if sk["min_runs_per_eval"] < 3:
        L.append("UNCERTAINTY: fewer than 3 runs for some evals; variance estimates are weak.")
    rows = [[e["eval_id"], f"{e['configs'][c.skey]['n_passed']}/{e['configs'][c.skey]['n_runs']}"] for e in (c.evals or {}).get("evals", []) if c.skey in e["configs"] and e["configs"][c.skey]["flaky"]]
    if rows:
        L += ["", "Flaky evals:"] + table(["Eval", "Passed/Runs"], rows)
    return L


def trigger_block(c):
    if not c.tg:
        return ["Not measured: no trigger records."]
    g = c.tg; cf = g["confusion"]; m = g["metrics"]
    f = lambda x: f"{pct(x['value'])} (95% CI {cis(x.get('ci95_wilson'))})" if x.get("measured") else f"{NM} ({x.get('reason')})"
    L = table(["", "Predicted: triggered", "Predicted: not triggered"], [["Should trigger", f"TP={cf['tp']}", f"FN={cf['fn']}"], ["Should not trigger", f"FP={cf['fp']}", f"TN={cf['tn']}"]]) + [""]
    L += [f"Precision {f(m['precision'])}; Recall {f(m['recall'])}; F1 {pct(m['f1'].get('value')) if m['f1'].get('measured') else NM}.",
          f"Observation methods: {kv(g['observation_methods'])}; unobservable records: {g['unobservable_records']}."]
    if g["missed_positive_cases"]: L.append(f"Missed positives (not always triggered): {', '.join(g['missed_positive_cases'])}.")
    if g["false_trigger_cases"]: L.append(f"False triggers: {', '.join(g['false_trigger_cases'])}.")
    L += [f"LIMITATION: {x}" for x in g["limitations"]]
    return L


def failure_block(c, detail=False):
    skf = [f for f in c.fails if f["configuration"] == c.skey]
    bsf = [f for f in c.fails if f["configuration"] == "without_skill"]
    L = [f"MEASURED: {len(skf)} failed graded run(s) with skill; {len(bsf)} failed baseline run(s)."]
    if not skf:
        return L + ["No failures recorded for the skill configuration in graded runs."]
    nd = sum(1 for f in skf if not (f.get("diagnosis") or {}).get("likely_cause"))
    if nd:
        L.append(f"UNCERTAINTY: {nd} of {len(skf)} skill failure(s) have no diagnosis yet (cause not determined).")
    by = {}
    for f in skf:
        by.setdefault(f["eval_id"], []).append(f)
    rows = []
    for e, fs in sorted(by.items()):
        n = ((c.cfg or {}).get("n_runs_graded") and next((x["configs"][c.skey]["n_runs"] for x in c.evals["evals"] if x["eval_id"] == e and c.skey in x["configs"]), None))
        cat = sorted({f.get("failure_category") or "uncategorised" for f in fs})
        conf = sorted({(f.get("diagnosis") or {}).get("cause_confidence") or "undiagnosed" for f in fs})
        rows.append([e, f"{len(fs)}/{n}" if n else len(fs), ", ".join(cat), ", ".join(conf)])
    L += [""] + table(["Eval", "Failed/Runs", "Category", "Cause confidence"], rows)
    if detail:
        for f in skf:
            d = f.get("diagnosis") or {}
            L += ["", f"### {f['eval_id']} (run {f['run']}, {f['configuration']})",
                  f"- **Prompt:** {f.get('prompt') or NM}", f"- **Expected behavior:** {f.get('expected_behavior') or NM}",
                  f"- **Actual behavior:** {f.get('actual_behavior') or NM}", f"- **Failure category:** {f.get('failure_category') or 'uncategorised'}",
                  "- **Evidence:** " + ("; ".join(str(x) for x in f.get("evidence") or []) or NM),
                  f"- **Likely cause:** {d.get('likely_cause') or 'Not diagnosed'} ({d.get('cause_confidence') or 'no confidence assigned'})",
                  f"- **Suggested modification:** {d.get('suggested_modification') or 'Not provided'}"]
    return L


def version_block(c):
    r = c.reg
    if not r:
        return ["Not evaluated: no version comparison (regression.json) is available."]
    L = [f"Compared `{r['a']['key']}` (A) with `{r['b']['key']}` (B) over {r['fairness']['shared_evals']} shared eval(s). No overall winner is declared.", ""]
    ag = r["aggregate"]["pass_rate"]
    L.append(f"MEASURED pass rate: A {pct(ag['a'])} -> B {pct(ag['b'])} ({pp(ag['delta_pp'])}).")
    for m, nm, f in (("tokens", "tokens", tok), ("time_seconds", "runtime", secs), ("tool_calls", "tool calls", cnt)):
        x = r["aggregate"][m]
        L.append(f"MEASURED {nm}: A {f(x['a_mean'])} -> B {f(x['b_mean'])} ({relp(x['relative_change'])})." if x["measured"] else f"{nm}: {NM}.")
    sup = {x["eval_id"]: x["statistically_supported"] for x in r["per_eval"]}
    tag = lambda ids: ", ".join(f"{i}{'' if sup.get(i) else ' (not stat. supported)'}" for i in ids) or "none"
    L += ["", f"- **Improvements:** {tag(r['improvements'])}", f"- **Regressions:** {tag(r['regressions'])}",
          f"- **Unchanged:** {len(r['unchanged'])} eval(s)", f"- **New failures** (A all-pass, B not): {', '.join(r['new_failures']) or 'none'}",
          f"- **Removed failures** (A had failures, B all-pass): {', '.join(r['removed_failures']) or 'none'}",
          f"- **Failure categories new in B / removed in B:** {', '.join(r['failure_categories']['new_in_b']) or 'none'} / {', '.join(r['failure_categories']['removed_in_b']) or 'none'}",
          f"- **Regression rate:** {pct(r['regression_rate'])}"]
    L += [f"WARNING: {w}" for w in r["warnings"]]
    return L


def env_rows(c):
    e, m = c.env, c.meta
    runs = [x["min_runs_per_eval"] for x in ((c.perf or {}).get("configurations", {}) or {}).values()]
    val = lambda v: v if v not in (None, "") else "not recorded"
    return [["Target skill", val(m.get("skill_name"))], ["Skill version", f"{val(m.get('skill_version'))} ({m.get('version_source', 'unknown source')})"],
            ["Skill content SHA-256", (m.get("content_sha256") or "not recorded")[:16] + "…"], ["Model", val(e.get("model"))],
            ["Agent / harness", " ".join(f"{val(e.get('agent'))} {e.get('agent_version') or ''}".split()) + f" / {val(e.get('harness'))}"],
            ["OS", val(e.get("os"))], ["Python", val(e.get("python"))], ["Evaluation date", val(e.get("evaluation_date"))],
            ["Test suite version", val(m.get("suite_version") or e.get("suite_version"))],
            ["Min runs per eval (per configuration)", ", ".join(str(r) for r in runs) or NM],
            ["Available tools", ", ".join(e["available_tools"]) if e.get("available_tools") else "not recorded"],
            ["Execution modes in graded runs", "; ".join(f"{k} -> {kv(v['execution_modes'])}" for k, v in ((c.perf or {}).get("configurations", {}) or {}).items()) or NM]]


def coverage_block(c):
    rows = (c.evals or {}).get("evals", [])
    if not rows:
        return ["Not measured: no evaluation results."]
    cnt_by = lambda k: {v: sum(1 for r in rows if (r.get(k) or "unspecified") == v) for v in sorted({(r.get(k) or "unspecified") for r in rows})}
    L = [f"MEASURED: {len(rows)} functional eval(s) with graded runs.", f"- By category: {kv(cnt_by('category'))}", f"- By difficulty: {kv(cnt_by('difficulty'))}"]
    if c.tg:
        L.append(f"- Trigger prompts: {len(c.tg['per_case'])} distinct ({sum(1 for x in c.tg['per_case'] if x['expected_trigger'])} positive, {sum(1 for x in c.tg['per_case'] if not x['expected_trigger'])} negative).")
    else:
        L.append("- Trigger prompts: Not measured.")
    if c.perf:
        ex = {k: v["excluded_runs"] for k, v in c.perf["configurations"].items() if v["excluded_runs"]}
        if ex: L.append("- Runs excluded from metrics (counted, not hidden): " + "; ".join(f"{k} -> {kv(v)}" for k, v in ex.items()))
    return L


def results_table(c):
    rows = []
    for e in (c.evals or {}).get("evals", []):
        s, b = e["configs"].get(c.skey), e["configs"].get("without_skill")
        f = lambda x: f"{x['n_passed']}/{x['n_runs']}" + (" (flaky)" if x["flaky"] else "") if x else "—"
        rows.append([e["eval_id"], e.get("category") or "", f(b), f(s)])
    return table(["Eval", "Category", "Baseline passed/runs", "Skill passed/runs"], rows) if rows else ["Not measured."]


def limitations(c):
    L = ["Results may vary between models, agents/harnesses, environments, and individual runs; they describe the conditions recorded under Reproducibility only."]
    if c.perf:
        L += list(c.perf.get("warnings", []))
    if c.tg:
        L += c.tg["limitations"]
    if c.struct:
        L.append("Structure validation is static inspection; it does not show that scripts run correctly.")
    L += c.narr.get("limitations", [])
    seen, out = set(), []
    for x in L:
        if x not in seen: seen.add(x); out.append(x)
    return out


def narrative_blocks(c):
    L = []
    for x in c.narr.get("inferences", []):
        L.append(f"INFERENCE: {x['text']} (evidence: {', '.join(x.get('evidence', [])) or 'none cited'})")
    for x in c.narr.get("uncertainties", []):
        L.append(f"UNCERTAINTY: {x}")
    return L


def recs_block(c):
    recs = c.narr.get("recommendations", [])
    if not recs:
        return ["No evidence-backed recommendations recorded (add them to narrative.json; each must cite evidence)."]
    L = []
    for r in recs:
        if not r.get("evidence"):
            L.append(f"- (omitted: recommendation '{r.get('id', '?')}' cites no evidence)")
            continue
        L.append(f"- **{r.get('id', '')} RECOMMENDATION:** {r['text']}  \n  Evidence: {', '.join(r['evidence'])}" + (f"  \n  Verify by: {r['verification']}" if r.get("verification") else ""))
    return L


def methodology():
    return ["### Structure Validation", "Static checks of SKILL.md frontmatter, referenced files, script syntax and declared dependencies (`validate_structure.py`). Static inspection only; nothing is executed.", "",
            "### Trigger Evaluation", "Positive prompts (should activate) and negative/near-miss prompts (should not) are run; triggering is recorded only when the harness exposes an observable signal. Precision, recall and F1 come from the confusion matrix.", "",
            "### Functional Evaluation", "Realistic tasks run with assertions graded by the strongest available method: deterministic checks first, then artifact/schema checks, rubrics, and an LLM judge only when needed.", "",
            "### Baseline Comparison", "Each eval is run without and with the skill under the same model, environment and prompt; the delta is computed over evals present in both.", "",
            "### Reliability Testing", "Evals are repeated; pass rate, per-eval consistency, flaky evals, and Wilson intervals are reported. A single run is never treated as proof of reliability.", "",
            "### Regression Testing", "Two skill versions are compared per eval (Fisher exact test for support), reporting improvements, regressions, unchanged areas, new and removed failures, without declaring a single winner.", "",
            "### Metric Definitions"] + [f"- **{k}:** {v}" for k, v in METRIC_DEFS]


# ---------- history ----------
def update_history(c, path, append):
    h = load_json(path, {"schema_version": 1, "entries": []})
    if append and c.cfg:
        key = f"{c.meta.get('skill_version')}|{c.meta.get('suite_version')}|{(c.env.get('evaluation_date') or '')[:10]}|{c.skey}"
        entry = {"run_id": key, "date": (c.env.get("evaluation_date") or now_iso())[:10], "skill_version": c.meta.get("skill_version"),
                 "suite_version": c.meta.get("suite_version"), "model": c.env.get("model"), "agent": c.env.get("agent"),
                 "n_runs_graded": c.cfg["n_runs_graded"], "pass_rate": c.cfg["pass_rate"], "pass_rate_ci95": c.cfg["pass_rate_ci95_wilson"],
                 "precision": (c.tg["metrics"]["precision"].get("value") if c.tg and c.tg["metrics"]["precision"].get("measured") else None),
                 "recall": (c.tg["metrics"]["recall"].get("value") if c.tg and c.tg["metrics"]["recall"].get("measured") else None),
                 "avg_tokens": mean_of(c.cfg["tokens"]), "avg_runtime_s": mean_of(c.cfg["time_seconds"])}
        h["entries"] = [e for e in h["entries"] if e["run_id"] != key] + [entry]
        write_json(path, h)
    return h


def history_block(h):
    es = sorted(h.get("entries", []), key=lambda e: (e["date"], str(e["skill_version"])))
    if not es:
        return ["No evaluation history recorded yet."]
    rows = [[e["skill_version"], pct(e["pass_rate"]), pct(e["precision"]), pct(e["recall"]), tok(e["avg_tokens"]), secs(e["avg_runtime_s"]), e["n_runs_graded"], e["date"], e.get("suite_version")] for e in es]
    return table(["Version", "Pass Rate", "Precision", "Recall", "Avg Tokens", "Avg Runtime", "Graded runs", "Date", "Suite"], rows) + ["", "Rows from different suite versions, models or dates are not directly comparable; see regression analysis for like-for-like comparisons."]


# ---------- documents ----------
def build_summary_md(c):
    L = [f"# Evaluation Report: {c.name}", f"_Generated {now_iso()} from JSON in `{c.d}`._", "", "## 1. Executive Summary"]
    L.append(f"FACT: skill `{c.name}`, version `{c.meta.get('skill_version') or 'not recorded'}`.")
    if c.struct:
        s = c.struct["summary"]; L.append(f"FACT (static inspection): structure validation found {s['error']} error(s), {s['warn']} warning(s), {s['info']} info note(s).")
    if c.cfg:
        L.append(f"MEASURED: with-skill pass rate {pct(c.cfg['pass_rate'])} ({c.cfg['n_passed']}/{c.cfg['n_runs_graded']} graded runs, 95% CI {cis(c.cfg['pass_rate_ci95_wilson'])}).")
        L.append(tradeoff_line(c))
    else:
        L.append("MEASURED: no graded functional runs; no performance claims can be made.")
    if c.tg:
        m = c.tg["metrics"]; L.append(f"MEASURED: trigger precision {pct(m['precision'].get('value')) if m['precision'].get('measured') else NM}, recall {pct(m['recall'].get('value')) if m['recall'].get('measured') else NM}.")
    L += narrative_blocks(c)
    L += ["", "## 2. Environment"] + table(["Item", "Value"], env_rows(c))
    L += ["", "## 3. Test Scope", "Pipeline stages with data: " + ", ".join(n for n, ok in (("structure", c.struct), ("trigger", c.tg), ("functional/baseline", c.cfg), ("reliability", c.cfg and c.cfg["consistency"].get("measured")), ("regression", c.reg)) if ok) + ".",
          "Stages with no data (Not measured): " + (", ".join(n for n, ok in (("structure", c.struct), ("trigger", c.tg), ("functional/baseline", c.cfg), ("reliability", c.cfg and c.cfg["consistency"].get("measured")), ("regression", c.reg)) if not ok) or "none") + "."]
    L += ["", "## 4. Test Coverage"] + coverage_block(c)
    L += ["", "## 5. Results", "", "### Performance"] + perf_block(c) + ["### Per-eval results"] + results_table(c) + ["", "### Trigger evaluation"] + trigger_block(c)
    L += ["", "## 6. Baseline Comparison", tradeoff_line(c), "", "Quality vs cost is reported above without declaring an overall winner."]
    L += ["", "## 7. Reliability"] + reliability_block(c)
    L += ["", "## 8. Regression Analysis"] + version_block(c)
    L += ["", "## 9. Failures"] + failure_block(c)
    L += ["", "## 10. Recommended Changes"] + recs_block(c)
    L += ["", "## 11. Limitations"] + [f"- {x}" for x in limitations(c)]
    if c.selfc:
        L.append(f"- Self-validation: {c.selfc.get('overall')}")
    L += ["", "## 12. Reproducibility Information"] + table(["Item", "Value"], env_rows(c))
    return "\n".join(L) + "\n"


def build_readme_sections(c, skill_dir, hist, rmeta):
    S = {}
    S["evaluation-methodology"] = ["## Evaluation Methodology"] + methodology()
    S["test-coverage"] = ["## Test Coverage"] + coverage_block(c)
    S["performance"] = ["## Performance"] + perf_block(c)
    base = ["## Baseline Comparison", "", "Without Skill vs With Skill (same evals, model and environment):", ""]
    base += (table(["Metric", "Without Skill", "With Skill", "Delta"], perf_rows(c)) if perf_rows(c) else ["Not measured."]) + ["", tradeoff_line(c)]
    base += [x for x in narrative_blocks(c)]
    S["baseline-comparison"] = base
    S["version-comparison"] = ["## Version Comparison"] + version_block(c)
    S["failure-analysis"] = ["## Failure Analysis"] + failure_block(c)
    S["evaluation-results"] = ["## Evaluation Results", "", "### Per-eval"] + results_table(c) + ["", "### Trigger", ""] + trigger_block(c) + ["", "### Reliability"] + reliability_block(c)
    S["limitations"] = ["## Limitations"] + [f"- {x}" for x in limitations(c)]
    S["reproducibility"] = ["## Reproducibility"] + table(["Item", "Value"], env_rows(c)) + ["", "Re-run with the same model/agent/suite to reproduce; expect run-to-run variation."]
    S["evaluation-history"] = ["## Evaluation History"] + history_block(hist)
    return {k: "\n".join(v) + "\n" for k, v in S.items()}


def build_readme_unmanaged(c, skill_dir, rmeta):
    fm = c.meta.get("frontmatter") or {}
    desc = fm.get("description")
    heads, lic = [], None
    if skill_dir and (Path(skill_dir) / "SKILL.md").exists():
        t = (Path(skill_dir) / "SKILL.md").read_text(encoding="utf-8")
        heads = re.findall(r"^##\s+(.+)$", t, re.M)
        lic = next((p.name for p in Path(skill_dir).glob("LICENSE*")), None)
    files = [f["path"] for f in c.meta.get("files", [])]
    tree = sorted({p.split("/")[0] + ("/" + p.split("/")[1] if p.count("/") >= 2 else "") for p in files if True})
    TODO = "_Not provided by the skill author._ <!-- TODO: author-provided content -->"
    g = lambda k, default=TODO: rmeta.get(k) or default
    S = {}
    S["head"] = [f"# {c.name}", ""]
    S["overview"] = ["## Overview", rmeta.get("overview") or (f"From the skill's own `description` (SKILL.md frontmatter): {desc}" if desc else TODO)]
    S["why"] = ["## Why This Skill Exists", g("why_exists")]
    feats = rmeta.get("features") or ([f"{h}" for h in heads] if heads else None)
    S["features"] = ["## Features"] + ([("Sections documented in SKILL.md (not a claim of tested behavior):" if not rmeta.get("features") else "")] + [f"- {x}" for x in feats] if feats else [TODO])
    S["usage"] = ["## Usage", g("usage")]
    S["configuration"] = ["## Configuration", g("configuration")]
    S["example"] = ["## Example", g("example")]
    reqs = rmeta.get("requirements") or ([f"compatibility: {fm['compatibility']}"] if fm.get("compatibility") else None)
    S["requirements"] = ["## Requirements"] + ([f"- {x}" for x in reqs] if reqs else [TODO])
    S["harnesses"] = ["## Supported Agents / Harnesses", f"Evaluated on: {c.env.get('agent') or 'not recorded'} ({c.env.get('harness') or 'harness not recorded'}), model {c.env.get('model') or 'not recorded'}. Not evaluated elsewhere unless listed in Evaluation History."]
    S["structure"] = ["## Project Structure", "```text"] + [t for t in tree] + ["```"] if tree else ["## Project Structure", TODO]
    S["troubleshooting"] = ["## Troubleshooting", g("troubleshooting")]
    S["license"] = ["## License", rmeta.get("license") or (f"See `{lic}`." if lic else "No license file found in the skill directory.")]
    return {k: "\n".join(v) + "\n" for k, v in S.items()}


def assemble_readme(managed, unmanaged):
    order = ["head", "overview", "why", "features", "evaluation-methodology", "test-coverage", "performance", "baseline-comparison", "version-comparison",
             "failure-analysis", "usage", "configuration", "evaluation-results", "example", "requirements", "harnesses", "limitations", "reproducibility",
             "evaluation-history", "structure", "troubleshooting", "license"]
    out = []
    for k in order:
        if k in managed:
            out.append(f"<!-- skill-eval:begin {k} -->\n{managed[k]}<!-- skill-eval:end {k} -->\n")
        else:
            out.append(unmanaged[k])
    return "\n".join(out)


def update_existing(text, managed):
    replaced, appended = [], []
    for k, body in managed.items():
        rx = re.compile(rf"<!-- skill-eval:begin {k} -->.*?<!-- skill-eval:end {k} -->\n?", re.S)
        block = f"<!-- skill-eval:begin {k} -->\n{body}<!-- skill-eval:end {k} -->\n"
        if rx.search(text):
            text = rx.sub(lambda m: block, text, count=1); replaced.append(k)
        else:
            text = text.rstrip("\n") + "\n\n" + block; appended.append(k)
    return text, replaced, appended


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True); ap.add_argument("--skill"); ap.add_argument("--target-readme")
    ap.add_argument("--readme-meta"); ap.add_argument("--primary-key"); ap.add_argument("--no-history-append", action="store_true")
    ap.add_argument("--history")
    a = ap.parse_args()
    c = Ctx(a.results, a.primary_key)
    out = Path(a.results)
    if not c.perf and not c.tg and not c.struct:
        sys.exit("error: no measured JSON found in results dir; run the pipeline scripts first")
    rmeta = load_json(a.readme_meta, {}) if a.readme_meta else {}
    hist = update_history(c, a.history or (out / "history.json"), not a.no_history_append)

    summary = {"schema_version": 1, "generated_at": now_iso(), "skill": {"name": c.name, "version": c.meta.get("skill_version"), "content_sha256": c.meta.get("content_sha256")},
               "primary_configuration": c.skey, "environment": c.env,
               "headline": {"with_skill": {k: c.cfg[k] for k in ("n_runs_graded", "n_passed", "pass_rate", "pass_rate_ci95_wilson")} if c.cfg else None,
                            "baseline": {k: c.base[k] for k in ("n_runs_graded", "n_passed", "pass_rate", "pass_rate_ci95_wilson")} if c.base else None,
                            "delta_vs_baseline": c.delta, "trigger": c.tg["metrics"] if c.tg else None,
                            "regression": {k: c.reg[k] for k in ("improvements", "regressions", "new_failures", "removed_failures", "regression_rate")} if c.reg else None},
               "not_measured": [n for n, ok in (("structure", c.struct), ("trigger", c.tg), ("functional", c.cfg), ("baseline", c.base), ("reliability", c.cfg and c.cfg["consistency"].get("measured")), ("regression", c.reg)) if not ok],
               "evidence_files": sorted(p.name for p in out.glob("*.json")), "selfcheck": (c.selfc or {}).get("overall")}
    write_json(out / "summary.json", summary)
    (out / "summary.md").write_text(build_summary_md(c), encoding="utf-8")
    (out / "comparison.md").write_text("\n".join([f"# Comparison: {c.name}", "", "## Without Skill vs With Skill"] + (table(["Metric", "Without Skill", "With Skill", "Delta"], perf_rows(c)) if perf_rows(c) else ["Not measured."]) + ["", tradeoff_line(c), "", "## Version comparison"] + version_block(c)) + "\n", encoding="utf-8")
    (out / "failure-analysis.md").write_text("\n".join([f"# Failure Analysis: {c.name}", ""] + failure_block(c, detail=True)) + "\n", encoding="utf-8")
    (out / "benchmark.md").write_text("\n".join([f"# Benchmark: {c.name}", ""] + perf_block(c) + ["## Per-eval"] + results_table(c) + ["", "## Reliability"] + reliability_block(c) + ["", "## Trigger"] + trigger_block(c) + ["", "## Metric definitions"] + [f"- **{k}:** {v}" for k, v in METRIC_DEFS]) + "\n", encoding="utf-8")

    managed = build_readme_sections(c, a.skill, hist, rmeta)
    unmanaged = build_readme_unmanaged(c, a.skill, rmeta)
    if a.target_readme and Path(a.target_readme).exists():
        existing = Path(a.target_readme).read_text(encoding="utf-8")
        if "<!-- skill-eval:begin" in existing:
            new, rep, app = update_existing(existing, managed)
            Path(a.target_readme).write_text(new, encoding="utf-8")
            print(f"updated {a.target_readme}: replaced {rep}, appended {app}")
        else:
            alt = Path(a.target_readme).with_name("README.generated.md")
            alt.write_text(assemble_readme(managed, unmanaged), encoding="utf-8")
            print(f"{a.target_readme} has no skill-eval markers; left untouched. Wrote {alt} for manual merge.")
    else:
        dest = Path(a.target_readme) if a.target_readme else out / "README.md"
        dest.write_text(assemble_readme(managed, unmanaged), encoding="utf-8")
        print(f"wrote {dest}")
    print(f"wrote summary.json, summary.md, comparison.md, failure-analysis.md, benchmark.md in {out}")


if __name__ == "__main__":
    main()
