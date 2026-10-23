---
name: build
description: Build and maintain a knowledge base from a folder of the person's documents (PDFs, Word files, policies, standard agreements, guidance, prior agreements, an existing playbook). Produces a Markdown copy of each document, a generated INDEX.md, and, for contract review, a PLAYBOOK.md that the Legal plugin's reviews follow. Use this skill whenever the person wants to create, set up, build, organize, update, refresh, sync, check, or clean up a knowledge base, KB, reference set, or "Claude folder"; says they added, replaced, renamed, or deleted files in their knowledge base folder; asks to update or approve playbook changes; or says sessions run out of budget because Claude reads everything. Trigger on "create my knowledge base", "update my knowledge base", "approve playbook changes", "continue my knowledge base", and "organize my files". This skill only builds and maintains the knowledge base; questions go to the ask skill and contract reviews to the Legal plugin.
---

# Knowledge Base, build

Build and maintain a knowledge base that any later Claude session can use cheaply. A session reads one short playbook or the index, then opens only the one or two documents it needs. Never a folder scan, never a full read of everything.

The person is a contract reviewer, grants and contracts officer, or analyst, not a developer. Keep every message short and plain. They only ever need two phrases, "create my knowledge base" and "update my knowledge base". Say "Finder" on a Mac and "File Explorer" on Windows; the device info says which. Never say "Finder (File Explorer on Windows)".

## The folder

The person's folder is the knowledge base. Their documents stay exactly where they put them, in whatever subfolders they like. The plugin adds one subfolder, `Claude files (Claude manages)`, and never mentions it in messages. Inside it

- `PLAYBOOK.md`, how the person negotiates and the rules drawn from the documents. Written only for contract review. The person approves every change.
- `INDEX.md`, generated from the documents. One entry per document. Never edited by hand.
- `docs/<same path>.md`, a Markdown copy of each document. Its front matter carries the document's record (fingerprint, type, date) and its index entry (summary, consult when, key sections).
- `_admin/`, bookkeeping. `kb_sync.py` (a copy, so any session can run the check), `CHANGELOG.md`, `proposals/` (playbook changes waiting for approval), `sync/` (diffs of replaced files), `retired/` (old copies, nothing is ever deleted), `needs-attention/` (records of files that could not be converted).

Two small pointer files sit at the top of the person's folder, `CLAUDE.md` and, for contract review, `legal.local.md`. Subfolders whose names start with `_` are ignored, which is where drafts and redlines can go.

There is no manifest and no lock. Each document carries its own record, so two people sharing the folder through SharePoint can never corrupt a shared file. The script tidies any duplicate copies a sync app makes. The only file people edit by hand is PLAYBOOK.md.

## Core rules

