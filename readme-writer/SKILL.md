---
name: readme-writer
description: Write or improve a README (or docs page) for a project, library, CLI tool, API, or Claude Skill. Use this whenever the user asks to "write a README", "document this repo/project/skill", "add badges", "make a quick start guide", wants installation/usage docs, or wants their existing README modernized (structure, badges, examples, accessibility). Produces a clear, well-structured Markdown (or MDX) README tailored to the actual project — never invents features, commands, or metadata the project doesn't have.
---

# README Writer

## Purpose

Produce a README that accurately documents a real project: what it is, how to install/use it, and where to go for more. Works for libraries, CLIs, APIs, web apps, and Claude Skills alike.

## Core rule

**Document what exists — don't invent it.** Before writing:
- Read the actual code, manifest, or skill files if available (package.json, SKILL.md, setup.py, existing docs).
- If a detail (license, version, CI status, install command) isn't known, ask the user or mark it clearly as a placeholder (e.g. `<!-- TODO: add license -->`) rather than fabricating it.
- Badges, links, and commands must reflect the real project — don't paste generic Shields.io badges for CI/coverage/PyPI unless that infrastructure actually exists.

## Step 1 — Gather context

Ask or infer:
1. What does the project do, in one sentence?
2. Who's the primary audience — end users, developers integrating it, or both?
3. How is it installed/run (pip, npm, CLI binary, "just copy this file", "install as a Claude Skill")?
4. Does it have: a license, CI, a changelog, existing screenshots/demos, a repo URL?
5. Is this a single flat README, or does it need a docs/ site (MDX, Docusaurus, etc.)? Default to a single Markdown README unless the project is large enough to need more, or the user asks for a site.

Don't stall on unanswered questions — use sensible defaults (plain Markdown, MIT-style placeholder, no badges if no CI/package registry exists) and flag assumptions in the response.

## Step 2 — Choose structure

Default section set (use only what applies — skip sections that don't fit a small project, e.g. a one-file Skill doesn't need a CI badge or a Customization section):

1. **Title + one-line description**
2. **Badges** — only for infrastructure that's real (license, version, build). Omit entirely for small/simple projects rather than padding with fake badges.
3. **Features** — short bullet list, only real capabilities
4. **Demo** — a screenshot, GIF, or short sample input/output block if available; skip if there's nothing to show
5. **Installation / Quick Start** — copy-pasteable, minimal
6. **Usage** — real code snippets or CLI examples with expected output
7. **Configuration / Customization** — only if the project has options
8. **API / CLI Reference** — table of functions/commands, only for libraries or tools with a real surface area
9. **Contributing** — link to CONTRIBUTING.md if it exists, else a short one-liner or omit
10. **License**

For a Claude Skill specifically, replace "Installation" with **how to add the skill** (e.g. "save this `.skill` file / drop the folder into your skills directory") and "Usage" with **example prompts that trigger it** and what output to expect.

## Step 3 — Write it

- Plain, concise language. Imperative voice for instructions ("Run `pip install x`", not "You should run...").
- Fenced code blocks with the right language tag.
- Keep examples runnable/accurate — don't show a command or function signature that doesn't match the real project.
- Alt text on every image (`![Description of what's shown](path)`), never left blank unless the image is purely decorative.
- If interactive elements (tabs, live demo embeds) are wanted and the target is a docs site (MDX/Docusaurus/Next.js) rather than a bare GitHub README, use those — but note plain GitHub-flavored Markdown can't render tabs/JS, only badges/images/collapsible `<details>` blocks. Don't propose iframes or React components for a plain `.md` file that GitHub will render as-is.

## Step 4 — Assets and automation (only if asked)

If the user wants automated screenshots, GIFs, changelog generation, or CI badges wired up, that's a separate, larger task — confirm what's actually available in their repo/CI setup first rather than generating scripts against tooling (Puppeteer workflows, Shields endpoints, changelog generators) that may not be installed or wanted. Offer this as a follow-up rather than bundling it into every README by default.

## Step 5 — Output

- Single README.md (or the file the user named) using create_file, following the docx/pptx-style file-creation conventions of this environment (i.e., only make it a downloadable file if that's what's wanted — otherwise show it inline for review first).
- Briefly flag any placeholders or assumptions made (e.g. "I didn't see a license file, so I left a placeholder — let me know what license to use").
