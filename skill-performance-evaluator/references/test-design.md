# Test Design, Assertions, Rubrics and Grading (Stage 3, 6-7)

## Contents
1. Suite design principles
2. Test case schema
3. Trigger case design
4. Assertion hierarchy
5. Rubric templates (only when needed)
6. LLM judge protocol
7. Grading protocol
8. Example cases (illustrative)

## 1. Principles
- Coverage reflects the skill's purpose. Map every test to a risk or instruction branch; delete tests that probe nothing new.
- Balance: normal, edge, ambiguous, invalid-input, boundary, adversarial (only where the skill handles untrusted or tricky input), and negative-trigger cases.
- Realistic prompts: write how a real user would (typos, context, casual tone, file paths), not clean textbook instructions.
- Discriminating assertions: an assertion is weak if a wrong or generic answer also passes. For each assertion ask "what would a confidently wrong output look like, and does this catch it?" Add checks for correctness, not just presence ("file exists" is a floor).
- Keep tests independent and repeatable; provide input files under `evals/files/`.
- Prefer a mix of difficulties so that baseline is not at 0% or 100% everywhere; a suite where both configurations always pass or always fail cannot show lift. Report such evals as "non-discriminating" rather than dropping them silently.

## 2. Test case schema
Fields (full JSON schema in `schemas.md`):
`id, kind (functional|trigger), category, difficulty, prompt, expected_behavior, assertions[], input_files[], expected_artifacts[], positive_or_negative, expected_trigger, tags[]`.
Each assertion: `{"text", "method": "deterministic|artifact|schema|rule|comparison|rubric|llm_judge", "check": "<code/command/regex if automatable>", "origin": "stated|inferred"}`.
Compatibility: skill-creator's `evals.json` (`expected_output`, `expectations`) is accepted; `expected_output` maps to `expected_behavior`.

## 3. Trigger case design
Positive prompts (should trigger): direct requests; indirect/implicit requests that never name the skill's topic word; casual or abbreviated phrasing; requests embedded in a larger task; prompts using synonyms ("audit", "review", "check") for the core verb.
Negative prompts (should not trigger): **near-misses** that share keywords but belong elsewhere (adjacent domain, a different file format, a conceptual question about the topic, a request for a different deliverable); plain unrelated tasks; prompts for a competing skill. Easy negatives inflate specificity; most should be near-misses.
Aim for at least 8-10 positive and 8-10 negative prompts; run each 3+ times when observable. Write each as a trigger record (`kind: "trigger"`).
Observability reminder: record `observation_method` (`cli_stream`, `transcript_skill_read`, `self_report`, `not_observable`). If unobservable, record `triggered: null`.

## 4. Assertion hierarchy (strongest first)
1. Deterministic assertion in code (exit code, string/regex, numeric tolerance, row counts).
2. Exact artifact validation (file opens, page/slide/sheet counts, checksum vs golden file).
3. Schema validation (JSON schema, required headings/fields, XML validity).
4. Rule-based checks (forbidden phrases absent, ordering, length bounds, required citations).
5. Automated comparison (diff vs reference, similarity with stated threshold - say that thresholds are arbitrary).
6. Rubric scoring (below).
7. LLM judge (below), last resort.
When a check can be automated, write the script into `evals/checks/` and cite it in the assertion's `check`.

## 5. Rubric templates
Use only when the dimension truly needs graded judgment; define anchors so two graders agree. Don't compute one blended "overall score"; report dimensions separately, or use a pass threshold you justify.
```
Correctness (0-3):  0 incorrect | 1 partially correct | 2 mostly correct | 3 fully correct
Completeness (0-3): 0 major omissions | 1 several omissions | 2 minor omissions | 3 complete
Instruction compliance (0-3): 0 ignored | 1 partial | 2 mostly compliant | 3 fully compliant
```
Add task-specific anchors ("3 = all five required sections present AND each cites a source row"). A rubric dimension is `passed` when score >= the threshold stated in the assertion.

## 6. LLM judge protocol
- Provide: the rubric with anchors, the task prompt, the output (and transcript if relevant), and ask for a score plus **quoted evidence** per dimension.
- Blind the judge to configuration (do not say which output used the skill); randomize order in pairwise comparisons.
- Preserve the judge's reasoning in the assertion `evidence` field.
- Limits to state in the report: judge is a model with its own biases (length, position, style), can be wrong, shares blind spots with the executor if it is the same model. Spot-check a sample of judgments by hand and report agreement if you did.
- Never let the judge's verdict override a deterministic check.

## 7. Grading protocol
1. Run deterministic checks first and record their evidence (command + output excerpt).
2. For remaining assertions, read the transcript and inspect output files directly (do not trust the executor's own claims that it succeeded).
3. Each assertion gets `passed` true/false and **evidence** (quote or file/line). No evidence, no pass.
4. If you notice an assertion that is trivially satisfied, or an important outcome nothing checks, record it in the failure analysis as an *Evaluation limitation* and propose a stronger assertion.
5. A run `passed` only if all its assertions passed, unless the suite states otherwise.

## 8. Example cases (illustrative, for a hypothetical CSV-summary skill)
```json
{"id":"f03","kind":"functional","category":"edge","difficulty":"hard",
 "prompt":"here's sales.csv (semicolon separated, european decimals). give me totals per region as a short md report",
 "expected_behavior":"Detects ';' delimiter and ',' decimals; totals per region correct; report is Markdown",
 "assertions":[
  {"text":"report.md exists","method":"artifact","check":"test -f report.md","origin":"stated"},
  {"text":"North total equals 1234.50","method":"deterministic","check":"grep -q '1234.50' report.md","origin":"inferred"}],
 "input_files":["evals/files/sales_semicolon.csv"],"positive_or_negative":"positive","tags":["delimiter","locale"]}
{"id":"t07","kind":"trigger","prompt":"explain how CSV quoting works","expected_trigger":false,
 "positive_or_negative":"negative","category":"near-miss"}
```