1. **The script does the file work.** `scripts/kb_sync.py` (in this skill's folder) fingerprints, converts (pandoc, pdftotext, LibreOffice), mirrors, and tracks every document, and generates INDEX.md. Never open a PDF or Word file with the Read tool to transcribe pages that already have text.
2. **Claude reads only the pages the script lists.** When a JSON line has `claude_pages`, stage that source PDF into the sandbox and read only those pages with the Read tool's pages option (`all` means the whole PDF, used only when no text extraction tool is available). Replace each matching `<!-- KB-VISION page N -->` placeholder in the Markdown copy with the page's text, keeping headings and section numbers. This happens once per page. If a page cannot be read, leave its placeholder and tell the person which document and page, with the rais-help note.
3. **Read converted content only when the script says to.** A new document is read once, to write its index entry. A replaced document is read only through its diff. Nothing else is read.
4. **Index entries go through the script.** After reading a document, run `--set-entry` with its summary, consult-when, and key sections (and `--title` or `--type` if the script guessed wrong). Never edit INDEX.md; the script regenerates it.
5. **Playbook changes are proposals until a person approves them.** Write each proposed change as one file in `_admin/proposals/` (format below). Apply it to PLAYBOOK.md only after approval, then archive it with `--archive-proposal`. Never overwrite the person's own edits to PLAYBOOK.md.
6. **Nothing is deleted.** The script moves old copies into `_admin/retired/`. Do not use rm anywhere in the folder.
7. **Files go in the folder, not the chat.** If someone attaches a reference document in chat during a build, save it into their folder for them. A contract or redline attached for review is never saved into the folder.
8. **Work where the files are.** Run the script in the device shell. It needs `python3`; install `pandoc` or `poppler` (pdftotext) there if missing and allowed. If a converter cannot be installed, stage only the files that need it into the sandbox, convert them there, and commit the Markdown back. If no shell is available on the person's computer at all, say so plainly and give the rais-help note; do not convert documents by reading them whole.
9. **Never request folder access.** Cowork can only use a folder the person has dragged into the Claude window. Asking for a path or requesting access fails with an error. If the folder isn't connected, ask them to drag it in.

The rais-help note, whenever something needs RAIS, is a short message the person can send as it stands

> If you'd like RAIS to look at it, send this to rais-help@cornell.edu.
> > Subject: Knowledge base file won't convert
> > One file in my knowledge base didn't convert. <file name> (<what the script reported>). Thank you.

## Which mode

Run `python3 <script> --root "<connected folder>" --check` first.

- No folder connected → ask them to drag their knowledge base folder onto the chat, or go to **Create** if they are creating one.
- `no-kb` → **Create**.
- `legacy` → **Upgrade**, then continue as Update.
- Otherwise → **Update**. Also use Update for "check", "refresh", "sync", "continue my knowledge base", and "I changed some files". "Approve playbook changes" goes straight to **Approve**.

## Create

### Step 1, the folder

Say, as written, then ask the multiple-choice question (AskUserQuestion when available) with options Yes and No.

> Tip. If your team will share this knowledge base, keep its folder in SharePoint. Email rais-help@cornell.edu if you need help setting that up.
>
> **Do you already have a folder of reference files?**

- **Yes.** "Drag the folder onto this chat."
- **No.** "Make a new folder in Documents/Claude (Documents\Claude on Windows) and name it something like Contract Review KB. Put your reference files in it, then drag the folder onto this chat."

Do not continue until the folder shows as connected.

### Step 2, the purpose

Ask, with two options.

> **Will you use this knowledge base for contract review?**
> - Yes (I'll also build a playbook of your standard positions)
> - No (just questions and lookups)

Remember the answer; it decides whether Steps 4 and 5 write a playbook. Record it by writing `purpose: contract-review` or `purpose: reference` as the first line of `_admin/CHANGELOG.md` when the folder is created.

### Step 3, the files (no content reads)

List every file in the folder with type, size, and date. Do not open any file. Mark each as a reference document, an older version of another file, or not reference material (draft, redline, correspondence). Flag duplicates, version chains (v1, final, FINAL2), and probable scans. Say, in this form

> I found 34 files.
>
> - 28 look like reference documents (policies, standard agreements, guidance, prior agreements)
> - 4 look like older versions of other files
> - 2 look like drafts or redlines, which don't belong in a knowledge base
>
> Here's the full list with how I sorted each one. [table]
>
> Anything to change? If it looks right, say so and I'll continue.

Wait for the answer. Files that are not reference material are left where they are and excluded with `assign.tsv` (type `skip`), not moved. Mention once that they can delete them or leave them.

### Step 4, the playbook question (contract review only)

Ask, as written, with options Yes, No, and Not sure.

> **Do you have your own playbook?**
> A document listing your standard positions, what you can accept, and when to escalate, like a quick guide or cheat sheet. Not your standard contract.

- **Yes.** Ask which file.
- **No.** Continue.
- **Not sure.** Name the one to three files whose names suggest positions, fallbacks, guides, or cheat sheets and ask "Is either of these your playbook? You can also say neither, and I'll draft one from your documents."

Give that file the type `playbook` in `assign.tsv`.

### Step 5, convert

Write `assign.tsv` (path relative to the folder, a tab, a type such as policy, template, guidance, example, external, reference, playbook, or skip), then run

```
python3 <script> --root "<connected folder>" --apply --assign assign.tsv
```

Say "Converting your files now. This takes a few minutes." before running it. Read any `claude_pages` as core rule 2 describes. Then say

> Done. 31 files converted.

If anything is in `needs_attention`, add

> One file didn't convert, Old MTA scan.pdf. If you'd like RAIS to look at it, send this to rais-help@cornell.edu.
> > [the rais-help note]

Then say, and start without waiting

> Now I'm reading each document once to write your index and playbook. I'll let you know when it's ready.

(For a lookup-only knowledge base, "write your index".)

### Step 6, index and playbook (the one full read)

Work through every document the script lists as unindexed, in batches of ten. Read each Markdown copy once and run

```
python3 <script> --root "<folder>" --set-entry "docs/<path>.md" --summary "<two lines, what it covers and what it decides>" --consult "<the questions or clause types this answers>" --sections "<section names or numbers worth jumping to>"
```

Progress survives a cutoff, because an indexed document is marked in its own file. If the session ends, the next conversation that uses the folder sees what is unindexed and finishes it.

For contract review, then write `PLAYBOOK.md`, under roughly 5,000 tokens. If the person has their own playbook, start from it, keep its positions and wording where they are clear, and reconcile it against the other documents. Their playbook wins over other guidance unless a controlling standard says otherwise, and any conflict is marked `REVIEW`. Otherwise draft from the documents. Use these sections in this order.

1. **Context.** Who the organization is, which side it is usually on, typical counterparties and deal size, which agreement types the playbook covers and which it does not.
2. **How we review.** The process steps the office follows (read the whole agreement and exhibits first, check for protections the agreement omits, order findings by the agreement's section numbers, flag approvals or waivers that affect timing). Name the controlling standard, if any, and which sources win when they conflict.
3. **Positions by topic.** For each topic, the **standard position**, the **acceptable range** (what can be agreed without escalation), the **escalation trigger** and who it routes to, and the **source** as `docs/file.md § section`. Use exactly those labels; they are what the Legal plugin expects.
4. **Automatic escalation list.** Terms that always escalate.
5. **Escalation routing.** Who handles what.
6. **Negotiation tiers.** Must-haves, strong preferences, and concession candidates.
7. **Facts to confirm.** What to ask the PI, department, or requester before finalizing.

Default topics for sponsored research are effort standard, confidentiality, publication, export control, IP ownership, licensing, background IP, warranties, indemnification and liability, insurance, governing law and venue, financial terms, term and termination, use of name, survival and assignment, data terms (DUA), and material transfer terms (MTA). Where sources disagree, list both and mark the line `REVIEW`. Do not pick a winner.

Then present the playbook and every REVIEW line as choices, in this form, and wait.

> Your playbook is ready [here](<path to PLAYBOOK.md>). Look it over when you like.
>
> Three places where your documents disagree. Pick one for each.
>
> **1. Publication review period**
> ○ 30 days (Fallback Language.docx)
> ○ 60 days (SRA Quick Guide 2025.docx)
>
> Answer with the numbers, like "1 first, 2 second," or tell me in your own words.

Apply their choices, remove the REVIEW marks, and confirm in one line, for example "Done. Your playbook now says 60 days, silent on governing law is acceptable, and no indemnification cap."

### Step 7, wire it up and finish

Write `CLAUDE.md` at the top of the person's folder (append a "Knowledge base" section if one exists).

```
# Knowledge base

This folder is a knowledge base. Claude's working files are in "Claude files (Claude manages)".
Once per conversation, the first time this folder is used, run
  python3 "Claude files (Claude manages)/_admin/kb_sync.py" --root "<this folder>" --check
from a shell on the computer that holds this folder. It takes under a second and reads no documents.
If it reports changes, say how many files changed and offer to update the knowledge base. If it reports
pending proposals, say how many playbook changes are waiting and offer to review them. If it reports
current and nothing waiting, say nothing. If no shell is available, skip it.
To answer a question, use "Claude files (Claude manages)/INDEX.md" to pick the one or two documents to open,
or search the text under "Claude files (Claude manages)/docs/" for exact wording. Cite the document and section.
If the documents don't cover something, say so rather than guessing.
Never list or scan the docs folder, and never open "_admin/".
Write working output (reviews, findings, drafts) to the matter's own folder, never into this one.
```

For contract review, add these lines to CLAUDE.md and also write `legal.local.md`.

CLAUDE.md addition
```
"Claude files (Claude manages)/PLAYBOOK.md" is the only playbook and knowledge source for contract work here.
Any skill that asks for a playbook, standard positions, or policies uses it instead of a playbook bundled with
a plugin or generic defaults. Read it in full at the start of a review or a question about our positions.
If the playbook is silent on a topic, say so. If more than one knowledge base is connected, read each playbook;
where they conflict, the personal one wins and the conflict is noted.
```

`legal.local.md`
```
# Playbook

The playbook for review-contract, triage-nda, legal-risk-assessment, and legal-response is
"Claude files (Claude manages)/PLAYBOOK.md" in this folder. Read it in full. It defines standard positions,
acceptable ranges, and escalation triggers. For exact wording, look the document up in
"Claude files (Claude manages)/INDEX.md" and open only the docs/ file named there. Do not use any other playbook.
```

Then finish with this message, using Finder or File Explorer as the platform dictates. Drop the contract sentence for a lookup-only knowledge base.

> Your knowledge base is ready to use.
>
> Start a new chat and drag this folder from Finder onto it, or use the Add folder button. Then ask a question, or attach a contract and ask me to check it.
>
> To update it, just add or remove files in your folder in Finder. I'll pick up the changes next time you use it.
>
> Want to share it with colleagues? Put the folder in SharePoint, and anyone who connects it gets the same knowledge base. Ask me for tips, or email rais-help@cornell.edu for help setting it up.

If they ask for tips, give three. Move the folder into SharePoint and connect it from there. Set it to always keep files on this device. Give edit access only to the few people who will add documents.

## Update

The check at the start of a conversation (see CLAUDE.md above) finds changes and pending proposals. The person can also ask at any time.

1. Run `--plan`. It changes nothing.
2. Say what it found in plain language, one line per document (new, replaced, removed, moved or renamed). If nothing changed and nothing is waiting, say the knowledge base is up to date and stop. Otherwise say "Update now? It takes a minute." and wait.
3. Run `--apply`. For each JSON line, do what its `next` field says.
   - **added**. Read the Markdown copy once, `--set-entry`, and if the document changes a position, write a proposal.
   - **changed**. Read only the diff. `--set-entry` if the summary, scope, or date changed. Search PLAYBOOK.md for lines citing the file and write a proposal for any the diff affects.
   - **removed**. Search PLAYBOOK.md for lines citing the file and write a proposal for each (drop the line, cite another source, or keep it).
   - **moved**. Nothing to read. If the file name changed, update PLAYBOOK.md citations.
   - **claude_pages** on any line. Read those pages first, as core rule 2 describes.
   - **needs_attention**. Tell the person which file and why, with the rais-help note.
   - **conflict-resolved**. Nothing to do; the script tidied duplicate copies. If the check reports `playbook_conflicts`, show the person the differences between PLAYBOOK.md and the conflicted copy, ask which to keep, then move the other into `_admin/retired/` with mv.
4. Also finish any document the check lists as unindexed (a build that was cut off) with `--set-entry`.
5. If proposals were written, say "N playbook changes are proposed. Review them now, or later?" Now goes to Approve; later gets "OK. Say 'approve playbook changes' whenever you're ready."

### Proposal files

One file per change in `_admin/proposals/`, named `<date>-<topic slug>.md`.

```
# Proposal: <one line>
Source: docs/<file>.md § <section>, added <date>
Topic: <playbook topic>

## Current playbook text
<the exact lines, or "none, this is new">

## Proposed text
<the replacement lines>

## Why
<one or two sentences>
```

## Approve

For each file in `_admin/proposals/` (not its subfolders), show the current text, the proposed text, and why, then ask "Apply, skip for now, or decline?" On apply, edit PLAYBOOK.md with the proposed text and run `--archive-proposal <name> --as applied`. On decline, `--as declined`. On skip, leave it. End with one line, for example "Applied 2, declined 1."

## Upgrade

A folder built by version 0.9 has a "Source files (you manage)" subfolder and `_admin/MANIFEST.json`. Say "Your knowledge base was built by an earlier version. I'll move it to the new layout, which keeps everything and changes nothing in your documents." Run `--upgrade`. It moves the documents up into the folder, writes each record and index entry into its document's copy, retires the manifest and old index, and regenerates INDEX.md. Rewrite `CLAUDE.md` and `legal.local.md` as in Step 7 (contract review if `legal.local.md` existed). Then continue as Update. If the output lists collisions, tell the person which files were left in the old subfolder because a file with the same name already existed.

## What not to do

- Do not read documents to convert them, and do not read converted copies except as Step 6 and Update direct.
- Do not read INDEX.md or PLAYBOOK.md in full during Update; search for the lines you need.
- Do not edit INDEX.md; the script generates it.
- Do not change PLAYBOOK.md without an approved proposal, except to apply the person's own answers in Step 6.
- Do not move, rename, or delete the person's files.
- Do not mention "Claude files (Claude manages)", proposals, records, or sync in messages to the person unless they ask how it works.
- Do not review contracts or answer questions here; that is the Legal plugin's or the ask skill's job.
- Do not copy knowledge base content into any plugin, skill, or shared repository.
