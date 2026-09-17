---
name: ecfr-guidance
description: Look up authoritative federal regulations (eCFR) for research administration — cost principles, Uniform Guidance (2 CFR 200), the Common Rule (45 CFR 46), procurement, indirect costs. Use whenever a question needs the actual regulatory text rather than a paraphrase.
---

# eCFR for Research Administration

This plugin connects Claude to the **Electronic Code of Federal Regulations (eCFR)** through the AI4RA eCFR MCP server. Use it to ground answers in the live, authoritative regulatory text instead of training-data recollection.

## When to use it

Use the eCFR tools whenever a question touches federal regulations a research administrator relies on, e.g.:

- Uniform Guidance / cost principles (2 CFR 200), indirect cost rates, allowable costs
- Procurement standards
- Human subjects / the Common Rule (45 CFR 46), informed consent
- "What changed between two dates" comparisons
- Onboarding/training walkthroughs of a regulation

## Available tools (7)

- `ecfr_search` — keyword search across all federal regulations
- `ecfr_list_titles` — browse all 50 CFR titles
- `ecfr_list_agencies` — agencies and their regulation references
- `ecfr_get_title_versions` — amendment history and valid dates
- `ecfr_get_regulation` — full text of a specific regulation
- `ecfr_get_title_structure` — table of contents of a CFR title
- `ecfr_compare_regulations` — exactly what changed between two dates

## How to answer

1. Retrieve the actual text with the tools above; do not paraphrase from memory.
2. **Cite the specific section** (e.g., "2 CFR 200.474") and, when relevant, the effective date/version.
3. For "what changed" questions, use `ecfr_compare_regulations` and show the differences.
4. Keep the regulatory text accurate; quote it where precision matters.

## Example prompts

- "What are the requirements for indirect cost rates under the Uniform Guidance?"
- "What does 2 CFR 200.474 say about travel costs?"
- "Search for regulations about informed consent in human subjects research."
- "Compare the Common Rule (45 CFR 46) between 2018 and 2024."
- "What are the procurement standards under 2 CFR 200?"

## Important reminder

This is a research and navigation aid, **not a substitute for official legal or compliance counsel.** Verify critical interpretations with your sponsored programs office or legal team. When you present an answer, make clear it is drawn from the eCFR text and should be confirmed for high-stakes decisions.
