# Failure Analysis Methodology

## Contents
1. What counts as a significant failure
2. Record fields
3. Failure categories
4. Diagnosis procedure
5. Confidence levels
6. Turning a diagnosis into a recommendation

## 1. Significant failure
Analyze: any eval that fails in the skill configuration in any run, flaky evals, trigger misses/false triggers, evals where the skill is worse than baseline, and baseline-pass/skill-fail pairs. Group repeated failures of one eval into one analysis.

## 2. Record fields (in `results/failures.json`, `diagnosis` filled by you)
`eval_id, configuration, run, prompt, expected_behavior, actual_behavior, failed_assertions[], failure_category, evidence[], diagnosis{likely_cause, cause_confidence, suggested_modification}`.
`actual_behavior` should be a factual description from the transcript/output, not an interpretation.

## 3. Categories
Trigger failure | Instruction ambiguity | Missing instruction | Incorrect reasoning | Tool failure | Missing validation | Context failure (needed info not loaded/retained) | File handling failure | Output formatting failure | Dependency failure | Environment failure | Model limitation | Evaluation limitation (bad/weak assertion, unfair test, grader error).
Use one primary category; mention a secondary one in the evidence if relevant. Check "Evaluation limitation" and "Environment failure" first: a surprising amount of apparent skill failure is a flawed test or a broken sandbox. Environment failures that invalidate the run should be re-run or recorded as `infra_error`.

## 4. Diagnosis procedure
1. Read the transcript, not just the verdict. Find the first step where behavior diverged from expected.
2. Check what the skill actually told the agent at that point (quote the relevant lines) and whether the agent read the referenced file/script.
3. Compare with passing runs of the same eval (flaky) or with the baseline: what differed?
4. Form a hypothesis, then test it where cheap: **minimal-pair rerun** (change one sentence/script/condition in a copy of the skill and rerun the failing eval 3-5 times), **ablation** (remove a section), or **trigger probe** (paraphrase the prompt).
5. Decide the confidence level. Record what you did to reach it.

## 5. Confidence levels
- **Confirmed cause**: a controlled change (minimal pair/ablation) flipped the outcome consistently, or the transcript shows the mechanism explicitly (e.g. the script raised ImportError for a missing module).
- **Likely cause**: transcript evidence consistently points to it and an alternative explanation is implausible, but no controlled test.
- **Possible cause**: plausible from the evidence; other explanations remain. Say what would distinguish them.
Never upgrade confidence for narrative neatness. Evaluator-side explanations ("the model sometimes ignores long instructions") are INFERENCE unless tested.

## 6. From diagnosis to recommendation
Each recommendation must name: the evidence (IDs, rates), the specific change (file/section/sentence/script), the expected effect, and how to verify (which evals to rerun, how many runs, what threshold).
Good: "Trigger recall 62.5% (5/8). Prompts t03, t06, t07 ('audit', 'review', 'check my X') never triggered across 3 runs each (Likely cause: description lacks these verbs). Add them to the description's trigger phrases; rerun trigger evaluation (3 runs) and confirm recall >= the previous 62.5% with no new false triggers on t10-t14."
Bad: "Improve the description."
After the change, rerun the affected evals and report the effect as a version comparison; do not claim the fix worked without that rerun.
