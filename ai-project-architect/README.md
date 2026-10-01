# 🏗️ AI Project Architect & Phase Planner

[![Antigravity Compatible](https://img.shields.io/badge/Antigravity-Skill-4285F4?logo=google&logoColor=white)](https://github.com/lingjw02/personal-used-skill-library)
[![Claude Compatible](https://img.shields.io/badge/Claude-Code%20%26%20Desktop-D97757?logo=anthropic&logoColor=white)](https://github.com/lingjw02/personal-used-skill-library)
[![Planning: Autonomous Blueprint](https://img.shields.io/badge/Planning-Autonomous%20Execution-blue.svg)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Category: System Architecture](https://img.shields.io/badge/Category-Architecture%20%26%20Roadmap-00897B)](SKILL.md)

Turn a software idea, product requirement, rough specification, or existing codebase into an autonomous, dependency-aware, phase-by-phase implementation blueprint (the `.planning/` directory) that another AI coding agent (Antigravity, Claude Code, Cursor, Codex, Gemini CLI) can execute without stalling.

This is a **pure planning & architecture skill** — it does not write application code. It establishes verifiable requirement IDs, architecture sketches, dependency graphs, phased roadmaps, atomic tasks with concrete validation commands, risk registers, and handoff contracts.

---

## ⚖️ Before & After Comparison

| Factor | ❌ Standard LLM Planning (Ad-hoc Task Checklist) | ✅ Autonomous `ai-project-architect` Blueprint |
|---|---|---|
| **Execution Continuity** | Generates a 20-bullet generic checklist; agent stalls halfway due to missing dependencies | Strict dependency DAG with explicit prerequisite contracts and atomic execution phases |
| **Fact Verification** | Silently hallucinates directory layouts, library versions, and API capabilities | Uses strict **Evidence Labels** (`VERIFIED`, `UNKNOWN`, `ASSUMPTION`, `REQUIRES USER DECISION`) |
| **Task Atomicity** | Bloated tasks ("Build authentication and database"); executor loses context and times out | Single-context tasks (15–30 min execution bounds) each equipped with automated verification commands |
| **Codebase Alignment** | Rewrites architecture from scratch without inspecting existing patterns | Inspects existing repo conventions, manifests, types, and schemas before designing phases |
| **State Tracking** | No persistent tracking; subsequent agent runs lose context of progress | Generates `.planning/STATE.md` and phase manifests with real-time status and handoff contracts |

---

## 🔄 Architectural Planning Pipeline

```mermaid
flowchart TD
    A[Raw Spec / Idea / Existing Codebase] --> B[Phase 0: Research & Discovery]
    B --> C[Phase 1: Requirements Definition<br/>Stable REQ-IDs & Traceability]
    C --> D[Phase 2: Architectural Blueprints<br/>Contracts, Schemas & Boundaries]
    D --> E[Phase 3: Work Decomposition<br/>Phases & Atomic Tasks]
    E --> F[Phase 4: Dependency Graph & Sequencing]
    F --> G[Phase 5: Automated Validation & Quality Gates]
    G --> H[Execution Handoff: .planning/ Blueprint<br/>STATE.md, SPEC.md, TASKS.md]
```

---

## 📂 Repository Structure

```
ai-project-architect/
├── SKILL.md                                  # Core architectural planning protocol
├── README.md                                 # Documentation & phase-planning methodology
├── scripts/
│   ├── init_plan.py                          # Initializes standardized .planning/ directory tree
│   └── validate_plan.py                      # Validates DAG integrity, task IDs & prerequisite links
├── references/
│   ├── architecture.md                       # Architectural sketching & boundary definitions
│   ├── discovery.md                          # Repository inspection & orientation probes
│   ├── execution-handoff.md                  # Handoff contracts for autonomous AI executors
│   ├── phases-and-tasks.md                   # Sizing, atomicity, and phase structure guides
│   ├── quality-gates.md                      # Verification gates and validation command standards
│   ├── requirements.md                       # Stable REQ-ID formats & traceability matrices
│   └── risk-decisions-unknowns.md            # Risk register, ADR templates & unknowns tracking
└── examples/
    └── sample-plan/                          # Worked full .planning/ blueprint example
```

---

## 🚀 Installation & Setup

### For Google Antigravity (AGY)
```bash
# Workspace level
mkdir -p .agent/skills
cp -r ai-project-architect .agent/skills/

# Global level
cp -r ai-project-architect ~/.gemini/antigravity-cli/builtin/skills/
```

### For Claude Code / Claude Desktop / Cursor
```bash
mkdir -p ~/.claude/skills
cp -r ai-project-architect ~/.claude/skills/
```

---

## 💡 Example Trigger Prompts

- *"Break down this multi-tenant SaaS idea into a phase-by-phase `.planning/` implementation blueprint."*
- *"Architect a migration from REST to GraphQL for this codebase before we begin coding."*
- *"Audit our existing PRD and generate atomic, dependency-sequenced tasks with automated validation checks."*
- *"Create a phased roadmap and handoff contract for another AI agent to implement user authentication."*

---

## 📄 License

This skill is distributed under the [MIT License](../LICENSE).
