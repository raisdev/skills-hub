# Knowledge Base

Knowledge Base turns a folder of your documents into something Claude can answer questions from. For contract review, it also writes a playbook of your standard positions that the Legal plugin follows. Your documents stay in your folder on your computer, and the folder can be shared with colleagues through SharePoint. Because Claude reads a short index or playbook instead of every document, work is faster and sessions stop running out of budget.

**Owner** Cornell RAIS, contact rais-help@cornell.edu. **Version** 0.10.0. **Connectors needed** None.

## Steps

1. **Install.** In Claude, go to Customize, Plugins, Organization, RAIS, and install Knowledge Base. For contract review, also install Legal from the same place, and turn off Legal for OSP if you have it.
2. **Create your knowledge base (once).** Say **"create my knowledge base."** Claude asks whether you already have a folder of reference files. If yes, drag it onto the chat. If not, make a folder, put your files in it, and drag it onto the chat. Claude asks whether it's for contract review, lists your files so you can confirm which belong, converts them, and writes the index. For contract review it also drafts the playbook and asks you to settle any places where your documents disagree.
3. **Use it.** Start a new chat and drag the folder onto it (or use the Add folder button). Then ask a question, or attach a contract and ask Claude to check it.
4. **Keep it current.** Add, replace, or remove files in your folder the way you would in any folder. The next time you use the knowledge base, Claude notices and offers to update it. You can also say **"update my knowledge base."** Claude shows you what changed and asks before changing your playbook.

## Sharing with colleagues

Put the folder in SharePoint, and anyone who connects it gets the same knowledge base. Three tips. Connect the folder from SharePoint on your computer, not from a network drive. Set the folder to always keep files on this device. Give edit access only to the few people who will add documents; everyone else can read. Email rais-help@cornell.edu for help setting it up.

## Additional detail

**Playbook changes.** When a new or replaced document affects a position, Claude writes a proposed change and waits. The next person who uses the knowledge base and can edit it is told that changes are waiting and can say **"approve playbook changes."** Nothing changes in the playbook until someone approves it.

**Replacing a file.** Save the new version over the old one with the same name, and Claude shows you exactly what changed and which playbook lines it affects. A new name works too, but shows up as one document removed and another added.

**Drafts.** Keep drafts and redlines out of your knowledge base, or put them in a subfolder whose name starts with an underscore, like **_drafts**. Those are ignored.

**Nothing is deleted.** Removed and replaced documents are kept in a retired folder inside Claude's subfolder, and you can clear it whenever you like.

**Scanned PDFs.** Pages that are images are read by Claude once, when the file is added, and the text is saved so they are never read again. If a page can't be read, Claude tells you and gives you a note to send to rais-help@cornell.edu.

**Personal and shared.** You can connect a shared knowledge base and your own at the same time. Claude reads both playbooks, and where they disagree your personal one wins and Claude points out the conflict.

**Earlier versions.** A knowledge base built by version 0.9 is moved to the new layout the first time you use it. Nothing in your documents changes.

**Not legal advice.** Reviews and checks are an aid for your own review.

## Under the hood

The expensive part of using Claude with reference material is Claude reading documents, so the design reads each document once and never again unless it changes. Everything else (converting files, spotting changes, building the index) is done by a script on the person's computer, which costs no tokens.

1. **The person's folder is the knowledge base.** They add, replace, and remove files like any folder. The plugin keeps one subfolder, `Claude files (Claude manages)`, which its messages never mention.
2. **The script makes the text copies.** `kb_sync.py` converts each document to Markdown in `docs/`, mirroring the person's folders. Word and HTML go through pandoc, legacy `.doc` through LibreOffice, and PDFs through pdftotext page by page. A PDF page with no text layer is marked for Claude, which reads just that page once and saves the text.
3. **Each copy carries its own record.** The copy's front matter holds the source path, document type, date, fingerprint (SHA-256), size, and modified time, plus the index entry Claude writes after reading it (summary, consult when, key sections). There is no manifest.
4. **INDEX.md is generated.** The script assembles it from the records in milliseconds whenever one changes. Nobody edits it.
5. **The playbook is the one hand-edited file.** Claude writes `PLAYBOOK.md` for contract review, with Context, How we review, Positions by topic (standard position, acceptable range, escalation trigger, source), the automatic escalation list, routing, negotiation tiers, and facts to confirm. Those labels are what the Legal plugin expects. Later changes are written as one proposal file each in `_admin/proposals/`, and applied only when a person approves.
6. **Each conversation checks once.** The first time a conversation uses the folder, `CLAUDE.md` has Claude run `kb_sync.py --check`. It compares the files in the folder with the records (a file whose size and date match its record is not reread), counts documents waiting to be indexed, pages waiting for Claude, pending proposals, and duplicate copies, and prints one line. Under a second for a few hundred documents.
7. **Updates touch only what changed.** A new file is converted, read once, and given an entry. A replaced file is converted again and Claude reads only a diff. A removed file's copy moves to `_admin/retired/`. A moved or renamed file has its record corrected without being reread.

**Why it is safe to share.** No two people ever write the same file. Each document's record lives in that document's copy, the index is regenerated from the records, and playbook changes are separate proposal files. If a sync app still makes a "conflicted copy" of a generated file, the script keeps the copy whose fingerprint matches the document in the folder and retires the other, with no questions asked. A conflicted copy of the playbook is the one case that needs a person, and Claude shows the two versions and asks which to keep. There are no locks, nothing runs in the background, and reading never waits.

**What must be true on the person's computer.** The script runs in Cowork's own workspace on the person's computer, which needs `python3`, plus `pandoc`, `pdftotext` (poppler), and LibreOffice for the formats that use them. Confirmed on a RAIS Mac; the locked-down Cornell Windows test, including a SharePoint folder shared by two people, must pass before rollout. If a converter is missing, Claude converts those files in its cloud workspace instead.

**Script usage.** `kb_sync.py --root <folder>` with `--check`, `--plan`, `--apply [--assign assign.tsv]`, `--set-entry <copy> --summary --consult --sections [--title] [--type]`, `--index`, `--archive-proposal <name> --as applied|declined`, or `--upgrade`. `--full` forces a fingerprint of every file.

**Where this plugin lives.** `incubator/rais-kb/` in the raisdev/skills-hub repo until it is promoted to `plugins/rais-kb/`. Changes go through testing with an uploaded copy, then the incubator, then a code review, then `plugins/`. Bump `version` in `.claude-plugin/plugin.json` on every change. Nothing from anyone's knowledge base ever goes into the repo.
