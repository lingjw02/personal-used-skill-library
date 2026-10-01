# Phase 0 — Project Discovery

Goal: replace guesses with evidence. Every finding is written down with its source so the executor never repeats the discovery.

## Contents
1. Order of inspection
2. Reuse search protocol
3. Existing planning conventions
4. Research rule
5. Discovery report format (goes into PROJECT.md §Existing State)

## 1. Order of inspection

Go breadth-first; go deep only where the new work will touch.

1. **Layout** — list the tree 2–3 levels deep (ignore `node_modules`, `.git`, build output, venvs). Identify monorepo/workspaces.
2. **Manifests & toolchain** — `package.json`, lockfiles, `pyproject.toml`/`requirements*.txt`, `Cargo.toml`, `go.mod`, `pom.xml`/`build.gradle`, `Gemfile`, `composer.json`, `Dockerfile`, `docker-compose*`. Record framework + version *as written in the manifest* (VERIFIED) — never from memory.
3. **Commands** — real build/test/lint/typecheck/run commands from scripts sections, `Makefile`, `justfile`, CI workflows. These become validation commands in tasks.
4. **Configuration & environment** — `.env.example`, config modules, feature flags, secrets handling. Never print secret values into the plan.
5. **Architecture signals** — entry points, routing, API layer, service layer, data access, DB schema/migrations/ORM models, auth, state management, UI component library, i18n, background jobs, queues, WebSockets.
6. **Tests** — framework, locations, coverage, fixtures, E2E setup. Run the existing test command only if safe and cheap; record the baseline (pass/fail counts). A failing baseline is a risk the plan must account for.
7. **Docs & agent instructions** — `README`, `docs/`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursor/rules`, `CONTRIBUTING`, ADRs, changelog.
8. **Work in flight** — `TODO`/`FIXME` grep, existing planning files, recent git history, uncommitted changes (do not disturb them).
9. **Deployment** — Dockerfiles, IaC, hosting config, CI/CD, environments.

If you cannot run commands, say so and mark runtime facts `UNKNOWN`.

## 2. Reuse search protocol

Before proposing any new component, search for it:

- grep for domain nouns/verbs (`invoice`, `upload`, `retry`, `auth`) and for the kind of thing (`Button`, `useQuery`, `BaseRepository`, `middleware`).
- find similar features and copy their structure into the plan ("follow `src/features/orders/` layout").
- check installed dependencies that already provide the capability (do not add a second HTTP client / date library / validator).
- record per candidate: path, what it does, fit (REUSE / EXTEND / NOT SUITABLE + reason).

Proposing something new when a reusable equivalent exists requires a `DEC-` entry.

## 3. Existing planning conventions

If any exist (`.planning/`, `docs/plans`, `PLAN.md`, `ROADMAP.md`, `TODO.md`, ADR folders, agent rule files), adopt them. State in PROJECT.md: "Existing convention found: X. This plan maps artifacts as: …". If an active plan already lives in `.planning/`, do not overwrite it — extend it, or mark `REQUIRES USER DECISION` on which to supersede.

## 4. Research rule

Research only what a decision depends on. Source priority: official docs → standards/RFCs → primary repos & maintainer docs → reputable references. Treat tutorials/blogs as non-authoritative; if used for lack of better, label `LOW-CONFIDENCE SOURCE`.

Record references as: `REF-NN | topic | URL | date accessed | what it established | version`. Check current stable version, deprecations, licensing, runtime/hosting limits, rate limits/pricing when cost matters, security advisories for chosen packages. Anything unconfirmed becomes `REQUIRES RESEARCH` with the exact question.

## 5. Discovery report format

```markdown
## Existing State (Discovery)
**Inspected:** <what was actually inspected>   **Not inspected:** <and why>

### What exists            (fact — VERIFIED (path))
### What can be reused     (path — fit — how)
### What must be modified  (path — change — reason)
### What must be created   (component — why nothing existing fits)
### Existing constraints   (framework, conventions, API shapes, DB, hosting …)
### Technical debt & risks (item — impact on this plan — RISK-ID)
### Baseline               (build: pass/fail · tests: N pass / M fail · lint: …) (cmd)
### Commands               build: … test: … lint: … typecheck: … run: …
```

For greenfield projects, replace "What exists" with environment facts (target OS, runtime, available services, hardware such as GPU) and mark unconfirmed ones `UNKNOWN`.
