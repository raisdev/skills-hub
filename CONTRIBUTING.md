# Contributing to the Skills Hub

Everything here ships to real machines the day it is merged, so the bar is "would I be comfortable with every research administrator at Cornell running this tomorrow." Most contributions are a folder of Markdown. You do not need to be a developer.

## Ways to contribute, easiest first

**File an issue.** Request a plugin, share an idea, report a bug. Use the forms under Issues, New issue. No git needed.

**Improve an existing plugin.** Edit a `SKILL.md` on GitHub (pencil icon), which opens a pull request for you. Bump `version` in that plugin's `.claude-plugin/plugin.json`.

**Add a plugin.** Copy `plugins/_template` to `plugins/<owner>-<name>`, fill in `plugin.json`, `README.md` and your skills, open a pull request. The validator runs automatically and tells you what is missing.

**Start something in the incubator.** Same layout under `incubator/<owner>-<name>`. It appears on the catalog as in development and is not installed anywhere. Move it to `plugins/` and add it to `marketplace.json` when it is ready.

## What a plugin needs

- `.claude-plugin/plugin.json` with `name` (same as the folder, lowercase, hyphens), `version` (semver), `description` (one or two sentences a user can act on), `author`.
- `README.md` saying what it does, who maintains it, which connectors it needs, and any caveats.
- At least one `skills/<skill>/SKILL.md` with YAML front matter `name` and `description`. The description is what triggers the skill, so write it as "use when the user asks about X, Y, Z," not as marketing.
- No secrets, keys, personal data, or internal-only documents. This repo is public. Playbooks with negotiation positions or anything you would not email to a stranger stay out; a plugin can reference an internal SharePoint page instead.
- Keep it small. Under 2 MB per plugin. Large reference sets belong in a knowledge base the skill points to, not in the repo.

## Review and ownership

`main` is protected. Every pull request needs one approving review from the owners named in `.github/CODEOWNERS`. RAIS owns the repo as a whole; a department that maintains its own plugins gets a CODEOWNERS line for its folder pattern (for example `/plugins/oria-*/`) so its own reviewers approve changes there, with RAIS still able to review before merge.

To get a department folder, open the "Publish our unit's plugins" issue. RAIS adds the CODEOWNERS line and a GitHub team for your reviewers.

## Naming

`<owner>-<purpose>`, all lowercase. Owner is the unit abbreviation (`rais`, `osp`, `oria`, `ctl`, `cares`) and purpose is one or two words. The prefix shows up in the app, so users can tell whose plugin it is.

## Versions and updates

Bump `version` in `plugin.json` on every change that users would notice. Claude Desktop re-syncs on launch and periodically, so a merge reaches machines within a day. If a change turns out to be bad, revert the merge; the revert ships the same way.

## Testing before you open a PR

Zip your plugin folder and upload it in Claude Desktop under Settings, Plugins, as a personal plugin. Try the skills in a Cowork session. That is the same thing users will get. Uninstall your personal copy after the hub version ships so you do not end up with two.

## Skill writing tips

- One skill, one job. Split when a description starts saying "and also."
- Put the trigger phrases users actually say into `description`.
- Under 500 lines of instructions. Move long reference material to separate files in the skill folder and tell the skill when to read them.
- Say what the skill should not do and when to hand off to a person.
- Prefer plain language over jargon in anything the user will read.
