# PHASE-{{PHASE_NUM_PADDED}} — {{PHASE_NAME}}

**Status:** {{PHASE_STATUS}}

## Objective
{{What the system can do / what is proven after this phase.}}

## Why this phase exists
{{Dependency/risk reason it sits here.}}

## Entry criteria
- {{Previous checkpoint passed; required env/tools/decisions resolved (DEC-…).}}

## Dependencies
{{PHASE-… ; external prerequisites}}

## Deliverables
- {{files / components / endpoints / schemas}}

## Acceptance criteria
- [ ] AC-{{PHASE_NUM}}.1 {{observable, testable statement}}

## Verification
{{Which tests/commands prove the acceptance criteria. IDs: TEST-{{PHASE_NUM}}.x-A}}

## Checkpoint
```text
CHECKPOINT PHASE-{{PHASE_NUM_PADDED}}
1. {{command}} → {{expected result}}
2. {{command}} → {{expected result}}
```

## Exit criteria
- Every task COMPLETE; checkpoint passed; HANDOFF.md written; STATE.md updated.

## Risks
{{RISK-… relevant here}}

## Rollback / Recovery
{{How to return to the last known good state (git tag/branch, migration down, flag off, backup).}}
