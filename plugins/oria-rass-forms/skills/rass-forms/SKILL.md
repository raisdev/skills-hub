---
name: rass-forms
description: Fills ORIA forms (currently the Grant-IACUC Protocol Comparison Checklist, the "congruence form") from a RASS record PDF and returns a finished PDF. Use when the user says things like "I need a form with the RASS information filled out", "make the congruence form", "fill the OSP to IACUC checklist", "process the RASS PDFs", or wants to add a new form filled from RASS.
---

# RASS forms

Fill one of ORIA's forms from a RASS record PDF. Every step that produces values is deterministic, done by the bundled Python scripts. Don't type values by hand and don't guess.

The person you're helping may not be technical or familiar with Claude. Use plain language and don't mention scripts, JSON or bash unless they ask.

## How the user gets the RASS PDF

On the RASS website, the user opens the grant record and clicks the **cloud icon with a downward arrow** in the **upper right corner** of the page. That generates a PDF of the record. They select the sections the form needs and save the PDF into their **Documents › Claude › RASS grant data** folder. Don't tell them to use the browser's print command; the RASS cloud download is the correct method.

## Where things are

- **Scripts (read-only, ship with this plugin):** `${CLAUDE_SKILL_DIR}/scripts/`.
  - `run_form.py` is the one entry point. `extract_rass.py` and `fill_checklist.py` do the work, and `forms.json` lists the forms.
  - In the bash workspace, that folder may appear under a different path. If the path above doesn't exist in bash, locate it with `find / -path "*rass-forms/scripts/run_form.py" 2>/dev/null | head -1`.
- **User guide:** `${CLAUDE_SKILL_DIR}/USER-GUIDE.md`. It's a plain-language guide: Part 1 covers filling out a form, Part 2 covers adding a form, and there's a one-time setup section. Offer to save a copy into the user's data folder the first time.
- **User's data folder:** `C:\Users\<username>\Documents\Claude\RASS grant data`. It holds RASS PDFs, the form templates, outputs, and `rass_extracted.json`.
  - If `Documents\Claude` isn't connected, call `request_cowork_directory` with the user's `Documents\Claude` path. Explain in one sentence that this lets Claude read the RASS PDF and save the form.
  - If the `RASS grant data` subfolder doesn't exist, create it.
  - Pass this folder to every command with `--dir "<bash path of the folder>"`.
- **Form templates are NOT shipped** with the plugin, because this repo is public and the template is marked confidential. On first use, check that the template named in forms.json, e.g. `OSP to IACUC Template GCC.dotx`, is in the data folder. If it isn't, tell the user to get it from the IACUC office and save it there, and stop until they have.
  - A user may add their own forms: a `forms.json` in the data folder overrides the shipped one.

## Commands

```
python3 "<scripts>/run_form.py" --dir "<data>" --list               # forms and sections each needs
python3 "<scripts>/run_form.py" --dir "<data>" congruence           # new RASS PDFs in the folder
python3 "<scripts>/run_form.py" --dir "<data>" congruence a.pdf     # specific files
python3 "<scripts>/run_form.py" --dir "<data>" congruence --all     # reprocess everything
```

## Workflow

1. **Pick the form.** If the user named a form, match it against the `id` and `aliases` from `--list` / forms.json. If they didn't, offer the forms with AskUserQuestion. If there's only one form, confirm it in one short line.
2. **Tell them the RASS sections to include** in the cloud-icon download: that form's `rass_sections`. For the congruence form, they are:
   - the OSP # line (the page header)
   - Award Details
   - Compliances

   If the form has `optional_sections`, list them separately under "also include when it applies", giving each one's `when` text. Subawards is the usual example. Tell them that including extra sections never hurts.

   Remind them to save the PDF into Documents › Claude › RASS grant data. If the PDFs are already there, skip this step.
3. **Run it.**
4. **Report the results.** For each PDF, report one of these:
   - DONE: give a computer:// link to the output PDF, and show the filled values in a short table so they can check them.
   - STOP: in plain words, say what's missing (a section that wasn't included, a field that's blank in RASS, or the template) and how to fix it. Don't produce a form, don't fill gaps from any other source, and don't guess.
   - Notes: pass on any `note:` lines, such as a protocol whose status isn't Approved.
   - Optional sections: pass on each `[INFO]` line saying whether an optional section was included. If one that probably applies is missing, ask whether they meant to include it.
5. Output is **PDF only**.

## Congruence form rules

These were set by the IACUC office and are built into the scripts. Change them in the scripts, not by hand.

- **Source:** every header field comes from RASS only. That covers the comparison date (today, YYYY-MM-DD), OSP #, grant PI, grant title, sponsor abbreviation, grant sponsor #, IACUC protocol #, IACUC PI, and IACUC protocol title.
- **Missing fields:** if the Sponsor Award Number is blank, write "Not in RASS". If any other field is missing, the record is STOP and no form is made.
- **Sponsor abbreviation:** take the last abbreviation in parentheses in Awarding Sponsor. For example, "Public Health Service (PHS) -> NIH National Institutes of Health (NIH)" gives "NIH".
- **Grant title:** remove a trailing year range, such as "- yrs 4 - 5".
- **Names:** never include NetIDs.
- **One protocol:** write the number only, e.g. "2021-0018".
- **Several protocols:** separate everything with semicolons, in the order RASS lists them.
  - Protocol #: "2021-0018 (Smith); 2021-0109 (Jones)", with the PI's last name in parentheses.
  - IACUC PI: "Jane Smith; Robert Jones".
  - Protocol title: "Title A; Title B".
- **Document title line:** "<OSP #> to <IACUC Protocol # field>".
- **Comment sentence:** fill in the OSP# and the protocol number(s), and remove the yellow highlight. Use the plural "protocols" when there's more than one.
- **What stays the same:** the 12 congruence items stay "Y", Corrective Action stays "No", Follow Up stays "None", and the signature block is untouched. Don't evaluate these items or ask about them.
- **IACUC table only:** read only the IACUC table in Compliances. The IBC "MUA Number" table below it has the same layout, so don't confuse the two.
- **Output file name:** `Checklists\<OSP> to <protocol numbers, comma-separated>.pdf`. If that file is open, a numbered copy such as "(2)" is saved instead.

## Adding a new form

Follow Part 2 of USER-GUIDE.md, so your questions match what it asks of the user.

1. Get the blank form (.docx/.dotx), a sample RASS PDF downloaded with the cloud icon, and the list of blanks. For each blank you need the RASS section and label, the formatting, and what to do when the value is blank.
2. Sort the sections into **required** (if missing, the record is STOP) and **optional** (`optional_sections` entries `{section, marker, when}`). If an optional section is missing, the form is still made, and its fields are left blank or get the user's stand-in.
3. The bundled scripts are read-only. Copy `forms.json` and any new or changed scripts into the user's data folder, then add the entry and the fill script there. A data-folder forms.json overrides the shipped one. Use `section_span(lines, "<Heading>")` from extract_rass.py to read a section. It detects RASS section headings by font size (about 13.5 pt), so extra sections can't bleed into the one being read.
4. Test on the sample, render the PDF and look at it, then confirm with the user. Their corrections become rules in the script.
5. If the form should be available to everyone, tell the user to file an issue or PR at https://github.com/raisdev/skills-hub so it can be added to this plugin. Templates still can't go in the public repo.

## When not to use this skill, and when to hand off

- **Don't make IACUC determinations.** The congruence items are pre-set by office policy; don't review grant content against protocols.
- **Hand off to the IACUC office** if the user asks to change form wording, the congruence defaults or the rules above.
