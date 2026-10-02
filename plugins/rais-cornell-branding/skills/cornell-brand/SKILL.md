---
name: cornell-brand
description: "Use whenever the user builds, edits, reviews or asks about anything Cornell-branded: web pages, HTML/CSS, React or other front-end code, slides, PDFs, Word or Excel files, charts, email, or copy and UI strings. Also use for questions about the Cornell brand, Cornell red or carnelian, brand colors, fonts, logo, seal, lockup, wordmark, clear space, nomenclature (how to name colleges, schools, units and campuses), the ban on abbreviating Cornell University, the founding principle, photo credits, AI-generated images, music licensing, or 'is this on brand', 'check brand compliance', 'review against brand.cornell.edu'. Answers only from the bundled knowledge base, cites rule IDs, and never draws or edits a Cornell logo or seal."
---

# Cornell brand compliance

Keeps code, documents and copy consistent with the Cornell University brand guidelines (https://brand.cornell.edu/). Every answer comes from the knowledge base in `knowledge-base/`, which was built from a crawl of that site. Do not answer brand questions from memory.

## Ground rules (read these first)

1. **Only state what the knowledge base (KB) says.** Every Cornell requirement you state must come from a KB rule and carry its ID (for example `COL-10`) and status tag.
2. **Three statuses.** `Official` means brand.cornell.edu says it. `Derived` means it is RAIS's extrapolation. Say "derived" and never say "Cornell requires" for it. `Unspecified` means the site is silent. Say "brand.cornell.edu does not specify this", then, if useful, offer a labeled Derived suggestion from `knowledge-base/derived-guidance.md`.
3. **Never draw, trace, recolor, crop or recreate a Cornell logo, seal, lockup or wordmark**, as SVG, CSS, an image or ASCII. Leave a labeled placeholder and send the user to the official downloads (`LOG-80`). This has no exceptions.
4. **Check before you cite.** Open the KB file that holds the rule. Confirm the ID exists there. Do not cite an ID you did not read in this session.
5. **Date the verdict.** The KB is as of 2026-10-02 (see `knowledge-base/_sources.md`). When you give a compliance verdict, say so and note the site may have changed. For high-stakes or public-facing work, suggest confirming with Brand Communications (brand@cornell.edu).
6. **Do not invent rules to sound thorough.** A short honest "not specified" beats a confident guess.

## Choose a mode

| The user wants | Mode | Output |
|---|---|---|
| Something built or edited (page, stylesheet, deck, chart, copy) | **Build** | Produce it following the KB, then list the rule IDs you applied and any Derived or Unspecified choices you made |
| Existing code, a page, a document or copy checked | **Review** | The findings table below |
| A question ("what red do we use?", "can we use CU?") | **Answer** | The rule quoted or closely paraphrased, its ID, status and source URL |

## Route to the right KB files

Read only what the task needs. All paths are under `knowledge-base/`.

| If the task involves | Read |
|---|---|
| Colors, contrast, palette, CSS variables | `colors.md` |
| Fonts, web layout, accessibility, Web Communications Standards | `typography-web.md` (and `colors.md`) |
| Any logo, seal, lockup, wordmark, favicon, header/footer identity, department or program marks | `logos.md` |
| Any mention of a Cornell college, school, unit, campus or office; the words "Cornell", "CU", "Weill"; student orgs; the founding principle; mission text | `nomenclature.md` |
| Photos, video, illustrations, AI-generated images, music, releases, credits | `media-licensing.md` |
| Approvals, forms, policies, merchandise, who to contact | `governance.md` |
| Charts, dashboards, Word, Excel, PowerPoint, PDF, email, dark mode, buttons and components | `derived-guidance.md` (and `colors.md`) |
| Where a rule came from, source conflicts, what was not reviewed | `_sources.md` |

For a full review of a web page, read `colors.md`, `typography-web.md`, `logos.md`, `nomenclature.md`, `governance.md` (host, policies, hand-offs) and `derived-guidance.md` (dark mode, buttons, links). Add `media-licensing.md` if the page has images or media, and `_sources.md` when a finding touches a known source conflict (`SRC-01` to `SRC-07`).

## Quick rules (always on; details and IDs in the KB)

- Cornell red is "first and only": carnelian `#B31B1B` should be the first color seen (`COL-01`, `COL-10`).
- Prefer palette colors; anything else is unofficial (`COL-04` says avoid, `COL-50` Derived). Text uses an approved pairing (`COL-41`, `COL-06`). Graphic-only accents never carry text (`COL-31`, `COL-34`, `COL-36`).
- Link blue is `#006699`, not `#3787b0` (`COL-30`, `COL-51`).
- Web typefaces are Freight Text Pro and Freight Sans Pro, Palatino for print and the logo. All are licensed, so never bundle them (`TYP-01` to `TYP-05`).
- Logos appear only in carnelian, black or white, once per homepage or communications piece (`LOG-27` for multi-page pieces), with clear space of 1/4 the seal diameter (`LOG-02`, `LOG-21`, `LOG-24`).
- A site outside cornell.edu should not show a Cornell logo or seal. Do not add one (`LOG-03`).
- No "CU" anywhere users read (`NOM-05`).
- Spell unit names exactly as `nomenclature.md` lists them, and check its not-approved variants (`NOM-90`).
- The founding principle is used verbatim or not at all (`NOM-70` to `NOM-72`).
- AI-generated media is labeled, and never passed off as a real photograph (`MED-21`, `MED-22`).
- Web content must meet WCAG AA contrast (`COL-06`, `WEB-10`).

## Review mode: workflow

1. **Identify the artifact and its host.** Is it on a cornell.edu domain? Do not ask. RAIS treats the color, type and naming rules as binding for its sites whatever the host (`WEB-26`), so report those findings as plain Mandatory or Advisory, never as conditional. The host matters for one thing only: a Cornell logo or seal on a non-cornell.edu site (`LOG-03`). State the host you found in **Host and scope**. If the user says the site is not a Cornell property, say the rules were applied on that assumption and let them decide.
2. **Collect the evidence.** For code, grep for hex and rgb colors, `font-family`, logo/seal/`img` references, "Cornell", "CU", unit names, and any `<title>`, meta, alt text and footer text. For a live page, read both the source and the rendered text. Fetch the raw HTML (for example with curl): summarizing fetch tools drop client-rendered content and exact strings. For documents, inspect the generation code.
3. **Check each item against the KB.** Convert colors to hex before comparing. For contrast, use the ratios in `colors.md` where the pair is listed. Otherwise compute with the WCAG formula and label the result Derived.
4. **Classify each finding.**
   - **Mandatory**: an explicit Official rule is broken: text below the AA thresholds in `COL-06` (the ratio is Derived, the threshold is Official), a graphic-only or large-text-only accent used as text (`COL-31` to `COL-37`), the wrong link blue (`COL-51`), a logo rule (`LOG-02`, `LOG-22`, `LOG-23`, `LOG-24`), a Cornell logo on a non-cornell.edu host (`LOG-03`, whose wording is "should not"), the banned abbreviation (`NOM-05`), a not-approved name (`NOM-10` to `NOM-45`), a modified founding principle (`NOM-71`, `NOM-72`), unlabeled or fabricated AI media (`MED-21`, `MED-22`).
   - **Advisory**: the rule is Derived, or the site only says "avoid": off-palette colors (`COL-04`, `COL-50`), non-brand fonts (`TYP-11`), links without an underline, missing `lang` or alt text (`WEB-14`).
   - **Question**: the site is silent or in conflict (`Unspecified`, `SRC-xx`): unit names not in the table, homemade marks, dark themes. Do not call it wrong. Route it to Brand Communications.
5. **Do not fix anything unless asked.** Report first. If asked to fix, make the smallest change and keep the rule IDs in the commit message or summary.

### Report layout

Always start the review with this block, even when there are no findings (then say what was checked). Use these exact labels so reviews are comparable.

- **Bottom line:** one factual sentence with counts, for example "1 mandatory, 5 advisory, 6 questions for Brand Communications." Say "no mandatory findings" or "N mandatory findings". Do not say "approved" or "safe to publish": that is Brand Communications' call, not this skill's.
- **Fix first:** up to three findings, one line each with its row number.
- **Needs a human decision:** every Question in one list, worded so the user can send it to Brand Communications as a single message.
- **Host and scope:** the host (cornell.edu or not). Color, type and naming rules are applied as binding regardless of host (`WEB-26`); only the logo rule (`LOG-03`) depends on the host.

Then the findings table:

### Findings table

| # | Severity | Location (file:line or URL) | Finding | Rule | Source | Suggested fix |
|---|---|---|---|---|---|---|

Use one row per finding. `Rule` is the KB ID and status, for example `COL-51 Official`. `Source` is the URL in the KB rule. After the table, add:
- **Passed**: the checks that came back clean, so the user knows what was covered.
- **Not covered**: anything you could not check and why (for example the Freight font kit is not visible from the markup).
- **Out of scope**: real problems that are not brand issues (broken links, bugs), mentioned in one line each.
- **KB as-of 2026-10-02**: and the suggestion to confirm with Brand Communications before publishing.

## Build mode: workflow

1. Confirm the host (cornell.edu or not) and audience if that changes a rule.
2. Read the relevant KB files. Start from the CSS variables in `colors.md` (`COL-60`).
3. Build. Keep brand decisions in one place (a tokens file or constants block) so they are easy to audit.
4. Finish with a short "Brand notes" section: rule IDs applied, Derived choices, Unspecified gaps, and placeholders the user must fill (logo file, Adobe Fonts kit).

## Hand off to a person

Stop and send the user to Brand Communications (brand@cornell.edu, consultation form at https://apps.univcomm.cornell.edu/brand-forms/forms/consult.html) when the request involves any of the cases listed in `knowledge-base/governance.md`, section 6, including: any logo or seal creation or alteration, a new logo or identity for a department, lab, program or event, use of the Cornell logo on a site outside cornell.edu, merchandise, affiliates or co-branding, unit names not in the nomenclature table, photos of minors, and accessibility exceptions. Explain why in one sentence, and do not attempt a workaround. In Review mode, keep reviewing everything else: record the item that needs a decision as a Question, say who decides, and propose no workaround.

## What this skill does not do

- It does not read the full text of Policy 4.10 or 5.12, the gated downloads, or the PowerPoint templates (`_sources.md`). Say so when asked about them.
- It gives no legal advice on trademark or copyright. Point to the policies and contacts in the KB.
- It is not for non-Cornell styling tasks. If the task has no Cornell connection, do not apply these rules.
