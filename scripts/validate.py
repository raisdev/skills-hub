#!/usr/bin/env python3
"""Checks the hub before anything ships. Runs on every pull request and push.

Fails the build when:
  - .claude-plugin/marketplace.json is missing, invalid, or has the wrong name
  - a listed plugin folder is missing, or its plugin.json name differs from the folder
  - a plugin (published or incubator) lacks plugin.json, README.md, or a SKILL.md with front matter
  - a SKILL.md front matter lacks name or description
  - a file looks like a secret (API keys, private keys) or is larger than MAX_FILE_BYTES
  - a plugin is larger than MAX_PLUGIN_BYTES
Warns (does not fail) when a plugin folder exists under plugins/ but is not listed.
"""
import json, os, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_NAME = "rais-skills-hub"        # must match allowedPluginMarketplaces expectedName on machines
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_PLUGIN_BYTES = 5 * 1024 * 1024
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
SECRET_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "looks like an API key (sk-...)"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "looks like an AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}"), "GitHub token"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
]
TEXT_EXT = {".md", ".json", ".txt", ".yml", ".yaml", ".py", ".js", ".sh", ".ps1", ".cmd", ".csv", ".html"}

errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

def load_json(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"{p.relative_to(ROOT)}: invalid JSON ({e})")
        return None

def front_matter(p):
    txt = p.read_text(encoding="utf-8", errors="replace")
    if not txt.startswith("---"):
        return None
    end = txt.find("\n---", 3)
    if end < 0:
        return None
    fm = {}
    for line in txt[3:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm

def check_plugin(folder, listed_name=None):
    rel = folder.relative_to(ROOT)
    pj = folder / ".claude-plugin" / "plugin.json"
    if not pj.exists():
        err(f"{rel}: missing .claude-plugin/plugin.json"); return
    meta = load_json(pj)
    if meta is None: return
    name = meta.get("name", "")
    if not NAME_RE.match(name):
        err(f"{rel}: plugin.json name '{name}' must be lowercase letters, digits and hyphens")
    if name != folder.name:
        err(f"{rel}: plugin.json name '{name}' does not match folder name '{folder.name}'")
    if listed_name and name != listed_name:
        err(f"{rel}: marketplace.json lists it as '{listed_name}' but plugin.json says '{name}'")
    for key in ("version", "description"):
        if not meta.get(key):
            err(f"{rel}: plugin.json is missing '{key}'")
    if not (folder / "README.md").exists():
        err(f"{rel}: missing README.md")
    skills = list((folder / "skills").glob("*/SKILL.md")) if (folder / "skills").exists() else []
    if not skills and not (folder / ".mcp.json").exists():
        err(f"{rel}: no skills/<name>/SKILL.md and no .mcp.json; nothing to ship")
    for s in skills:
        fm = front_matter(s)
        srel = s.relative_to(ROOT)
        if fm is None:
            err(f"{srel}: missing YAML front matter (--- name / description ---)"); continue
        if not fm.get("name"): err(f"{srel}: front matter needs 'name'")
        if not fm.get("description"): err(f"{srel}: front matter needs 'description'")
        elif len(fm["description"]) < 40: warn(f"{srel}: description is short; say when to use the skill")
    total = 0
    for f in folder.rglob("*"):
        if f.is_file():
            size = f.stat().st_size
            total += size
            if size > MAX_FILE_BYTES:
                err(f"{f.relative_to(ROOT)}: {size // 1024} KB exceeds the {MAX_FILE_BYTES // 1024} KB per-file limit")
            if f.suffix.lower() in TEXT_EXT:
                txt = f.read_text(encoding="utf-8", errors="replace")
                for pat, label in SECRET_PATTERNS:
                    if pat.search(txt):
                        err(f"{f.relative_to(ROOT)}: {label}; remove it, this repo is public")
    if total > MAX_PLUGIN_BYTES:
        err(f"{rel}: plugin is {total // 1024} KB, over the {MAX_PLUGIN_BYTES // 1024} KB limit")

def main():
    mp = ROOT / ".claude-plugin" / "marketplace.json"
    if not mp.exists():
        err("missing .claude-plugin/marketplace.json"); report(); return
    cat = load_json(mp)
    if cat is None: report(); return
    if cat.get("name") != EXPECTED_NAME:
        err(f"marketplace.json name is '{cat.get('name')}', machines expect '{EXPECTED_NAME}'")
    listed = {}
    for p in cat.get("plugins", []):
        src = p.get("source", "")
        if not isinstance(src, str) or not src.startswith("./plugins/"):
            err(f"marketplace.json: plugin '{p.get('name')}' source must be a relative ./plugins/<name> path"); continue
        folder = ROOT / src[2:]
        if not folder.is_dir():
            err(f"marketplace.json: plugin '{p.get('name')}' points at missing folder {src}"); continue
        listed[folder.name] = p.get("name")
        if p.get("name") != folder.name:
            err(f"marketplace.json: plugin '{p.get('name')}' should be named after its folder '{folder.name}'")
        check_plugin(folder, p.get("name"))
    plugins_dir = ROOT / "plugins"
    for folder in sorted(plugins_dir.iterdir()) if plugins_dir.exists() else []:
        if folder.is_dir() and not folder.name.startswith("_") and folder.name not in listed:
            warn(f"plugins/{folder.name} exists but is not listed in marketplace.json (it will not ship)")
    inc = ROOT / "incubator"
    for folder in sorted(inc.iterdir()) if inc.exists() else []:
        if folder.is_dir():
            check_plugin(folder)
            if folder.name in listed:
                err(f"incubator/{folder.name} is also listed in marketplace.json; pick one")
    report()

def report():
    for w in warnings: print(f"WARN  {w}")
    for e in errors: print(f"ERROR {e}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
