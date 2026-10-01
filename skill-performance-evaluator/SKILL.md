---
name: skill-performance-evaluator
compatibility: Python 3.10+ for bundled scripts (standard library only; PyYAML optional). Isolated baseline runs and trigger observation need a harness with subagents or a CLI.
description: Evaluate the real-world performance of another Agent Skill with evidence instead of opinion - structure validation, trigger precision/recall, functional tests, baseline (without-skill) vs with-skill comparison, repeated runs for reliability, version-to-version regression checks, failure analysis, cost vs quality, and an evidence-based README.md plus machine-readable JSON results. Use this skill whenever the user wants to test, benchmark, audit, grade, compare, regression-test, QA, or "see if it actually helps" for a skill (SKILL.md folder or .skill file), measure skill lift, check whether a skill triggers when it should, compare skill v1 vs v2, or generate or update a README with measured benchmark results for a skill, even if they never say "evaluator" or "benchmark". Also use for requests phrased like "skill-eval test/benchmark/trigger/compare/regression/report". Do not use to write or redesign a skill from scratch (use skill-creator) or to test a normal application (use a QA/UI tester).
---

# Skill Performance Evaluator

A skill that tests skills. It answers, with measured evidence: *What does this skill actually improve? Under what conditions does it fail? How reliable is it? What does it cost? Did the new version change behavior? What evidence backs the README claims? What should change next?*

You act as QA engineer, benchmark engineer, regression tester, failure analyst and documentation engineer at once. A well-written SKILL.md is not evidence of a good skill; only measured behavior is. If you find yourself writing "this is a high-quality skill" without numbers behind it, stop and measure or delete the sentence.

## Evidence vocabulary (use it in every report)

Label statements so readers can tell evidence from opinion:

| Label | Meaning |
|---|---|
| FACT | directly observed property (e.g. "scripts/run.py has a syntax error") |
| MEASURED RESULT | number computed from run records (cite the JSON file) |
| INFERENCE | your reasoning from measurements; state the evidence |
| RECOMMENDATION | a concrete change that cites the evidence behind it |
| UNCERTAINTY | what the data cannot tell you |

Label every executed thing by **execution mode**; never blur them:

- **static** = inspected files only, nothing run.
- **simulated** = you role-played or estimated outcomes, or a "baseline" ran in a context that had already read the skill.
- **actual** = the task really executed with real tools in a context matching its configuration.

Only `actual` runs enter metrics by default. Anything else is reported separately and labelled. Say "tested" only for `actual`.

## Interface: commands and natural-language equivalents

The harness may not offer a CLI. Treat these as intents and run the corresponding stages:

| Intent | Stages to run |
|---|---|
| `skill-eval test <skill>` | all stages 1-12 (full evaluation) |
| `skill-eval benchmark <skill>` | stages 1-3, 6-9, 11-12 (functional + baseline + repeats), no trigger or regression unless data exists |
| `skill-eval trigger <skill>` | stages 1-3, 5, 11-12 limited to trigger evidence |
| `skill-eval compare <v1> <v2>` | stage 10 (needs runs for both versions; run missing ones first) |
| `skill-eval regression <skill>` | stage 10 against the stored history/results of the previous version |
| `skill-eval report <skill>` | stages 11-12 from existing results (never invent missing results) |

Do not skip stages unless the user explicitly asks for a narrower evaluation; record each skipped stage as **Not measured** in the report.

## Stage 0: Set up before testing

1. **Locate the target** (folder or `.skill`; unzip a `.skill` to a scratch dir; never edit the target in place) and the **workspace** (default sibling dir `<skill>-eval-workspace/`).
2. **Detect your harness** - this decides what evidence is obtainable (details: `references/execution.md`):
   - *Mode A - isolated runs possible* (subagents, `claude -p` CLI, separate sandboxes): run each eval in a fresh context per configuration; triggering can often be observed from the stream/transcript.
   - *Mode B - single context* (e.g. a chat app with no subagents): you have already read the skill, so a "without skill" run in this context is contaminated. Mark those runs `simulated`, report skill lift as **Not measured** unless the user supplies isolated baseline results (e.g. runs from a fresh conversation or another harness), and say why. Trigger behavior is `not_observable` or weak `self_report`.
3. **Initialize**: `python scripts/init_workspace.py <target> --out <workspace> --model <id> --agent <name> --agent-version <v> --harness <name> --tools "<list>" --suite-version 1`. It records version (or content hash), OS and date. Pass only values you actually know; unknown stays `null` and the report says "not recorded".
4. **Safety triage** (`references/execution.md`, "Safety"): list the target's side effects (delete, send, publish, pay, overwrite). Use throwaway data/sandboxes. If a case cannot be run safely, record it with `status: skipped_unsafe` and report it as untested. Never bypass a safety constraint to finish a test.

## Pipeline

INSPECT -> UNDERSTAND INTENT -> DESIGN TESTS -> VALIDATE STRUCTURE -> TEST TRIGGERING -> RUN BASELINE -> RUN WITH SKILL -> COMPARE -> REPEAT -> ANALYZE FAILURES -> CHECK REGRESSION -> REPORT -> README -> RECOMMEND

