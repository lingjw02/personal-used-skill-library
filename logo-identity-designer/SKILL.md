---
name: logo-identity-designer
description: Guides a complete logo/brand-identity design workflow -- brief intake, creative strategy, 3+ differentiated concept directions, AI-generation prompts, evaluation scoring, refinement, and a full delivery package (SVG vector master, transparent PNG, PDF, monochrome/reversed versions, icon-only, horizontal/vertical lockups, color codes, typography and font-licensing notes). Use whenever the user asks to design, create, generate, or brainstorm a logo, brand mark, wordmark, monogram, symbol/icon, or full brand identity -- for a business, product, app, rebrand, or personal project -- even from a one-line request like "make me a logo for X." Also use to critique/refine an existing logo, build out a logo system/lockup set, pick fonts/colors for a mark, or run a preliminary trademark-conflict check on a logo/name. Auto-selects one of six creative modes (minimal, detailed/default, creative-exploratory, corporate, vintage, tech-startup) based on the brief, or lets the user pick explicitly.
---

# Logo Identity Designer

A logo request is rarely well served by a single "make it modern and blue" prompt straight to an image generator -- the model has nothing to differentiate the brand from thousands of others. It's also poorly served by six unrelated one-off prompts that each reinvent the workflow. Use **one** identity-design workflow every time: brief → strategy → concept exploration → evaluation → refinement → production → delivery. Layer a creative-mode preset on top to shift tone and emphasis (minimal, detailed, creative-exploratory, corporate, vintage, tech/startup) without ever dropping the underlying production discipline.

Treat any AI-generated logo image as **concept material** until it has been rebuilt or verified as genuine editable vector artwork. A raster image saved with a `.svg` extension is not a vector logo.

## Operating principles

Optimize concepts and the final mark for, in rough priority order: strategic relevance to the brand → differentiation from category clichés and named competitors → legibility → memorability → appropriate simplicity → scalability → reproduction across the stated use contexts → consistency as a system (not just one pretty image). Visual attractiveness alone is not the goal -- a beautiful mark that's indistinguishable from ten competitors, illegible at 32px, or unreproducible in one color has failed the brief.

## Step 0 -- User mode and creative mode

**User mode** (ask if unclear, or infer from how the person writes):
- **Designer** -- use professional terminology, preserve their explicit technical decisions, expose rationale and production detail, don't over-explain.
- **Non-designer** -- translate jargon into plain language, offer compact choices ("clean/modern," "friendly/human," "traditional/premium," "expressive/custom") instead of asking for typographic classifications, and only explain decisions that materially change the result.

**Creative mode** -- one of `minimal | detailed | creative | corporate | vintage | tech`, or `auto`. Default to `auto`, which uses **Detailed** as the base and layers in a preset when the brief clearly calls for it:

| Signal in the brief | Add this preset |
|---|---|
| Fast ideation, non-designer, very little detail given | Minimal |
| Most real-world/general branding requests (the safe default) | Detailed |
| Music, fashion, culture, entertainment, youth brand, wants to stand out above all | Creative-exploratory |
| Finance, law, consulting, insurance, B2B, regulated/institutional | Corporate |
| Heritage, craft, hospitality, food & beverage, period/nostalgic character | Vintage |
| SaaS, AI, dev tools, fintech, app-first product | Tech/startup |

If the user names a mode explicitly, use it as stated. Read `references/mode-presets.md` for what each preset changes (question priorities, exploration breadth, default typography/color logic, cliché-avoid lists, and a worked example) -- **only load the section for the mode(s) actually in play**, not all six. A mode preset only ever adjusts *emphasis*; it never removes a required deliverable (a vintage mark still needs a clean monochrome vector, a tech mark still needs a flat one-color fallback, a minimal mark still needs proper lockups).

## Step 1 -- Gather the brief

Ask for missing **required** fields; for everything else, state a reasonable assumption and move on. Never present the person with the full field list as a questionnaire -- **ask at most 3 questions at a time**, and only about high-impact missing information.

| Field | Priority | What to capture |
|---|---|---|
| Brand name | Required | Exact spelling/capitalization/pronunciation |
| Industry / niche | Required | Category plus the specific niche |
| Product or service | Required | What the brand actually sells or does |
| Brand values | Required | Ideally 3-5 |
| Usage contexts | Required | Web, app, social, packaging, signage, print, merch, decks... |
| Color preferences | Required or defaultable | Preferred, prohibited, existing brand colors |
| File formats | Required or defaultable | Default to SVG + PNG + PDF if unstated |
| Aspect ratios | Required or defaultable | Default to 1:1 icon + horizontal + stacked vertical |
| Tagline | Optional | Exact copy; must it appear in the primary lockup? |
| Target audience | Recommended | Who buys/uses it, geography, B2B/B2C |
| Desired / avoided perception | Recommended | "Should feel..." / "must not feel..." |
| Style references | Optional | See note below -- extract attributes, don't copy |
| Iconography / metaphors, and clichés to avoid | Optional | |
| Typography preference | Optional | Serif/sans/slab/script/custom, etc. |
| Competitors | Recommended | Brands to visibly differentiate from |
| Existing assets | Optional | Current identity, brand guide, packaging |
| Budget / timeline | Optional | Scope control -- see scope tiers below, not an aesthetic direction |
| Trademark-screening level | Optional | `none` (default) / `preliminary` / `counsel_ready` -- see `references/trademark-screening.md` |
| Jurisdictions | Conditional | Only if screening was requested |
| Reproduction constraints | Optional | One-color printing, embroidery, engraving, tiny favicon, etc. |

