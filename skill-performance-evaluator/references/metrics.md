# Metrics, Intervals and "Not measured" Rules

## Contents
1. Definitions
2. Intervals and tests used
3. Sample-size guidance
4. Cost vs quality
5. Not measured rules
6. Interpreting small samples

## 1. Definitions (printed in every generated report)
| Metric | Formula / source |
|---|---|
| Pass Rate | graded runs passed / graded runs (a run passes if all assertions pass) |
| Failure Rate | 1 - Pass Rate |
| Skill Lift | skill pass rate - baseline pass rate (percentage points), over evals present in both configurations |
| Assertion pass rate | assertions passed / assertions evaluated (secondary; skill-creator's `pass_rate` convention) |
| Trigger Precision | TP / (TP + FP) |
| Trigger Recall | TP / (TP + FN) |
| Specificity | TN / (TN + FP) |
| F1 | 2TP / (2TP + FP + FN); meaningful only if TP+FP+FN > 0 |
| Reliability | per eval with 2+ runs: always-pass / always-fail / flaky counts |
| Avg / Median runtime | mean / median of `metrics.duration_s` among runs that recorded it |
| Token usage | mean of `metrics.tokens` |
| Tool calls | mean of `metrics.tool_calls` |
| Error count | mean `metrics.errors` per run |
| Artifact success rate | runs with `artifacts_ok` true / runs where recorded |
| Regression rate | evals `regressed` / shared evals between versions |

Population: only `execution_mode: actual` runs that were graded. Excluded runs (`infra_error`, `skipped_unsafe`, simulated, ungraded) are counted and reported, never silently dropped.

## 2. Intervals and tests
- **Wilson score interval (95%)** for every proportion (pass rate, precision, recall). Chosen over the normal approximation because it behaves at 0%, 100% and small n. Treats runs as independent; repeated runs of one eval are correlated, so it is approximate (stated in reports).
- **Eval-level bootstrap CI** (5000 resamples, seed recorded) for skill lift: resamples the *paired per-eval differences*, so it reflects variation across evals. It does not capture run-to-run noise. Not computed with fewer than 5 paired evals.
- **Fisher's exact test** (two-sided) for a per-eval or pooled change between two versions' pass counts. "Statistically supported" means p < alpha (default 0.05). With repeated evals the pooled p treats runs as independent and is flagged approximate.
- **Standard deviation** only when n >= 2 values exist; the report states n. Do not present a stddev from 2 values as a variance estimate.
- No multiple-comparison correction is applied across per-eval tests; with many evals, a few "supported" changes can occur by chance. Say so when listing them.

## 3. Sample-size guidance (Wilson 95% intervals)
| Observed | Interval |
|---|---|
| 3/3 | 44-100% |
| 4/5 | 38-96% |
| 8/10 | 49-94% |
| 16/20 | 58-92% |
| 40/50 | 67-89% |
| 80/100 | 71-87% |
| 10/10 | 72-100% |
| 20/20 | 84-100% |

So: 3 runs show a failure pattern, not a rate; 10 runs on one eval still leaves +-20 pp; to distinguish "80%" from "90%" you need on the order of 100+ runs. Examples of what Fisher can detect: 10/10 vs 5/10 p=0.033; 15/15 vs 8/15 p=0.006; 3/3 vs 1/3 p=0.40 (not supported). Plan runs to the claim you need to make; otherwise phrase findings as observations ("2 of 3 runs failed") not rates.
Defaults: 3 runs/eval/configuration; 5+ for flaky evals; 10-20 only for targeted claims. Suites of ~10-30 evals with 3 runs give useful pooled intervals while keeping cost sane.

## 4. Cost vs quality
Report both with explicit units, side by side, without a verdict:
```
Quality: +10 pp pass rate (82% -> 92%)
Tokens:  +37.5% (8,000 -> 11,000)
```
Then discuss the trade-off for stated use cases (e.g. "worth it if a failed run costs rework; not if latency-bound"). More tokens, tool calls or runtime are not inherently bad; fewer are not inherently good. Higher pass rate alone does not prove overall superiority (check cost, reliability, failure severity, trigger side-effects).

## 5. Not measured rules
- A metric no run recorded is `{"measured": false}` and prints **Not measured** with the reason.
- Never fill a gap with an estimate, average from elsewhere, or a "typical" value.
- Baseline-only or skill-only data -> no delta (print "—"/"N/A").
- Metrics from different run populations are not compared; deltas use paired evals only.
- If everything is "Not measured" for a stage, the executive summary lists the stage under "no data".

## 6. Interpreting small samples
- Report counts with rates ("2/3 runs, 66.7%, CI 21-94%").
- A change "observed" (|delta| >= threshold) is different from "statistically supported"; show both.
- Non-discriminating evals (always pass or always fail in both configurations) are listed; they do not show skill value.
- Flaky evals (mixed results across runs) indicate instability in the skill, the grader, or the model; investigate before trusting aggregate numbers.
