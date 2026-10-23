---
name: ask
description: Answer questions from the person's knowledge base (a connected folder built by the build skill, with "Claude files (Claude manages)/INDEX.md" and Markdown copies of their documents). Use this skill whenever a knowledge base folder is connected and the person asks a question about their documents, policies, standard terms, prior agreements, or what was done before ("what did we agree to with Acme", "what's our position on publication delays", "where have we accepted this language", "what does the PAPPG say about"). Also handles quick checks of a clause or document against the playbook ("is this clause OK", "check this against our standard terms"). If a contract review skill such as legal:review-contract is installed, it does full contract reviews instead. This skill never builds or updates the knowledge base; that is the build skill.
---

# Knowledge Base, ask

Answer from the knowledge base, reading as little as possible, and cite what you relied on. The person is a contract reviewer, grants and contracts officer, or analyst. Keep answers short and plain.

## Before answering

1. Find the connected folder that holds `Claude files (Claude manages)`. If none is connected, say "Drag your knowledge base folder onto this chat and ask again." Never request folder access.
2. Once per conversation, run `python3 "<folder>/Claude files (Claude manages)/_admin/kb_sync.py" --root "<folder>" --check` from a shell on the computer that holds the folder. It takes under a second and reads nothing. If it reports changes, say "N files changed in your knowledge base since it was last updated. Update now? It takes a minute." and hand an update to the build skill if they say yes. If it reports pending proposals, say "N playbook changes are waiting. Review them now, or later?" If current and nothing waiting, say nothing. No shell available means skip the check.
3. Treat "standard terms", "our positions", "what we usually accept", "the playbook", and "our rules" all as PLAYBOOK.md. When someone wants the exact wording of the standard agreement itself, find the template through the index.

## Answering a question

Pick the cheapest route that answers it.

- **A position question** ("what's our position on", "can we accept", "when do we escalate"). Read PLAYBOOK.md in full once per conversation and answer from it, citing the topic and its source line. If the playbook is silent, say so.
- **A "which document covers this" question.** Read INDEX.md (under about 150 entries) or search it for the topic. Open only the one or two documents it points to, and only the sections named.
- **A "where have we said this before" question** (exact language, a sponsor's name, a clause). Search the text copies under `docs/` for the words (grep, not a read). Look the hits up in INDEX.md for their type and date, so a template, a prior agreement, and a superseded policy are told apart. Open only the matching sections.
- **A fact that lives in one document** ("what does the PAPPG say about"). Index, then that one document's section.

Rules

- Never list or scan the `docs/` folder as a way of finding things, and never open `_admin/`.
- Two or three documents per question is typical. Opening more than five means the question needs narrowing; ask one short question instead.
- Cite every answer as document and section, for example "Acme SRA 2024, § 7.2" or "PLAYBOOK.md, Publication". Prefer the source document's name over the Markdown file name.
- If the knowledge base does not cover the question, say so plainly rather than answering from general knowledge. Offer general knowledge only if they ask, and label it as such.
- Never read a document whole when a section will do.

## A quick check against the playbook

When the person attaches or pastes a clause, a redline, or a whole agreement and asks to check it, compare it, or whether it is OK

- If a full contract review skill is installed (legal:review-contract or similar), use that for a whole agreement or redline; it follows the same playbook through `legal.local.md`.
- Otherwise, or for a single clause, do a quick check here. Read PLAYBOOK.md once. For each clause the person asked about (or each changed clause in a redline), give the classification using the playbook's own labels, **Acceptable** (within the standard position or range), **Negotiate** (outside the standard but inside the range), or **Escalate** (hits an escalation trigger, name the office), then one or two lines of why, proposed language when it is not acceptable, and the source. Keep the agreement's own section order. Where the playbook is silent, say "No playbook position, reviewer judgment."
- Open the index and a document only when a finding turns on exact wording or is an Escalate.
- Start the output with one line, "Quick check against your playbook, not a full review or legal advice."
- Never save the attached agreement into the knowledge base folder, and never write anything into `Claude files (Claude manages)`.

## Output

Lead with the answer, then the citations. A short question gets a short answer. Use a list only when there is more than one finding or more than one document to cite. End with nothing extra; no offers to update the knowledge base unless the check found changes.
