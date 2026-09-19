# Cornell Research & Innovation Skills Hub

Plugins and skills for Claude Desktop, published by RAIS and the units of Research & Innovation. Anything merged to `main` reaches every Cornell gateway machine on its own; there is no install step for RAIS and no visit from a tech.

**Catalog and requests:** https://raisdev.github.io/skills-hub (built from this repo on every push)

## Using a plugin

1. Open Claude Desktop, then Settings, Plugins, Organization.
2. Pick the **RAIS Skills Hub** tab.
3. Install the plugins you want. Skills inside them become available in Cowork and Chat right away.

Nothing installs on its own from this hub. If a plugin you expect is missing, check that your PC has been set up for marketplaces (RAIS did this in the v1.0.23 installer and with a one-time update on older machines) and that you have fully quit and reopened Claude Desktop since.

## Asking for something

Use the issue forms. They take a minute and they are how ideas get seen.

- **Request a plugin or skill** for something you do often.
- **Share an idea** even if you are not sure it is a plugin yet.
- **Report a problem** with a plugin from this hub.
- **Publish our unit's plugins**, if your department wants to maintain its own folder here.

Reactions (thumbs up) on an issue count as votes. The catalog page shows open requests and what is in development.

## Contributing a plugin

Read [CONTRIBUTING.md](CONTRIBUTING.md). The short version: copy `plugins/_template`, put your skills in it, open a pull request. RAIS reviews and merges. A department folder can have its own reviewers, so your team can approve its own changes while RAIS keeps a final look before anything ships.

Work in progress lives under `incubator/`. It shows on the catalog as "in development" and is never installed on anyone's machine until it moves to `plugins/` and is listed in `.claude-plugin/marketplace.json`.

## Layout

```
.claude-plugin/marketplace.json   the catalog Claude Desktop reads (only plugins listed here ship)
plugins/<name>/                   one plugin per folder; skills live inside plugins
  .claude-plugin/plugin.json      name, version, description
  README.md                       what it does, who owns it, how to use it
  skills/<skill>/SKILL.md         one folder per skill
  .mcp.json                       optional MCP connectors
incubator/<name>/                 same layout, not yet listed, shown as in development
submodules/<name>/                vendored external plugin repos, checked in directly, merged into the catalog
site/                             catalog page builder (GitHub Pages)
scripts/validate.py               checks every PR: manifests, names, secrets, size
scripts/merge_submodule_plugins.py  merges a submodule's marketplace into the root
scripts/vendor_subtree.py         pulls a forked repo into submodules/ as a git subtree
```

Plugin names carry their owner as a prefix, for example `rais-ecfr`, `osp-agreements`, `oria-protocols`, so ownership is obvious in the app and in CODEOWNERS.

### Vendoring external plugin repos

External repos (currently a fork of the Anthropic knowledge-work plugin marketplace) are checked in directly under `submodules/` so Claude Desktop loads them without any extra clone commands. To add or update them:

```bash
python3 scripts/vendor_subtree.py
```

First run vendors the repo with `git subtree add`; later runs pull the latest with `git subtree pull` and merge any local changes, so this repo's history stays flat.

### Merging submodule plugins

When you add or update a submodule that has its own `.claude-plugin/marketplace.json`, merge its plugins into the root catalog:

```bash
python3 scripts/merge_submodule_plugins.py submodules/<submodule-name>
```

The script adjusts local source paths. A submodule plugin that has the same name as an existing root plugin overwrites it.

### Validating the hub

Run the validator before pushing — it runs on every pull request and push, so catching problems locally saves a failed build:

```bash
python3 scripts/validate.py
```

It fails (exit 1) when the marketplace is missing, invalid, or named wrong; a listed plugin folder is missing or its `plugin.json` name differs from the folder; a plugin (published or incubator) lacks `plugin.json`, `README.md`, or a skill with front matter; a `SKILL.md` lacks `name`/`description`; a file looks like a secret or is over the per-file limit; or a plugin is over the total size limit. It only warns when a folder under `plugins/` is not listed in the marketplace.

## How machines get it

Cornell gateway installs of Claude Desktop carry a managed policy value, `allowedPluginMarketplaces`, that names this repository on branch `main`. Claude Desktop clones it with git at launch and re-fetches periodically. Because the entry is `available` rather than auto-install, users choose what to install, and because it follows `main`, a merged pull request is live everywhere within a day. That is also why `main` is protected and every change gets a review.

Maintained by Cornell RAIS. Questions to rais@cornell.edu.
