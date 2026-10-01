# 🧪 Software QA Tester — Autonomous Functional QA & Bug Reproduction

[![Antigravity Compatible](https://img.shields.io/badge/Antigravity-Skill-4285F4?logo=google&logoColor=white)](https://github.com/lingjw02/personal-used-skill-library)
[![Claude Compatible](https://img.shields.io/badge/Claude-Code%20%26%20Desktop-D97757?logo=anthropic&logoColor=white)](https://github.com/lingjw02/personal-used-skill-library)
[![Testing: Evidence-Backed](https://img.shields.io/badge/Testing-Evidence--Backed%20QA-red.svg)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Category: Functional Testing](https://img.shields.io/badge/Category-System%20QA%20%26%20Verification-C2185B)](SKILL.md)

Operate and test running software applications like a professional human QA engineer: launching services, clicking through workflows, submitting forms, inspecting console logs and network traffic, and reporting reproducible bugs with evidence files, severity ratings, root-cause diagnostics, and verification retests.

Equipped with `qa_tracker.py` to maintain an immutable audit trail and state machine so no feature is ever claimed "tested" or "passed" without captured runtime proof.

---

## ⚖️ Before & After Comparison

| Factor | ❌ Standard LLM Testing (Code Assumption / Guessing) | ✅ Autonomous `software-qa-tester` Protocol |
|---|---|---|
| **Proof Standard** | Claims code "looks good" by skimming function bodies in source files | Zero trust in unexecuted code; features only pass when directly exercised in running runtime |
| **Bug Reproduction** | Vague descriptions ("sometimes login fails"); no verifiable steps | Step-by-step reproduction records with network logs, screenshots, and exact input payloads |
| **State Machine** | Loses track of which features passed, failed, or were blocked | Tracked via `qa_tracker.py` state machine (`UNTESTED` → `IN_PROGRESS` → `PASSED` / `FAILED` / `BLOCKED`) |
| **Retest Discipline** | Marks issues resolved the moment a code diff is submitted | Requires an explicit retest against the running system to verify fix and detect regressions |
| **Safety & Secrets** | Risk of destructive actions against live databases or credentials leakage | Safe by default: treats unknown envs as production, isolates test data, redacts tokens and passwords |

---

## 🔄 Autonomous QA Testing Protocol

```mermaid
flowchart TD
    A[Step 0: Capability Tier & Environment Discovery<br/>A: Computer-Use | B: Browser | C: Terminal | D: Static] --> B[Step 1: Feature Inventory & Tracker Init<br/>qa_tracker.py init]
    B --> C[Step 2: Risk-Ordered Test Execution<br/>Smoke, Happy Path & Boundary Conditions]
    C --> D[Step 3: Anomaly Isolation & Reproduction<br/>Capture Logs, Network Requests & Screenshots]
    D --> E[Step 4: Root Cause Hypothesis & Bug Filing<br/>qa_tracker.py log-bug]
    E --> F[Step 5: Developer Fix Handoff & Smallest Patch Recommendation]
    F --> G[Step 6: Retest & Regression Verification<br/>qa_tracker.py retest]
```

---

## 📂 Repository Structure

```
software-qa-tester/
├── SKILL.md                                  # Core functional QA protocol & execution methodology
├── README.md                                 # Documentation & QA testing guide
├── scripts/
│   └── qa_tracker.py                         # CLI audit log & state tracker for features, bugs & retests
├── references/
│   ├── discovery.md                          # App discovery probes, route mapping & service launch
│   ├── evidence-and-bugs.md                  # Standards for reproduction steps, screenshots & logs
│   ├── report.md                             # Formats for QA summary, feature matrices & bug records
│   ├── retest.md                             # Protocol for verifying patches and avoiding false fixes
│   ├── safety-and-data.md                    # Environment classification, destructive guards & redaction
│   └── test-techniques.md                    # Boundary values, state forcing, concurrency & fault injection
├── assets/
│   ├── created-data-template.md              # Template to track test records for cleanup
│   └── summary-template.md                   # Executive QA summary template
└── examples/
    └── sample-run/                           # Complete worked example with logs, evidence & bug reports
```

---

## 🚀 Installation & Setup

### For Google Antigravity (AGY)
```bash
# Workspace level
mkdir -p .agent/skills
cp -r software-qa-tester .agent/skills/

# Global level
cp -r software-qa-tester ~/.gemini/antigravity-cli/builtin/skills/
```

### For Claude Code / Claude Desktop / Cursor
```bash
mkdir -p ~/.claude/skills
cp -r software-qa-tester ~/.claude/skills/
```

---

## 💡 Example Trigger Prompts

- *"Launch and smoke-test our local Web API on http://127.0.0.1:8000 and log any endpoint failures."*
- *"Test our shopping cart checkout flow for edge cases (empty cart, invalid card, double-submit).*
- *"Reproduce this reported authentication bug, capture network traces, and file a verified bug report."*
- *"Verify whether the recent bug fix in PR #42 actually resolved the issue without causing regressions."*

---

## 📄 License

This skill is distributed under the [MIT License](../LICENSE).
