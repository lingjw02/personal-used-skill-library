# Inspection and Intent Extraction (Stages 1-2)

Goal: understand what the target skill is *supposed* to do well enough to design fair tests, without inventing requirements.

## Contents
1. What to inspect
2. Intent template
3. Ambiguity log
4. Inferred criteria
5. Deciding what should and should not be tested

## 1. What to inspect
Read in this order and note facts (with file/line) as you go:
- `SKILL.md`: frontmatter (`name`, `description`), every instruction section, examples, stated constraints, tool/dependency requirements.
- `scripts/`: what each does, inputs/outputs, how SKILL.md tells the agent to call it, error handling, side effects (writes, deletes, network, publish, send).
- `references/`, `assets/`, `examples/`: are they referenced from SKILL.md and when should they be read? Are templates/example outputs usable as oracles for tests?
- `evals/`, `tests/`: existing cases and assertions. Quality-check them (see `test-design.md`).
- `README.md`, `LICENSE`, config, dependency files, previous `results/` or benchmark claims. Existing claims are hypotheses to verify, not facts.
- Version info: `version` in frontmatter/metadata, else the content hash recorded by `init_workspace.py`.

## 2. Intent template (fill in; keep in `results/intent.md` or your notes)
```
Purpose:                one sentence, from SKILL.md's own words
Target users/tasks:     who invokes it, for what
Inputs expected:        file types, formats, user phrasing, size ranges
Outputs expected:       artifacts, formats, structure, naming, where saved
Supported workflows:    numbered list
Required tools/deps:    interpreters, libraries, network, other skills, MCPs
Trigger conditions:     phrases/contexts that SHOULD activate it (from description + body)
Non-trigger conditions: neighbouring tasks that should NOT activate it
Constraints:            "must/never" rules in the skill
Failure conditions:     what the skill says to do on bad input/errors
Side effects/risk:      destructive or external actions
Success criteria:       measurable, each tagged [Stated] or [Inferred criterion]
```

## 3. Ambiguity log
When the skill is vague ("produce a good summary", "handle errors appropriately"), write each ambiguity as: *quoted text -> competing readings -> how it changes the test*. Resolve by (a) asking the user one concise question if the answer changes what "pass" means, or (b) choosing the most literal reading and tagging the resulting criterion **Inferred criterion** in the suite and report. Never silently replace vague text with your own preferences.

## 4. Inferred criteria
Allowed when the skill leaves success undefined, but:
- tag the assertion `"origin": "inferred"` in `evals.json`;
- report the share of assertions that are inferred; if most are, say that the suite measures your interpretation of the skill;
- keep inferred criteria minimal and objective (e.g. "output file exists and opens") before subjective ones.

## 5. What should / should not be tested
Test: behavior the skill claims or implies, each distinct instruction branch, each script entry point, documented edge/error handling, trigger boundaries, and cost-relevant behavior (does it read unneeded references?).
Do not test: things unrelated to the skill's purpose; behavior only a human could judge when no rubric can be written (record as untested); destructive operations you cannot sandbox (record `skipped_unsafe`).
Count unreachable parts: if a script path, reference file, or branch can never be exercised by any test, list it under Test Coverage gaps.
