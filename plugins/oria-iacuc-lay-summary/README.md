# oria-iacuc-lay-summary

Helps Cornell principal investigators write or improve the lay summary of an IACUC animal use protocol. Paste a specific aim, abstract, grant Vertebrate Animals section, syllabus or experimental design, or just describe the animal work, and Claude drafts a 1 to 2 paragraph summary a non-scientist can follow. It also trims long summaries, moving detail that belongs elsewhere out of the lay summary.

**Owner** Cornell ORIA, with content maintained by the IACUC office. **Status** published. **Version** 0.1.0. Questions, corrections and update requests go through the issue forms at https://github.com/raisdev/skills-hub/issues.

## What is inside

- Skill `iacuc-lay-summary`: drafts, starts, shortens or improves a lay summary. It triggers when someone asks for help with a lay summary or pastes grant text, specific aims or experimental design. It:
  - asks for source material first, and asks for the species if only a general term ("rodents", "fish") is given
  - adapts the format to the research type: biomedical or agricultural, teaching, or wildlife
  - treats trimming as its main job, and frames each cut as "belongs in another section" (animal numbers, dosages, detailed methods, statistics, budget, personnel, timelines)
  - keeps session notes of those cut details and hands them back, organized by protocol section, when asked
  - ends every draft with a reminder to review it for misinterpretations

## How to use

Start a conversation and paste plain text from your protocol materials. Plain text pasted into chat works best; avoid Word documents or PDFs. You can also describe your animal work and let Claude ask for what it needs.

## Connectors needed

None.

## Caveats

- **The output is a draft, not an IACUC determination.** The PI is responsible for reviewing it for accuracy before it goes into a protocol. Final review and approval of the protocol stays with the IACUC.
- **It never asks for or adds animal numbers, dosages or methodology detail.** Those belong in other protocol sections. If you need them, use the session notes, or write them into the right section yourself.
- **It works only from what you paste.** It does not read your protocol or any Cornell system, and it does not check your text against IACUC policy.
- **The skill triggers on lay summary requests and on pasted grant text, specific aims or experimental design.** If it triggers when you did not want it to, say so in the chat and carry on.
