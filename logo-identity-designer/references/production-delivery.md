# Production and delivery

There are three different statuses a logo can be in -- don't conflate them when talking to the user:

- **Concept-ready** -- the visual idea is coherent enough to compare against other directions. Not yet a deliverable.
- **Production-ready** -- the chosen logo exists as an actual identity system: reliable vector geometry, the required lockups, verified monochrome behavior, documented color specs, and usable exports.
- **Trademark-ready for professional review** -- the identity is documented well enough for a human/legal search, *not* an assertion that it's legally clear. See `trademark-screening.md`.

## Why SVG is the vector master

SVG is an XML-based, standards-defined format for vector and mixed vector/raster 2D graphics that scales to any display resolution -- that's exactly what a logo master needs. Treat a raster image that's merely wrapped in an `.svg` file extension as **not** a real vector logo; it must actually be built (or reconstructed) from vector shapes/paths to earn that label. If you can't produce genuine vector geometry given the current tools, say so plainly rather than mislabeling the output.

## Font licensing -- don't over-promise

Default to delivering **font suggestions plus source/license notes**, not transferable font files. Commercial font services (e.g. Adobe Fonts) commonly permit using a licensed font *in* finished logo artwork, but that's different from handing the actual font software to a client or collaborator for their own editable use -- that generally requires its own license and isn't something a designer can just package and redistribute. So:

- Always name the specific font family, weight(s), and style used or recommended.
- Always note where it comes from and, in general terms, that commercial/redistribution use may need its own license -- don't assert a specific license's terms unless you've actually verified them for that font.
- Only include actual font files in a deliverable package when the user has confirmed they hold (or the font is under) a license that permits that redistribution.

## Deliverable contract

Use this as the default checklist for a Standard-scope Detailed-mode project; trim per the scope tier and creative mode in play (a Minimal request still needs the starred items).

| Deliverable | Default | Note |
|---|---|---|
| Primary full-color logo * | Yes | The master composition |
| Reverse / dark-background logo | Yes | Verify actual contrast, don't just invert colors blindly |
| Black monochrome * | Yes | Must not depend on color to read correctly |
| White monochrome * | Yes | For dark backgrounds |
| Icon / symbol only * | Yes, when the identity supports one | Test at avatar/app-icon scale |
| Wordmark only | Recommended | Useful for constrained horizontal layouts |
| Horizontal lockup * | Yes | Web headers, signage, documents |
| Vertical / stacked lockup * | Yes | Square or tall compositions |
| Micro-size variant | Context-dependent | Favicon / tiny UI use |
| SVG * | Yes | Preferred editable, scalable vector master |
| Transparent PNG * | Yes | Practical raster sizes for the stated use contexts |
| PDF | Yes | Presentation / print / share package |
| HEX * | Yes | Digital brand color |
| RGB | Yes | Digital specification |
| CMYK recommendation | When print matters | Flag that it should be verified in the actual print workflow |
| Font family/weight names * | Yes | Exact, not "a clean sans-serif" |
| Font source/license note * | Yes | See above |
| Font files | Conditional | Only when redistribution rights are confirmed |
| Clear-space guidance | Recommended | A simple proportional rule (e.g. "clear space = height of the icon on all sides") |
| Minimum-size guidance | Recommended | Based on an actual legibility check, not a guess |
| Preliminary trademark report | Optional | Only if screening was requested -- see `trademark-screening.md` |

## Scope tiers, in more detail

Budget and timeline should shrink or grow the *scope* of work, never the *quality* of the recommended direction.

**Lean**
- 2-3 directions, 1 refinement cycle
- Core logo family only (primary, monochrome, icon)
- SVG + PNG + PDF
- Basic color values + type notes, no full style guide

**Standard (recommended default)**
- 3 directions, 2 refinement cycles
- Full lockup system (horizontal + vertical + reversed)
- Small-size + monochrome testing documented
- Core application mockups (e.g. one or two realistic use contexts)
- A mini one-page brand/style sheet

**Extended**
- 4-6 exploratory directions, multiple refinement passes
- Expanded responsive logo system (including micro-size variant)
- Deeper competitive/visual-similarity audit
- More application testing across the full stated use-context list
- Trademark-review handoff package (`counsel_ready` mode)
- Expanded usage guide (misuse examples, clear-space diagrams, etc.)

These are workflow-scope tiers, not market pricing benchmarks -- don't quote them to a user as dollar figures.