**Style references are attributes, not templates.** If someone says "like Apple" or names a designer/portfolio, translate that into qualities -- e.g. high negative space, geometric economy, restrained palette, compact silhouette -- and design from those qualities. Never reproduce, closely imitate, or output something a reasonable viewer would recognize as a real company's or designer's distinctive existing mark.

## Step 2 -- The workflow

Run through these in order. Keep the pace appropriate to the mode and scope tier (see below) -- a Minimal-mode request shouldn't get a five-territory exploration, and a Detailed/Corporate request shouldn't get rushed to one concept.

**A. Brief validation** -- Summarize the brief back in 5-8 lines. Flag contradictions (e.g. "playful and youthful" + "must feel like a 100-year-old institution") and any high-impact gaps or assumptions before designing anything.

**B. Creative strategy** -- Before any visuals: the core brand idea in one sentence, 3-5 visual keywords, the differentiation strategy, an icon strategy, a typography strategy, a color strategy, and the category clichés/conventions this brand should specifically avoid.

**C. Concept directions** -- Generate genuinely different territories (default **3**; Creative-exploratory mode uses 5 then narrows to 3, Tech/startup uses 4 -- see the preset file). Don't create superficial variants that only swap color. For each territory give: a name, a one-sentence idea, symbol construction, typography direction, color logic, why it fits the brand, its main weakness/risk, and a ready-to-use image-generation prompt.

**D. AI generation prompts** -- For each concept worth generating, write a clean prompt with: exact brand name and spelling, logo type, the visual concept, composition, geometric/form language, typography character, palette, background, intended reproduction behavior, and explicit exclusions (what *not* to include). Prefer a flat, plain-background presentation for evaluation -- don't let a decorative lifestyle mockup hide weaknesses in the actual mark.

**E. Evaluation** -- Score each concept 1-10 on: strategic fit, distinctiveness, legibility, scalability, monochrome performance, icon-only performance, and cross-context versatility. Give a one-line reason for each score. Recommend one direction while keeping the others visible -- don't silently discard them.

**F. Refinement** -- Resolve spacing, proportions, line weight, and balance on the selected direction. Test it mentally (or actually, if you can generate/view images) on: light background, dark background, monochrome, small icon/avatar size, horizontal layout, and vertical/stacked layout.

**G. Final logo system** -- Specify or produce: primary logo, primary reversed (dark-background), monochrome black, monochrome white, icon-only/symbol-only, horizontal lockup, vertical/stacked lockup. Add wordmark-only, favicon/app-icon, a micro-size simplified mark, or a tagline lockup when the use contexts call for them.

**H. Delivery** -- Package the outputs per the contract in `references/production-delivery.md` (vector SVG master, raster PNGs, PDF spec sheet, HEX/RGB/CMYK, typography + font-license notes, clear-space and minimum-size guidance, a one-page mini style guide). Read that file before promising deliverables -- in particular, never promise transferable font *files* by default; promise font suggestions plus licensing/source notes, and only include files where redistribution is actually authorized.

**I. Trademark mode** -- Only if the person asked for screening. Read `references/trademark-screening.md` and follow the mode (`preliminary` or `counsel_ready`) exactly, including its rule about never asserting a mark is "trademark safe" or "legally cleared."

**J. Final QA** -- Before presenting the result, run the three gates below.

```
DESIGN GATE
  Does the mark reflect the actual brand strategy (not just "looks nice")?
  Is it distinguishable from category clichés and named competitors?
  Does it still work without a presentation mockup?
  Does it survive being rendered in pure black and white?
  Is the brand name spelled correctly, with no unintended letters/shapes?
  Is it recognizable at the smallest size the brief requires?

PRODUCTION GATE
  Is a genuine vector master available, or clearly marked as pending?
  Are primary + monochrome + icon + horizontal + vertical accounted for?
  Are SVG + PNG + PDF accounted for (or the formats actually requested)?
  Are color values and typography documented?
  Is font licensing/transfer status stated?

RISK GATE
  Were references used as attributes, never copied outright?
  Is trademark-search status (if any) stated accurately, with no overclaiming?
  Are similarity concerns to real brands disclosed rather than glossed over?
  Are open assumptions and unresolved issues disclosed to the user?
```

## Scope tiers

Let budget/timeline control *scope*, never *quality* -- a smaller budget should mean fewer directions and lighter documentation, not a worse-looking mark.

- **Lean** -- 2-3 directions, 1 refinement pass, core logo family only, SVG + PNG + PDF, basic color/type notes.
- **Standard** (default) -- 3 directions, 2 refinement passes, full lockup system, small-size + monochrome testing, core application mockups, mini brand sheet.
- **Extended** -- 4-6 directions, multiple refinement passes, expanded responsive logo system, deeper competitive/visual audit, trademark-review handoff package, expanded usage guide.

## Reference files

- `references/mode-presets.md` -- what each of the six creative modes (minimal, detailed, creative-exploratory, corporate, vintage, tech/startup) changes about the brief questions, exploration breadth, typography/color defaults, and cliché-avoid list, plus one worked example per mode. Load only the mode(s) in play.
- `references/production-delivery.md` -- the full deliverable contract table, why SVG is the right vector master format, the font-licensing rule (and why "just include the font files" is not always safe to promise), and more detail on the scope tiers.
- `references/trademark-screening.md` -- the three trademark-screening levels, what a preliminary search can and can't tell you, and the exact language rules for never overstating legal clearance.
