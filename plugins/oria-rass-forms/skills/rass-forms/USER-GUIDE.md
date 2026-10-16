# RASS Forms: User Guide

This tool fills in office forms, such as the Grant–IACUC Protocol Comparison
Checklist, with information from a grant record in RASS. You download the record from
RASS as a PDF, ask Claude for the form, and get back a finished PDF. You don't need to
know anything about programming or about how Claude works.

---

## One-time setup

1. **Install the plugin.** In Claude Desktop, go to **Settings › Plugins ›
   Organization**, open the **RAIS Skills Hub** tab, and install **oria-rass-forms**.
2. **Make the folder.** Create a folder named **RASS grant data** inside
   **Documents › Claude**. Claude can also create it for you the first time.
3. **Get the blank form.** The form templates aren't included in the plugin. Get the
   blank form from the IACUC office, e.g. **OSP to IACUC Template GCC.dotx** for the
   congruence form, and save it into **RASS grant data**. Keep the file name
   unchanged.

---

## Part 1: Filling out a form

### Step 1: Download the record from RASS

1. Sign in to the RASS website and open the grant (proposal or award) record you need.
2. In the **upper right corner** of the page, click the **cloud icon with a downward
   arrow**. This creates a PDF of the record.
3. When RASS asks which sections to include, select the sections your form needs (see
   the table below). When you're unsure about a section, include it. Extra sections never
   cause problems.
4. Save the PDF into this folder:

   **Documents › Claude › RASS grant data**

   You can name the file anything, but a name like "Smith 123456.pdf" (PI and OSP #)
   makes it easy to find later.

**Sections to include, by form**

| Form | Always include | Also include when it applies |
|---|---|---|
| Grant–IACUC Protocol Comparison Checklist (congruence form) | OSP # line (the page header), Award Details, Compliances | none at this time |

Some forms need a section only for certain grants. **Subawards** is the common
example: include it when the grant has subawards. The same applies to any other section
listed in the right-hand column for your form. If you forget one, Claude will tell you
it was missing.

### Step 2: Ask Claude for the form

Open the Claude desktop app and type a request in plain words, for example:

> I need a form with the RASS information filled out.

or, if you know which form you want:

> Make the congruence form for the RASS PDF I just saved.

Claude will:

- ask which form you want, if you didn't say,
- remind you which RASS sections the form needs,
- possibly ask permission to use your **Documents › Claude** folder. Choose to allow
  it; this is how Claude reads the RASS PDF and saves the finished form.

You can save several RASS PDFs at once. Claude processes every new one in the folder.

### Step 3: Check the finished form

Claude replies with a link to each finished PDF and a short list of the values it
filled in, so you can check them at a glance. The PDFs are saved in a subfolder of
**RASS grant data**. For the congruence form, that subfolder is **Checklists**.

**If Claude says a record was stopped,** the RASS PDF was missing something the form
needs, such as a section that wasn't selected or a field that's blank in RASS. Claude
names what's missing. No form is made from incomplete information, and nothing is
guessed. Fix it in RASS or download the PDF again with the right sections, then ask
again.

**If a file name ends in "(2)",** an older copy was open when the new one was saved.
Close the old one and delete it if you no longer need it.

---

## Part 2: Adding a new form

Any form that's filled in from RASS information can be added. You provide the form
and the rules, and Claude does the setup.

### What to gather

1. **The blank form** as a Word file (`.docx` or `.dotx`). Leave the spots to be filled
   empty, or put placeholder text in them, such as `OSP#XX`, highlighted in yellow.
2. **A sample RASS PDF** for a real record, downloaded with the cloud icon as in Part 1.
   If you can, pick a record that shows the harder cases, such as more than one protocol
   or a blank field.
3. **A list of the blanks on the form.** For each one, write down:
   - **where the value is in RASS**: the section and the label next to it, e.g.
     "Award Details → OSP #".
   - **how it should look**: for example "no NetIDs", "separate several items with
     semicolons" or "date as year-month-day".
   - **what to do if it's blank in RASS**: either stop and don't make the form, or put
     in a stand-in such as "Not in RASS".
4. **Which RASS sections the form needs:**
   - **Always needed:** every record must have these. If one is missing, the form isn't
     made.
   - **Only sometimes needed:** for example Subawards, needed only when the grant has
     subawards. If it's missing, the form is still made, and the related blanks are
     left empty or get the stand-in you chose.

### How to add it

1. Save the blank form and the sample RASS PDF into **Documents › Claude › RASS grant
   data**.
2. In the Claude app, type something like:

   > I want to add a new RASS form. The template is "[file name]" and the sample is
   > "[file name]".

3. Give Claude your list of blanks and sections. Claude may ask a few questions.
4. Claude fills in the form from the sample and shows you the PDF. Check it carefully
   and say what to change. Your corrections become permanent rules for that form, for
   example "drop the years from the end of the title" or "no names after the protocol
   number when there's only one."
5. When it looks right, the new form appears in the list whenever you ask for "a form
   with the RASS information filled out."

---

## Good to know

- **Source:** information comes only from the RASS PDF. Claude doesn't look anything
  up elsewhere or fill gaps with guesses.
- **Output:** finished forms are always PDFs.
- **Re-runs:** you can make a form again from the same RASS PDF. The new version
  replaces the earlier information.
- **Access:** Claude can only work in the **Documents › Claude** folder. RASS PDFs and
  blank forms must be saved there, not in Downloads or on the desktop.
- **What's in this folder:**
  - The form templates, e.g. "OSP to IACUC Template GCC.dotx".
  - Saved RASS PDFs.
  - A data file ending in `.json` that the tool uses. Please don't edit, move or
    rename it.
  - Output subfolders such as **Checklists**.
