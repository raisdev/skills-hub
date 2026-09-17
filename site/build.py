#!/usr/bin/env python3
"""Builds the catalog page (site/dist/index.html + catalog.json) from the repo.

Reads .claude-plugin/marketplace.json, each plugin's plugin.json, README.md and
SKILL.md front matter, plus everything under incubator/. Open issues are pulled
live by the page itself from the GitHub API, so requests and ideas never go
stale between builds. Run locally with: python3 site/build.py && open site/dist/index.html
"""
import json, pathlib, re, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIST = ROOT / "site" / "dist"
REPO = "raisdev/skills-hub"

def front_matter(p):
    txt = p.read_text(encoding="utf-8", errors="replace")
    if not txt.startswith("---"): return {}
    end = txt.find("\n---", 3)
    fm = {}
    for line in txt[3:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1); fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm

def readme_summary(p):
    if not p.exists(): return ""
    body = p.read_text(encoding="utf-8", errors="replace")
    body = re.sub(r"^#.*$", "", body, count=1, flags=re.M).strip()
    para = body.split("\n\n")[0].strip()
    return re.sub(r"\s+", " ", para)[:400]

def owner_status(p):
    if not p.exists(): return "", ""
    txt = p.read_text(encoding="utf-8", errors="replace")
    o = re.search(r"\*\*Owner\*\*\s*([^.*]+)", txt)
    s = re.search(r"\*\*Status\*\*\s*([^.*]+)", txt)
    return (o.group(1).strip() if o else ""), (s.group(1).strip() if s else "")

def plugin_record(folder, status):
    pj = folder / ".claude-plugin" / "plugin.json"
    meta = json.loads(pj.read_text(encoding="utf-8")) if pj.exists() else {}
    skills = []
    for s in sorted(folder.glob("skills/*/SKILL.md")):
        fm = front_matter(s)
        skills.append({"name": fm.get("name", s.parent.name), "description": fm.get("description", "")})
    connectors = []
    mcp = folder / ".mcp.json"
    if mcp.exists():
        try: connectors = list(json.loads(mcp.read_text(encoding="utf-8")).keys())
        except Exception: connectors = ["(see .mcp.json)"]
    owner, st = owner_status(folder / "README.md")
    author = meta.get("author")
    if isinstance(author, dict): author = author.get("name", "")
    rel = folder.relative_to(ROOT).as_posix()
    return {
        "name": meta.get("name", folder.name),
        "version": meta.get("version", ""),
        "description": meta.get("description", ""),
        "summary": readme_summary(folder / "README.md"),
        "owner": owner or author or "",
        "status": status,
        "skills": skills,
        "connectors": connectors,
        "path": rel,
        "readme": f"https://github.com/{REPO}/blob/main/{rel}/README.md",
    }

def build():
    cat = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    published = []
    for p in cat.get("plugins", []):
        folder = ROOT / p["source"][2:]
        if folder.is_dir():
            rec = plugin_record(folder, "published")
            rec["tags"] = p.get("tags", []); rec["category"] = p.get("category", "")
            published.append(rec)
    incubating = []
    inc = ROOT / "incubator"
    if inc.exists():
        for folder in sorted(inc.iterdir()):
            if folder.is_dir() and (folder / ".claude-plugin" / "plugin.json").exists():
                incubating.append(plugin_record(folder, "in development"))
    data = {
        "marketplace": cat.get("name"),
        "description": cat.get("metadata", {}).get("description", ""),
        "built": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "repo": REPO,
        "published": published,
        "incubating": incubating,
    }
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "catalog.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    tpl = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
    html = tpl.replace("/*__CATALOG__*/null", json.dumps(data))
    (DIST / "index.html").write_text(html, encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    print(f"built {len(published)} published, {len(incubating)} in development -> {DIST}")

if __name__ == "__main__":
    build()
