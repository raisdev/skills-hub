# oria-rass-forms

Fills ORIA forms with information from a grant record in RASS. The user downloads the
record from RASS as a PDF (the cloud icon with a downward arrow, upper right of the
record page) and asks Claude for the form. Claude returns a finished PDF. The first
form is the **Grant–IACUC Protocol Comparison Checklist** (the "congruence form").
More forms can be added.

**Owner** Cornell ORIA, with content maintained by the IACUC office. **Status** published.
**Version** 0.1.0. Questions, corrections and update requests go through the issue
forms at https://github.com/raisdev/skills-hub/issues.

## What is inside

- **Skill `rass-forms`:** triggers on requests like "I need a form with the RASS
  information filled out" or "make the congruence form." It:
  - asks which form, if the user didn't say, and lists the RASS sections to include
    in the download. Some sections are needed only when they apply, such as Subawards.
  - runs bundled Python scripts that read the RASS PDF and fill the Word template.
    Values come from fixed parsing rules, not from the model's judgment.
  - stops and names what's missing when a required section or field isn't in the RASS
    PDF. It never guesses or fills gaps from other sources.
  - shows the values it filled so the user can check them.
- **`skills/rass-forms/scripts/`:**
  - `run_form.py`, the entry point.
  - `extract_rass.py`, which turns a RASS PDF into JSON.
  - `fill_checklist.py`, which turns the template and JSON into a PDF.
  - `forms.json`, the list of forms.
- **`skills/rass-forms/USER-GUIDE.md`:** a plain-language guide covering setup, filling
  out a form, and adding a new form.

## Setup

Form templates are **not** in this repo, because the repo is public and the templates
are internal. Each user saves the template from the IACUC office into
`Documents\Claude\RASS grant data\`; the skill says so on first use. Outputs and the
extracted data stay in that folder on the user's PC.

## Connectors needed

None. The skill uses the Cowork workspace, with Python and pdfplumber for reading
PDFs and LibreOffice for making the PDF output.

## Caveats

- **The checklist is not an IACUC determination.** The 12 congruence items are pre-set
  to "Y" by office practice; the skill doesn't compare grant content with protocols.
  The IACUC Administrator remains responsible for the comparison.
- **Only RASS is used.** If RASS is wrong or incomplete, the form will be too, or it
  won't be made at all.
- **Tested on one RASS PDF layout** (Sponsored Research Protocol Application, October
  2026). If RASS changes its PDF layout, the parsing rules may need updating. In that
  case the skill stops rather than produce a wrong form.
- **Output is PDF only.**
