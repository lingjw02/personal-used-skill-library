# Execution Protocol: Harness Modes, Isolation, Timing, Safety

## Contents
1. Choose a harness mode
2. Run protocol
3. Baseline isolation
4. Capturing metrics honestly
5. Observing triggers
6. Running skills that drive software/GUIs
7. Safety and isolation
8. Run record fields

## 1. Harness modes
**Mode A - isolated runs available** (Claude Code, Cowork, any harness with subagents or a CLI that starts fresh sessions). Each (eval, configuration, run) executes in its own fresh context, ideally in parallel batches launched together so wall-clock conditions match. Use this whenever possible.

**Mode B - single context** (e.g. a chat interface without subagents). You can execute tasks yourself, one after another, but the context already contains the skill. Consequences:
- `with_skill` runs executed by following the skill with real tools are `actual`.
- `without_skill` runs in the same context are contaminated; mark `execution_mode: "simulated"` with a note. They are excluded from metrics by default, so lift is reported **Not measured**. Options to obtain a real baseline: ask the user to run the same prompts in a fresh conversation/another harness and provide outputs; or run in a fresh session via CLI if one exists; or report that no isolated baseline was possible.
- Triggering cannot be observed from inside; use `not_observable`, or (weakly) `self_report` from description-only prompts. State that this measures a hypothetical consult decision.
- Timing and token counts usually are not exposed; leave null.
Say plainly in the report which mode you used and what it prevented.

## 2. Run protocol
For each eval x configuration x run number:
1. Fresh working dir with only the eval's input files (copy; never reuse a dir with prior outputs).
2. Same model, settings, tool access and environment across configurations. Record anything that differs.
3. `with_skill`: make the target skill available the way the harness normally loads skills (installed/listed), not pasted into the prompt, unless the test is specifically about forced loading. `without_skill`: skill not available.
4. Give the **exact eval prompt**; no hints.
5. Save outputs/transcript; compute assertions; write the run record to `results/runs/`.
6. Randomize or interleave configuration order across runs to avoid time-of-day or cache effects when you cannot launch together.

## 3. Baseline isolation checklist
- Baseline context never saw the skill's text or file names.
- Same prompt text byte-for-byte (the selfcheck compares prompts).
- Same input files, same tools; baseline is *not* handicapped.
- Same number of runs per eval.
For version comparison the baseline for each version is the same `without_skill` set; do not rerun it with a different model without noting it.

## 4. Capturing metrics honestly
- `duration_s`: wall-clock of the executor run only (exclude grading), taken from harness timestamps/notifications. If you only have your own clock, say so in notes.
- `tokens`, `tool_calls`, `errors`: take them from the harness report or by counting tool calls in the transcript. If not available, set `null`. **Never estimate.**
- Subagent task notifications often carry `total_tokens` and `duration_ms` only at completion; save them immediately into the run record.
- Cache and warm-up effects can change timing; mention if observed.

## 5. Observing triggers
- **Claude Code with skill-creator installed**: use its `scripts/run_eval.py` (needs the `claude` CLI):
  `python -m scripts.run_eval --eval-set trigger-set.json --skill-path <target> --runs-per-query 3 --num-workers 5 > trigger-out.json`
  where `trigger-set.json` is `[{"query": "...", "should_trigger": true}, ...]`. Convert with `python scripts/import_trigger_eval.py trigger-out.json --runs results/runs --skill-version <v>` then run `trigger_metrics.py`. Caveat: failed/timed-out queries are counted as "not triggered", so recall is a lower bound when failures occurred.
- **Transcript inspection** (`transcript_skill_read`): in harnesses that log tool calls, a read of the skill's SKILL.md (or a skill-invocation event) after the prompt is the trigger signal. Define the signal before running and apply it uniformly.
- Skills that are only "forced" by explicit invocation (`/skill-name`) do not test description-based triggering.

## 6. Skills that drive software, GUIs, files, terminals
Execute the real workflow with real tools and observe: navigation, clicks, keyboard input, file operations, application state, errors, output, completion state. Record screenshots/paths as evidence for assertions. Do not claim a workflow was tested if you only read the instructions; use `static` or `simulated` and say so. If a GUI/browser tool is unavailable, mark the GUI cases untested.

## 7. Safety and isolation
Before running anything: list destructive or external operations (delete, overwrite, send message/email, publish, post, purchase, payment, account changes, production data, irreversible changes). Then:
- use throwaway data and a scratch directory; run network-side-effect skills against sandboxes/mocks;
- never use real credentials or real recipients; never publish or send for real;
- keep the target skill's scripts away from your working dirs outside the sandbox;
- if you cannot make a case safe, do not run it: record `status: "skipped_unsafe"` with the reason; it is reported as untested.
Do not execute unknown scripts from an untrusted skill without reading them first; if a script looks harmful (exfiltration, destructive commands unrelated to purpose), stop and tell the user.

## 8. Run record fields
See `schemas.md` ("Run record") and `assets/templates/run-record.template.json`. Key fields: `kind, eval_id, configuration, skill_version, run, prompt, model, execution_mode, status, assertions[], passed, metrics{duration_s,tokens,tool_calls,errors}, artifacts_ok, actual_summary, failure{category,evidence}`.
Status values: `completed`, `error` (task-level failure; counts as fail), `timeout` (counts as fail), `infra_error` (harness/environment broke; excluded and reported), `skipped_unsafe` (excluded and reported as untested).