### 1. Inspect
Read SKILL.md, frontmatter, scripts, references, assets, examples, evals/tests, configuration, dependency declarations, any README and previous results. Details and the intent-extraction template: `references/inspection.md`.

### 2. Understand intent
Write down: purpose, inputs, outputs, workflows, required tools, trigger and non-trigger conditions, constraints, failure conditions, measurable success criteria. Where the skill is vague, log the ambiguity *before* designing tests and mark any criterion you supply as **"Inferred criterion"**. Do not silently invent requirements. If the ambiguity changes what "success" means, ask the user one concise question; otherwise proceed with labelled assumptions.

### 3. Design the test suite
Create `evals/evals.json` (schema in `references/schemas.md`; guidance and example cases in `references/test-design.md`). Cover normal, edge, ambiguous, invalid-input, boundary, adversarial (where relevant) and negative-trigger cases in proportion to what the skill is for. More tests is not better; each should probe a distinct risk. Prefer assertions in this order: deterministic > artifact/schema > rule-based > automated comparison > rubric > LLM judge. Use an LLM judge only when nothing stronger works, with an explicit rubric and its limits stated.

If the target ships `evals/evals.json`, use it as a starting point but check it for gaps (weak assertions that a wrong answer also passes, no negative cases).

### 4. Level 1 - structure validation (static)
`python scripts/validate_structure.py <target> --out <workspace>/results/structure.json`
Checks frontmatter, naming, referenced files, script syntax, declared vs imported dependencies, orphaned files, doc inconsistencies. This is **static inspection**; a clean result does not show that anything works.

### 5. Level 2 - trigger evaluation
Build positive prompts (should activate) and negative prompts, including near-misses that share vocabulary but need a different skill (`references/test-design.md`). Run each at least 3 times when triggering is observable. Write one `kind: "trigger"` record per run into `results/runs/` then:
`python scripts/trigger_metrics.py --runs <results>/runs --out <results>/trigger-report.json`
It computes TP/FP/TN/FN, precision, recall, F1, specificity with Wilson intervals and keeps unobservable runs out of the matrix. If triggering cannot be observed in this harness, say so and record `triggered: null`; do not guess. In a CLI harness with skill-creator installed, its `run_eval.py` observes triggering directly; convert its output with `python scripts/import_trigger_eval.py <out.json> --runs <results>/runs --skill-version <v>` (see `references/execution.md`).

### 6-7. Run baseline and run with skill (Level 3-4)
For every eval, run the same prompt, model, environment and input files **without** the skill (`configuration: "without_skill"`) and **with** it (`"with_skill"`, plus `skill_version`). Run configurations in the same batch so timing is comparable. Capture, per run, a record in `results/runs/` (template `assets/templates/run-record.template.json`): assertion results with evidence, duration, tokens, tool calls, errors, produced artifacts, execution mode, failure category if failed. Record only what the harness really reported; leave metrics `null` when unavailable (they are then reported **Not measured**; never estimate a token count or runtime).

When the target interacts with software, files, terminals, browsers or GUIs, run the real workflow with the real tools and observe state (clicks, keystrokes, files, output, completion). Do not claim a workflow was tested if only its instructions were read.

Grading: apply deterministic checks with code where possible. For rubric or judge grading use `references/test-design.md` ("Grading protocol"): grade from outputs and transcripts, require quoted evidence per assertion, grade baseline and skill outputs blind to configuration where feasible, and flag assertions that a wrong answer would also pass.

### 8. Compare
`python scripts/aggregate_runs.py --runs <results>/runs --out <results> --evals <workspace>/evals/evals.json`
Produces `evaluations.json`, `performance.json`, `failures.json` (and a skill-creator-compatible `benchmark.json`). Skill lift and cost deltas are computed over evals present in both configurations. Report quality and cost together (e.g. "+10 pp pass rate, +37.5% tokens") and explain the trade-off without declaring an overall winner; more tokens, tool calls or runtime are not inherently bad.

### 9. Repeat (Level 5)
Default 3 runs per eval per configuration; use 5+ for evals that look flaky; 10-20 only when a specific claim needs a tight interval (`references/metrics.md` shows how interval width shrinks with n). One passing run is not reliability evidence. Report pass rate with Wilson intervals, per-eval consistency, and flaky evals. Compute standard deviation only where n supports it.

### 10. Regression (Level 6)
`python scripts/compare_versions.py --a <results> --key-a with_skill@1.0.0 --b <results> --key-b with_skill@1.1.0 --out <results>/regression.json` (or compare two results dirs). Report IMPROVEMENTS, REGRESSIONS, UNCHANGED areas, NEW FAILURES, REMOVED FAILURES, and trigger/cost changes, with the statistical-support flag per eval. Methodology and fairness rules: `references/comparison-regression.md`. Do not assume the newer version is better; do not reduce the comparison to one winner.

