# Baseline and Version Comparison Methodology

## Contents
1. Baseline vs skill
2. Version vs version
3. Fairness checklist
4. Classification rules
5. Reading a regression report

## 1. Baseline vs skill
- Pair at the eval level. Only evals with graded runs in both configurations enter the delta (others are listed).
- Same prompts, model, environment, tools, input files, run counts.
- Report: pass rate for each, lift in pp, eval-level bootstrap CI (if >= 5 paired evals), relative change in tokens/runtime/tool calls, non-discriminating evals, evals where the skill did worse (a skill can lower the pass rate on some evals).
- Do not call the skill "effective" or "ineffective" in general; state which kinds of evals improved/regressed and by how much, and what was not covered.
- Failure patterns of the baseline also matter: they show what the skill is actually fixing (or not).

## 2. Version vs version
Inputs: runs for version A and B under identical suite, model and environment (A may be historical; reuse A's recorded runs only if suite and model match, otherwise re-run A).
Run `scripts/compare_versions.py` (see SKILL.md stage 10). It produces:
- per-eval pass counts, delta, Fisher p, classification
- aggregate pass rate, tokens, runtime, tool calls, trigger precision/recall/F1 deltas
- lists: IMPROVEMENTS, REGRESSIONS, UNCHANGED, NEW FAILURES, REMOVED FAILURES; failure categories new/removed/persisting
- regression rate, fairness block and warnings

## 3. Fairness checklist (verify before concluding anything)
- [ ] Same test suite version (`metadata.suite_version`), same eval ids and prompts.
- [ ] Same model and agent/harness; same tool configuration.
- [ ] Same number of runs per eval (or note the difference).
- [ ] Both sides executed in `actual` mode.
- [ ] Skill content differences between versions are known (diff the two skill dirs; hashes are in `metadata.json`) so you can relate behavior changes to specific edits instead of guessing.
- [ ] If anything above fails, state that differences may reflect the setup, not the skill.

## 4. Classification rules (defaults, adjustable)
- `improved` / `regressed`: |delta pass rate| >= `--min-delta` (default 0.2). `unchanged` otherwise. `insufficient_data` if a side has no graded runs.
- `statistically_supported`: Fisher p < `--alpha` (default 0.05). Most per-eval changes at 3 runs are not supported; say so, and propose more runs on those evals instead of over-interpreting.
- NEW FAILURE: A passed all runs, B failed at least one. REMOVED FAILURE: A failed at least one, B passed all.
- Trigger changes: compare precision/recall/F1 with intervals; a recall gain with a precision loss is a trade-off, not a win.

## 5. Reading a regression report
1. Check fairness warnings first.
2. Look at regressions and new failures before improvements (they are what users will notice).
3. Relate each notable change to a specific diff in the skill (a changed sentence, a new script) as an INFERENCE, with confidence per `failure-analysis.md`.
4. Report cost changes next to quality changes.
5. Never reduce the comparison to one winner; list what improved, regressed, stayed the same, and what remains uncertain.
6. Append the evaluation to `history.json` (done by `generate_report.py`); explain changes between rows rather than just listing them.
