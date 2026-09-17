# One-time repo setup (RAIS)

Not part of the hub content. Delete this file after doing the steps, or keep it as the runbook.

1. Unzip `skills-hub-scaffold.zip` (next to this folder) into your clone of github.com/raisdev/skills-hub, replacing the stub README. Use the zip, not the loose folder: the loose copy in 3P Installer is missing `.github/` and `plugins/rais-ecfr/.mcp.json` because the Claude desktop bridge refuses to write those paths (they are in the zip and in `_github/` and `mcp.json.txt` as plain copies). Commit and push to main. The `_template` plugin folder is skipped by the validator (leading underscore) and is not listed, so it never ships.
2. Settings > General > Features: turn on Issues (already on) and Discussions if you want a looser channel. Leave the repo public; the machines fetch it anonymously.
3. Settings > Pages > Build and deployment > Source: **GitHub Actions**. The `Publish catalog` workflow then deploys on every push to main. First URL will be https://raisdev.github.io/skills-hub. If the org already has a Pages site, the path is the same.
4. Teams (org Settings > Teams): create `rais-reviewers` with the RAIS people who review. Create one team per unit as they onboard (`osp-reviewers`, `oria-reviewers`) and add the matching CODEOWNERS lines.
5. Settings > Branches > Add rule for `main`: require a pull request before merging, require 1 approval, require review from Code Owners, require status checks to pass (`validate`), dismiss stale approvals. Do not allow force pushes.
6. Labels (Issues > Labels): `plugin-request`, `idea`, `bug`, `unit-onboarding`, `in-development`, `published`. The issue forms apply the first four on their own. Move a request to `in-development` when someone starts on it; the catalog page groups by label.
7. Test the machine side: on a v1.0.23 box (or one where Enable Claude Plugin Marketplaces.cmd ran), fully quit and reopen Claude Desktop, then Settings > Plugins > Organization should show a "RAIS Skills Hub" tab listing rais-ecfr. The marketplace `name` here (`rais-skills-hub`) must stay equal to `expectedName` in the machines' policy; the validator enforces the repo side.

## Everyday flow

- New plugin: PR adding `plugins/<owner>-<name>/` and one entry in `.claude-plugin/marketplace.json`. Merge. Live within a day.
- Change: PR editing files under the plugin, bump `version`. Merge.
- Retire: remove the marketplace.json entry (and the folder if you like). Claude Desktop uninstalls it from machines on the next sync.
- Something in progress the community should see: put it under `incubator/`. It shows on the catalog and installs nowhere.
- Department wants in: they file the "Publish our unit's plugins" issue; RAIS creates the team and the CODEOWNERS line; they PR into `plugins/<prefix>-*`.

## Things to decide later

- Whether to require sign-off from a second person for `.claude-plugin/marketplace.json` changes specifically (that file is the only thing that changes what ships).
- A LICENSE. Without one, others technically cannot reuse the skills. MIT or CC BY 4.0 would be the usual choices for prompt content; Cornell counsel may have a view.
- Whether the legal-for-osp plugin (with the OSP playbook inside) belongs here at all. As built it contains negotiation positions; if OSP wants it in the hub, strip the playbook out and have the skill read it from an internal location instead.
