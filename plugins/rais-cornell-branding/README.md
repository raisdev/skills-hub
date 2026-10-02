# rais-cornell-branding

Helps Claude build, edit and review web pages, front-end code, slides, PDFs, charts and copy so they follow the Cornell brand guidelines at https://brand.cornell.edu/. It works from a small knowledge base built from that site, cites a rule ID and source link for every requirement it states, and says plainly when the site is silent.

**Owner** Cornell RAIS. **Status** published. **Version** 0.1.0. **Knowledge base as-of** 2026-10-02. Contact rais@cornell.edu.

## What is inside

- Skill `cornell-brand`: build, review or answer questions about anything Cornell-branded. It triggers on brand, colors, fonts, logo, seal, nomenclature, "CU", photo credits, AI-generated images, music licensing, and "is this on brand". In review mode it returns a findings table with rule IDs, source URLs and suggested fixes.
- Knowledge base (`skills/cornell-brand/knowledge-base/`), each rule tagged **Official** (stated by the brand site), **Derived** (RAIS's extrapolation) or **Unspecified** (the site is silent):
  - `colors.md` palette, approved pairings, contrast ratios, paste-ready CSS variables
  - `typography-web.md` fonts, layout examples, web accessibility
  - `logos.md` which logo to use where, sizes, clear space, lockups, brand architecture
  - `nomenclature.md` unit, campus and student-organization names with approved and not-approved variants, the ban on "CU", the founding principle
  - `media-licensing.md` photography, credits, AI use, music, releases
  - `governance.md` policies, approval forms, merchandising, FAQ rules, when to hand off
  - `derived-guidance.md` charts, Office and PDF documents, components, dark mode (the site says nothing on these)
  - `_sources.md` every page crawled, what was not reviewed, conflicts in the source

## Connectors needed

None.

## Caveats

- **The site is the authority, not this plugin.** The knowledge base is a snapshot. Brand Communications (brand@cornell.edu) decides edge cases. Re-check anything public-facing.
- **It never draws or edits a Cornell logo or seal**, and bundles no Cornell artwork or fonts (Freight and Palatino are licensed). Get logos from https://brand.cornell.edu/resources/downloads (institutional sign-in required).
- **Not reviewed:** the gated downloads (PowerPoint templates, logo zips, favicon, outro video), the full text of Policy 4.10 and 5.12, and WCAG itself.
- **Charts, Office/PDF and UI components are Derived guidance.** The brand site does not cover them; the skill labels every such suggestion.
- The brand site contradicts itself in a few places (for example link blue is `#006699` on the colors page and `#3787b0` in the downloadable palette). The knowledge base records each conflict and which value it uses (`_sources.md`).

## Refreshing the knowledge base

See the "How to refresh" steps at the end of `skills/cornell-brand/knowledge-base/_sources.md`. Update the as-of date here and in that file, and bump `version` in `.claude-plugin/plugin.json`.
