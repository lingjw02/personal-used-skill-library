# JSON Schemas

All files live under `results/` unless noted. JSON is the source of truth for measured metrics; Markdown and README are generated from it. Unknown/unavailable values are `null` or `{"measured": false}`, never guessed.

## Contents
1. evals.json (suite)
2. Run record (functional)
3. Run record (trigger)
4. metadata.json / environment.json
5. evaluations.json
6. performance.json
7. trigger-report.json
8. regression.json
9. failures.json
10. narrative.json / readme-meta.json
11. history.json / summary.json / selfcheck.json
12. skill-creator compatibility

## 1. evals.json (`evals/evals.json`)
```json
{"skill_name":"x","suite_version":"1","evals":[
 {"id":"f01","kind":"functional","category":"normal","difficulty":"easy",
  "prompt":"...","expected_behavior":"...",
  "assertions":[{"text":"...","method":"deterministic","check":"test -f out.md","origin":"stated"}],
  "input_files":["evals/files/a.csv"],"expected_artifacts":["out.md"],
  "positive_or_negative":"positive","tags":["edge"]},
 {"id":"t01","kind":"trigger","prompt":"...","expected_trigger":true,"positive_or_negative":"positive","category":"direct"}]}
```
`id` unique string. `method` in deterministic|artifact|schema|rule|comparison|rubric|llm_judge. `origin` stated|inferred ("Inferred criterion").

## 2. Run record (functional) - `results/runs/*.json` (one object, a list, or `.jsonl`)
```json
{"kind":"functional","eval_id":"f01","configuration":"with_skill","skill_version":"1.0.0","run":1,
 "prompt":"exact text run","model":"...","execution_mode":"actual","status":"completed",
 "assertions":[{"text":"...","passed":true,"method":"deterministic","evidence":"stdout: ..."}],
 "passed":null,"artifacts_ok":true,
 "metrics":{"duration_s":41.2,"tokens":9120,"tool_calls":7,"errors":0},
 "actual_summary":"what happened, factually",
 "failure":{"category":"Missing validation","evidence":["..."]}}
```
- `configuration`: `with_skill` | `without_skill` (`skill_version` required for multi-version work).
- `execution_mode`: `actual` | `simulated` | `static`. `status`: `completed|error|timeout|infra_error|skipped_unsafe`.
- `passed`: if null, derived from assertions (all passed). `metrics.*`: null/absent when not reported.
- Include the exact `prompt` so the selfcheck can verify baseline/skill parity.

## 3. Run record (trigger)
```json
{"kind":"trigger","eval_id":"t01","run":1,"prompt":"...","expected_trigger":true,"triggered":true,
 "observation_method":"cli_stream","skill_version":"1.0.0"}
```
`triggered: null` = not observable. `observation_method`: cli_stream | transcript_skill_read | self_report | not_observable.

## 4. metadata.json / environment.json (from `init_workspace.py`)
metadata: `skill_name, skill_version, version_source, content_sha256, files[], frontmatter{}, suite_version, target_path`.
environment: `evaluation_date, model, agent, agent_version, harness, os, machine, python, available_tools[], runs_per_eval_planned, suite_version, notes` (null = not recorded).

## 5. evaluations.json
`{"evals":[{"eval_id","category","difficulty","prompt","expected_behavior","configs":{"<config key>":{"n_runs","n_passed","pass_rate","pass_rate_ci95_wilson","flaky","assertion_pass_rate","time_seconds":{stats},"tokens":{stats},"tool_calls":{stats}}}}]}`
Config keys: `without_skill`, `with_skill`, or `with_skill@<version>`. Stats object: `{"measured":true,"n","mean","median","min","max","stddev"}` or `{"measured":false,"n":0}`.

## 6. performance.json
`configurations{<key>:{n_runs_graded,n_evals,n_passed,pass_rate,failure_rate,pass_rate_ci95_wilson,eval_level_mean_pass_rate,min_runs_per_eval,consistency,assertion_pass_rate,time_seconds,tokens,tool_calls,errors_per_run,artifact_success,execution_modes,excluded_runs}}`, `deltas_vs_baseline{<key>:{paired_evals,baseline_pass_rate,skill_pass_rate,skill_lift_pp,eval_level_mean_lift_pp,eval_level_lift_ci95_bootstrap_pp,time_seconds{baseline_mean,skill_mean,relative_change},tokens{...},tool_calls{...}}}`, `warnings[]`, `load_errors[]`.

## 7. trigger-report.json
`by_version{<ver>:{confusion{tp,fp,tn,fn},metrics{precision,recall,specificity,f1,accuracy: {measured,value,ci95_wilson,denominator|reason}},per_case[],missed_positive_cases[],false_trigger_cases[],inconsistent_cases[],observation_methods{},unobservable_records,limitations[]}}`.

## 8. regression.json
`a{key,skill_version}, b{...}, thresholds, fairness{same_suite_version,same_model,shared_evals,only_in_a,only_in_b}, aggregate{pass_rate,time_seconds,tokens,tool_calls}, trigger{precision,recall,f1}, per_eval[{eval_id,a,b,delta_pass_rate,classification,statistically_supported,fisher_p}], improvements[], regressions[], unchanged[], insufficient_data[], new_failures[], removed_failures[], failure_categories{new_in_b,removed_in_b,persisting}, regression_rate, warnings[]`.

## 9. failures.json
`failures[{eval_id,configuration,run,prompt,expected_behavior,actual_behavior,failed_assertions[],status,failure_category,evidence[],diagnosis{likely_cause,cause_confidence,suggested_modification}}]`. `cause_confidence` in {"Confirmed cause","Likely cause","Possible cause"}; null = undiagnosed. Re-running `aggregate_runs.py` keeps existing `diagnosis` and `failure_category` for matching (eval, config, run).

## 10. narrative.json / readme-meta.json (analyst-authored)
narrative: `{"inferences":[{"text","evidence":["performance.json"]}],"uncertainties":["..."],"limitations":["..."],"recommendations":[{"id":"R1","text":"...","evidence":["failures.json: f03"],"verification":"rerun f03 x5"}]}`. Recommendations/inferences without `evidence` are omitted/flagged.
readme-meta: `{"overview","why_exists","features":[],"usage","configuration","example","requirements":[],"troubleshooting","license"}` (author-provided prose only).

## 11. history.json / summary.json / selfcheck.json
history: `entries[{run_id,date,skill_version,suite_version,model,agent,n_runs_graded,pass_rate,pass_rate_ci95,precision,recall,avg_tokens,avg_runtime_s}]`. summary: headline metrics + `not_measured[]` + `evidence_files[]`. selfcheck: `overall` and three `passes` (fact, logic, risk) with findings.

## 12. skill-creator compatibility
Accepts skill-creator `evals/evals.json` (`expected_output`, `expectations`). `aggregate_runs.py` also writes `benchmark.json` in skill-creator's schema (`configuration` is exactly `with_skill`/`without_skill`, `result.pass_rate` is the per-run *assertion* pass rate) so `eval-viewer/generate_review.py` can display it. `scripts/import_trigger_eval.py` converts its `run_eval.py` output. Task pass rate (all assertions) is this skill's primary metric; do not mix the two in one table.
