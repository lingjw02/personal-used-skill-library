# README Generation and Update Rules

## Contents
1. Principle
2. Section map (managed vs author-provided)
3. Update mechanics
4. Forbidden claims
5. Handling missing data
6. Checklist

## 1. Principle
Every performance claim in README.md must come from evaluation results (`results/*.json`). Prose that describes the skill (overview, usage) comes from the skill author or from SKILL.md itself, and is labelled as such. The generator never writes adjectives about quality.

## 2. Section map
README order: Title, Overview, Why This Skill Exists, Features, **Evaluation Methodology**, **Test Coverage**, **Performance**, **Baseline Comparison**, **Version Comparison**, **Failure Analysis**, Usage, Configuration, **Evaluation Results**, Example, Requirements, Supported Agents/Harnesses, **Limitations**, **Reproducibility**, **Evaluation History**, Project Structure, Troubleshooting, License.
Bold = *managed*: generated from JSON, wrapped in `<!-- skill-eval:begin NAME --> ... <!-- skill-eval:end NAME -->`, replaced on every update.
Others = *author-provided*: written once (from `readme-meta.json`, or derived facts such as SKILL.md description, SKILL.md headings, file tree, LICENSE presence), otherwise `_Not provided by the skill author._ <!-- TODO -->`. Never invent them. Ask the user or leave the TODO.

## 3. Update mechanics
- New README: `generate_report.py` writes `results/README.md` (or `--target-readme path`).
- Existing README with markers: only marked blocks are replaced (missing blocks appended at the end); author text is untouched.
- Existing README without markers: left untouched; `README.generated.md` is written next to it for a manual merge (to avoid destroying hand-written content).
- `history.json` gains an entry per (version, suite, date, config); the Evaluation History table is rebuilt from it. Older rows are never edited or removed by the generator.
- Every update regenerates numbers from current JSON; stale numbers cannot persist inside managed blocks.

## 4. Forbidden claims
No "high-quality", "robust", "excellent", "best", "production-ready", "significantly better", "proven", "guaranteed" or any evaluative wording unless a measured figure and interval are cited next to it. No performance claim without a source file. No comparison to other skills unless measured. No statement that something was "tested" if it was static/simulated. `selfcheck.py` flags these and untraceable numbers.

## 5. Handling missing data
Print `Not measured` (with reason where short) or `N/A` (concept doesn't apply, e.g. baseline trigger precision). Empty sections state what is missing and how to obtain it. A README with many "Not measured" cells is acceptable; a README with invented cells is not.

## 6. Checklist before publishing the README
- [ ] `selfcheck.py` shows no errors; warnings reviewed.
- [ ] Reproducibility table complete (model, agent, harness, OS, date, suite version, runs).
- [ ] Execution modes stated; excluded runs disclosed.
- [ ] Limitations mention small-sample caveats and harness limits.
- [ ] No hand-edited numbers inside managed blocks.