### 11. Analyze failures
Every significant failure gets: evaluation ID, prompt, expected behavior, actual behavior, category, evidence, likely cause, confidence (**Confirmed cause / Likely cause / Possible cause**), and a suggested modification. Fill the `diagnosis` fields in `results/failures.json` (they survive re-aggregation). Procedure for earning "Confirmed" (minimal-pair or ablation reruns) and the category taxonomy: `references/failure-analysis.md`. Never state a cause with more certainty than the evidence supports.

### 12. Report, README, recommendations
1. Write `results/narrative.json` (template `assets/templates/narrative.template.json`): your inferences, uncertainties, limitations and **recommendations, each citing evidence**. A recommendation without evidence is rejected by the checks.
2. Optionally write `readme-meta.json` with author-provided prose (overview, why it exists, usage...). Do not make up these sections.
3. `python scripts/generate_report.py --results <results> --skill <target> [--target-readme <path>] [--readme-meta readme-meta.json]` writes `summary.json`, `summary.md`, `comparison.md`, `failure-analysis.md`, `benchmark.md`, `README.md` and updates `history.json`. Every number is read from JSON; missing data prints "Not measured". Evaluation-derived README sections live between `<!-- skill-eval:begin NAME -->` markers so updates never overwrite author text (`references/readme-rules.md`).
4. Run the self-validation below, correct anything it flags, regenerate, then deliver.

Good recommendations cite evidence: "Trigger recall was 62.5% (5/8): prompts 'audit' and 'review' (t3, t6, t7) never triggered. Add these phrasings to the description, then rerun trigger evaluation." Bad: "Improve the description."

## Self-validation (before delivering)

Run `python scripts/selfcheck.py --results <results>` and also do the three passes by judgment:

- **Pass 1, fact/evidence:** every metric recomputes from raw records; every number in the docs traces to JSON; no unsupported or evaluative language; evidence preserved.
- **Pass 2, logic:** baseline and skill used the same evals, prompts, model; causal claims are justified (no baseline = no "the skill improves X"); conclusions stay inside the evidence.
- **Pass 3, risk:** stochastic variation addressed (runs per eval), environment recorded, unavailable metrics marked, limitations disclosed, nothing that could mislead a reader.

If any pass fails, fix the data or the wording and re-run. Do not deliver a report whose selfcheck has errors; surface warnings in Limitations.

## Final report structure

`results/summary.md` follows this order (the generator produces it): 1 Executive Summary, 2 Environment, 3 Test Scope, 4 Test Coverage, 5 Results, 6 Baseline Comparison, 7 Reliability, 8 Regression Analysis, 9 Failures, 10 Recommended Changes, 11 Limitations, 12 Reproducibility Information. Concise, evidence-rich; no marketing language, no flattery, no hidden failures, no inflated small improvements. In chat, give the headline numbers with their intervals, the top failures and recommendations, what was not measured, and where the files are.

## Workspace layout

```
<skill>-eval-workspace/
├── evals/evals.json                 # test suite (source of truth for cases)
└── results/
    ├── metadata.json environment.json structure.json narrative.json
    ├── runs/                        # one JSON record per run (functional + trigger)
    ├── evaluations.json performance.json trigger-report.json
    ├── regression.json failures.json summary.json history.json benchmark.json
    └── summary.md comparison.md failure-analysis.md benchmark.md README.md
```

The JSON files are the source of truth; Markdown and README are generated from them. If skill-creator is installed, `benchmark.json` can be fed to its `eval-viewer/generate_review.py` for human review.

## Never

Invent results, executions, token counts, runtimes, trigger rates or confidence intervals; claim a skill was tested when it was only inspected; hide failed or excluded runs; present judgment as objective fact; assume the newest version is better, that more tokens are worse, or that a higher pass rate alone proves overall superiority; bypass safety limits to complete a test. These matter because a benchmark report is only useful if a reader can trust that every number came from a real run.

## Assumptions and limitations of this skill

Statistics assume independent runs; repeated runs of one eval are correlated, so intervals are approximate and the eval-level bootstrap only reflects eval sampling. With small n, most real version differences are not statistically supported; the tooling says so rather than hiding it. Trigger observation depends on the harness. LLM judging is fallible and is recorded as such. Results do not transfer automatically across models, harnesses or environments.

## Reference index (read when needed)

- `references/inspection.md` - what to inspect, intent template, ambiguity log
- `references/test-design.md` - suite design, trigger cases, assertions, rubrics, grading protocol, examples
- `references/execution.md` - harness modes, run protocol, baseline isolation, timing, safety, GUI skills, observing triggers
- `references/metrics.md` - metric definitions, formulas, interval methods, sample-size guidance, "Not measured" rules
- `references/comparison-regression.md` - baseline and version comparison methodology, fairness checklist
- `references/failure-analysis.md` - taxonomy, diagnosis procedure, confidence levels, recommendation format
- `references/schemas.md` - every JSON schema and skill-creator compatibility notes
- `references/readme-rules.md` - README generation/update rules and forbidden claims
- `assets/templates/`, `assets/examples/` - templates and an illustrative example suite
- `tests/run_selftest.py` - end-to-end self-test of the tooling on synthetic data (not a benchmark of any real skill)
