#!/usr/bin/env python3
"""Merge plugins from a submodule marketplace into the root marketplace.

Usage: python scripts/merge_submodule_plugins.py <submodule-path>

Example:
  python scripts/merge_submodule_plugins.py submodules/anthropic-work-plugins

Fails when:
  - submodule path doesn't exist or lacks .claude-plugin/marketplace.json

Plugins with a name already in the root marketplace are overwritten by the
submodule's version.
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

def load_json(p):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: {p}: invalid JSON ({e})")
        sys.exit(1)

def adjust_source(plugin, submodule_rel):
    """Adjust local ./ paths to point into the submodule."""
    source = plugin.get("source")
    if isinstance(source, str) and source.startswith("./"):
        plugin = plugin.copy()
        plugin["source"] = f"./{submodule_rel}/{source[2:]}"
    return plugin

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/merge_submodule_plugins.py <submodule-path>")
        print("Example: python scripts/merge_submodule_plugins.py submodules/anthropic-work-plugins")
        sys.exit(1)

    submodule_path = pathlib.Path(sys.argv[1])
    submodule_abs = (ROOT / submodule_path).resolve()
    
    if not submodule_abs.is_dir():
        print(f"ERROR: submodule path does not exist: {submodule_path}")
        sys.exit(1)

    sub_marketplace = submodule_abs / ".claude-plugin" / "marketplace.json"
    if not sub_marketplace.exists():
        print(f"ERROR: submodule missing .claude-plugin/marketplace.json: {submodule_path}")
        sys.exit(1)

    root_marketplace = ROOT / ".claude-plugin" / "marketplace.json"
    if not root_marketplace.exists():
        print(f"ERROR: root missing .claude-plugin/marketplace.json")
        sys.exit(1)

    # Load both marketplaces
    root_data = load_json(root_marketplace)
    sub_data = load_json(sub_marketplace)

    root_plugins = root_data.get("plugins", [])
    sub_plugins = sub_data.get("plugins", [])

    # Check for overwrites
    existing = {p.get("name") for p in root_plugins}
    overwritten = [name for name in (p.get("name") for p in sub_plugins) if name in existing]
    for name in overwritten:
        print(f"Overwriting plugin '{name}'")

    # Compute relative path from ROOT to submodule
    submodule_rel = submodule_abs.relative_to(ROOT)

    # Adjust paths; submodule entries replace same-named root entries
    adjusted = [adjust_source(p, submodule_rel) for p in sub_plugins]
    by_name = {p["name"]: p for p in root_plugins if p.get("name")}
    by_name.update({p["name"]: p for p in adjusted if p.get("name")})
    root_data["plugins"] = list(by_name.values())

    # Write back
    root_marketplace.write_text(json.dumps(root_data, indent=2) + "\n", encoding="utf-8")

    print(f"Merged {len(adjusted)} plugins from {submodule_path}")
    print(f"Total plugins in marketplace: {len(root_data['plugins'])}")

if __name__ == "__main__":
    main()
