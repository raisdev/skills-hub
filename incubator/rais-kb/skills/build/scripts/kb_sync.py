#!/usr/bin/env python3
"""Keep a knowledge base in step with the person's folder without reading documents into the conversation.

The person's folder is the knowledge base. They manage it like any folder (add, replace, delete, move,
rename files). This script keeps one subfolder, "Claude files (Claude manages)", in step with it.

There is no manifest and no lock. Every converted document carries its own record in its front matter
(fingerprint, size, modified time, document type, and its index entry). INDEX.md is generated from those
records, so any copy of the folder can rebuild it and two people can never corrupt a shared record.
This is what makes the folder safe to share through SharePoint.

Usage:
    python3 kb_sync.py --root "<connected folder>" --check
    python3 kb_sync.py --root "<connected folder>" --plan
    python3 kb_sync.py --root "<connected folder>" --apply [--assign assign.tsv]
    python3 kb_sync.py --root "<connected folder>" --set-entry docs/x.md --summary "..." --consult "..." --sections "..." [--title "..."] [--type policy]
    python3 kb_sync.py --root "<connected folder>" --index
    python3 kb_sync.py --root "<connected folder>" --archive-proposal <name> --as applied|declined
    python3 kb_sync.py --root "<connected folder>" --upgrade

--check   one JSON line: current or changed, plus counts of documents waiting to be indexed, scanned pages
          waiting for Claude, pending playbook proposals, and conflicted copies. Nearly instant: a file whose
          size and modified time match its record is not reread. Add --full to fingerprint every file.
--plan    full report of added, changed, removed, moved, and everything --check counts. Changes nothing.
--apply   converts added and changed files, retires removed ones, cleans up conflicted copies of generated
          files, regenerates INDEX.md, appends to CHANGELOG.md. One JSON line per action with a "next" hint.
--set-entry  writes a document's index entry into its front matter and regenerates INDEX.md.
--index   regenerates INDEX.md only.
--archive-proposal  moves a playbook proposal to proposals/applied or proposals/declined.
--upgrade converts a folder built by version 0.9 (Source files subfolder, MANIFEST.json) to this layout.

assign.tsv (optional) sets the document type for new files, one per line:
    <path relative to the folder><TAB><doc_type>
The type "skip" marks a file that is not reference material (an old version, a draft); it is left in
place, remembered in _admin/skip.txt, and never converted.
Without it, a known first folder name (policies, templates, guidance, examples, external) decides,
otherwise the type is "reference".

Layout:
    <folder>/                                the person's documents, in whatever subfolders they like
        CLAUDE.md, legal.local.md            pointer files written by Claude, not this script
        _anything/                           subfolders starting with _ are ignored (drafts, redlines)
        Claude files (Claude manages)/
            PLAYBOOK.md                      written by Claude, approved by the person
            INDEX.md                         generated from the documents' front matter
            docs/<same path>.md              Markdown copy of each document, with its record in front matter
            _admin/kb_sync.py                copy of this script, so any session can run --check
            _admin/CHANGELOG.md              one line per sync
            _admin/proposals/                proposed playbook changes waiting for approval
            _admin/sync/*.diff               old vs new text for replaced files (read these, not the file)
            _admin/retired/                  old copies of removed, replaced, or duplicated files
            _admin/needs-attention/          records of files that could not be converted
    PDF pages without a text layer (scans) are marked with KB-VISION placeholders for Claude to read once.
"""
import argparse
import datetime as dt
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TODAY = dt.date.today().isoformat()
KB_NAME = "Claude files (Claude manages)"
TEXT_LIKE = {".md", ".markdown", ".txt"}
DOCX_LIKE = {".docx"}
LEGACY = {".doc", ".rtf", ".odt", ".wpd"}
HTML_LIKE = {".html", ".htm", ".xhtml"}
PDF = {".pdf"}
SUPPORTED = TEXT_LIKE | DOCX_LIKE | LEGACY | HTML_LIKE | PDF
TYPE_BY_FOLDER = {"policies": "policy", "policy": "policy", "templates": "template", "template": "template",
                  "guidance": "guidance", "examples": "example", "prior agreements": "example", "agreements": "example",
                  "external": "external", "sponsors": "external"}
TYPE_ORDER = ["playbook", "policy", "template", "guidance", "example", "external", "reference"]
SKIP_NAMES = {"Thumbs.db", "desktop.ini", ".DS_Store", "CLAUDE.md", "legal.local.md"}
TEMP_SUFFIXES = (".tmp", ".partial", ".crdownload", ".download", ".bak")
CONFLICT_RE = re.compile(r"conflicted copy|-conflict\b|\(conflict", re.I)
VISION_TAG = "<!-- KB-VISION"
ENTRY_KEYS = ("summary", "consult_when", "key_sections")
INDEX_HEADER = ("# Index\n\nGenerated from the documents. Do not edit this file; ask Claude to update an entry.\n"
                "Paths are relative to this folder.\n")


# ---------- conversion ----------

def have(tool):
    return shutil.which(tool) is not None


def run(cmd, timeout=300):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def slug(name):
    s = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()
    return s or "document"


def tidy_markdown(text):
    text = text.replace("\\[", "[").replace("\\]", "]")
    text = re.sub(r"\[([^\]]*)\]\{[^}]*\}", r"\1", text)
    return re.sub(r"\{\.[a-zA-Z-]+\}", "", text)


def title_from(path, text):
    for line in text.splitlines()[:40]:
        line = re.sub(r"[*_`#>\[\]{}\\]", "", line).strip().rstrip(":")
        if 8 <= len(line) <= 120 and not line.startswith("|"):
            return line
    return re.sub(r"[_\-]+", " ", path.stem).strip()


def date_from(path, text):
    hay = path.name + "\n" + "\n".join(text.splitlines()[:60])
    m = re.search(r"(20\d{2})[-._/ ](\d{1,2})[-._/ ](\d{1,2})", hay)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    m = re.search(r"\b(20\d{2})\b", hay)
    return m.group(1) if m else "unknown"


def validate(text):
    if len(text.strip()) < 200:
        return "empty", "under 200 characters of text"
    bad = sum(1 for c in text if (ord(c) < 32 and c not in "\n\r\t") or c == "�")
    if bad / max(len(text), 1) > 0.05:
        return "garbled", "more than 5 percent unreadable characters"
    words = re.findall(r"\S+", text)
    if words and sum(1 for w in words if len(w) == 1) / len(words) > 0.5:
        return "garbled", "mostly single characters, likely a scanned or badly encoded PDF"
    return "ok", ""


def clean_pdf_text(text):
    text = text.replace("\f", "\n\n")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text)


def is_text_page(t):
    return len(t) >= 200 and validate(t)[0] != "garbled"


def page_count(src: Path, fallback: int):
    if have("pdfinfo"):
        r = run(["pdfinfo", str(src)])
        m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
        if m:
            return int(m.group(1))
    return fallback


def pdf_to_markdown(src: Path):
    """Pages with a usable text layer are used as is. Every other page (an image page, such as a scan)
    gets a KB-VISION placeholder, and Claude reads just those pages from the PDF once and replaces the
    placeholders with their text. No OCR engine is needed. If pdftotext is not available at all,
    Claude reads the whole PDF once."""
    if not have("pdftotext"):
        return f"{VISION_TAG} all pages -->", "Claude to read the whole PDF (no text extraction tool here)", \
               {"vision": [{"page": "all"}]}
    r = run(["pdftotext", "-layout", str(src), "-"])
    if r.returncode != 0:
        raise RuntimeError("error: pdftotext failed (" + r.stderr.strip()[:120] + ")")
    raw = r.stdout.split("\f")
    n = page_count(src, len(raw) - 1 if raw and not raw[-1].strip() else len(raw))
    raw += [""] * max(0, n - len(raw))
    out, vision = [], []
    for i in range(1, n + 1):
        t = clean_pdf_text(raw[i - 1]).strip()
        if is_text_page(t) or (len(t) >= 40 and validate(t)[0] != "garbled"):
            out.append(t)  # includes sparse but real text pages, such as a signature page
        else:
            out.append(f"{VISION_TAG} page {i} -->")
            vision.append({"page": i})
    note = ("Claude to read page(s) " + ", ".join(str(v["page"]) for v in vision)) if vision else ""
    return "\n\n".join(out), note, {"vision": vision}


def to_markdown(src: Path):
    """Return (text, note, info). For PDFs, info lists the pages Claude must read."""
    ext = src.suffix.lower()
    if ext in TEXT_LIKE:
        return src.read_text(errors="replace"), "", {}
    if ext in DOCX_LIKE or ext in HTML_LIKE:
        if not have("pandoc"):
            raise RuntimeError("missing-tool: pandoc")
        r = run(["pandoc", "-f", "docx" if ext in DOCX_LIKE else "html", "-t", "gfm", "--wrap=none", str(src)])
        if r.returncode != 0:
            raise RuntimeError("error: " + r.stderr.strip()[:200])
        return r.stdout, "", {}
    if ext in LEGACY:
        if not have("soffice"):
            raise RuntimeError("missing-tool: soffice (LibreOffice)")
        with tempfile.TemporaryDirectory() as td:
            r = run(["soffice", "--headless", "--convert-to", "docx", "--outdir", td, str(src)])
            out = Path(td) / (src.stem + ".docx")
            if r.returncode != 0 or not out.exists():
                raise RuntimeError("error: LibreOffice conversion failed")
            return to_markdown(out)[0], "converted via LibreOffice", {}
    if ext in PDF:
        return pdf_to_markdown(src)
    raise RuntimeError("unsupported")


# ---------- front matter (the record each document carries) ----------

def parse_front(md: str):
    """Return (fields, body). Fields are single-line key: value pairs."""
    if not md.startswith("---"):
        return {}, md
    end = md.find("\n---", 3)
    if end < 0:
        return {}, md
    fields = {}
    for line in md[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    body = md[end + 4:]
    return fields, body.lstrip("\n")


def build_front(fields):
    order = ["title", "source_path", "doc_type", "effective_date", "converted", "sha256", "size", "mtime",
             "pages_read_by_claude", "status", "note", "indexed", "summary", "consult_when", "key_sections"]
    keys = [k for k in order if k in fields] + [k for k in fields if k not in order]
    return "---\n" + "".join(f"{k}: {oneline(fields[k])}\n" for k in keys) + "---\n\n"


def oneline(v):
    return re.sub(r"\s*\n\s*", " ", str(v)).strip()


def read_head(path: Path, n=4096):
    with open(path, "r", errors="replace") as f:
        head = f.read(n)
    if head.startswith("---") and "\n---" not in head[3:]:
        head = path.read_text(errors="replace")
    return head


def record_of(path: Path):
    """Read only the front matter of a generated file. Cheap even for long documents."""
    fields, _ = parse_front(read_head(path))
    return fields


def write_fields(path: Path, updates: dict):
    md = path.read_text(errors="replace")
    fields, body = parse_front(md)
    fields.update({k: v for k, v in updates.items() if v is not None})
    path.write_text(build_front(fields) + body)
    return fields


def render(src: Path, rel: str, doc_type: str, fp: dict, keep: dict = None):
    """Return (status, full_markdown, body, note, info). keep carries index fields from an earlier copy."""
    try:
        text, note, info = to_markdown(src)
    except RuntimeError as e:
        msg = str(e)
        status = msg.split(":")[0] if msg.startswith(("missing-tool", "unsupported")) else "error"
        return status, None, None, msg, {}
    text = tidy_markdown(text)
    status, why = validate(text)
    if info.get("vision"):
        status, why = "ok", ""  # image pages are waiting for Claude, the document itself is fine
    elif src.suffix.lower() in PDF and status == "empty" and text.strip():
        status, why = "ok", ""  # PDFs are judged page by page; a short document with readable text is fine
    fields = {
        "title": title_from(src, text), "source_path": rel, "doc_type": doc_type,
        "effective_date": date_from(src, text), "converted": TODAY,
        "sha256": fp["sha256"], "size": fp["size"], "mtime": fp["mtime"],
        "status": "current" if status == "ok" else "needs-attention",
    }
    if info.get("vision"):
        fields["pages_read_by_claude"] = ", ".join(str(v["page"]) for v in info["vision"])
    if why:
        fields["note"] = why
    keep = keep or {}
    for k in ENTRY_KEYS:
        if keep.get(k):
            fields[k] = keep[k]
    fields["indexed"] = "yes" if fields.get("summary") else "no"
    return status, build_front(fields) + text, text, "; ".join(x for x in (note, why) if x), info


def stub(rel: str, doc_type: str, fp: dict, status: str, note: str):
    """The record for a file that could not be converted, kept in needs-attention/ so it is not retried
    on every sync and the person can be told about it."""
    return build_front({"title": Path(rel).stem, "source_path": rel, "doc_type": doc_type, "converted": TODAY,
                        "sha256": fp["sha256"], "size": fp["size"], "mtime": fp["mtime"],
                        "status": "needs-attention", "note": f"{status}: {note}", "indexed": "no"})


# ---------- sync ----------

def sha256(path: Path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class Layout:
    def __init__(self, root: Path):
        self.root = root
        self.kb = root / KB_NAME
        self.docs = self.kb / "docs"
        self.admin = self.kb / "_admin"
        self.index = self.kb / "INDEX.md"
        self.playbook = self.kb / "PLAYBOOK.md"
        self.changelog = self.admin / "CHANGELOG.md"
        self.diffs = self.admin / "sync"
        self.retired = self.admin / "retired"
        self.attention = self.admin / "needs-attention"
        self.proposals = self.admin / "proposals"
        self.skiplist = self.admin / "skip.txt"

    def skipped(self):
        """Files the person said are not reference material (type skip in assign.tsv). Remembered here."""
        if not self.skiplist.exists():
            return set()
        return {l.strip() for l in self.skiplist.read_text().splitlines() if l.strip()}

    def add_skips(self, rels):
        if not rels:
            return
        self.admin.mkdir(parents=True, exist_ok=True)
        current = self.skipped() | set(rels)
        self.skiplist.write_text("\n".join(sorted(current)) + "\n")

    def rel(self, p: Path):
        return p.relative_to(self.kb).as_posix()


def is_conflict_name(name: str):
    return bool(CONFLICT_RE.search(name)) or bool(re.search(r" \(\d+\)\.\w+$", name))


def scan_sources(L: Layout, known, full=False):
    """Fingerprint every document in the person's folder. A file whose size and modified time match its
    record keeps the recorded fingerprint without being reread, so a check of an unchanged folder is
    nearly instant. Returns (found, skipped) where skipped lists sync temp files and conflicted copies."""
    found, skipped = {}, []
    not_reference = L.skipped()
    for p in sorted(L.root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(L.root)
        if rel.parts[0] == KB_NAME or any(part.startswith((".", "_")) for part in rel.parts[:-1]):
            continue
        if p.name.startswith((".", "~$")) or p.name in SKIP_NAMES:
            continue
        if p.suffix.lower() in TEMP_SUFFIXES or is_conflict_name(p.name):
            skipped.append(rel.as_posix())
            continue
        if rel.as_posix() in not_reference or p.suffix.lower() not in SUPPORTED:
            continue
        st = p.stat()
        key = rel.as_posix()
        prev = known.get(key)
        if not full and prev and str(prev.get("size")) == str(st.st_size) and str(prev.get("mtime")) == str(st.st_mtime_ns):
            digest = prev["sha256"]
        else:
            digest = sha256(p)
        found[key] = {"sha256": digest, "size": st.st_size, "mtime": st.st_mtime_ns}
    return found, skipped


def scan_records(L: Layout):
    """The records are the generated files themselves. Returns (known, conflicts)."""
    known, conflicts = {}, []
    for base in (L.docs, L.attention):
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            if is_conflict_name(p.name):
                conflicts.append(p)
                continue
            f = record_of(p)
            src = f.get("source_path")
            if not src or not f.get("sha256"):
                continue
            f["output"] = L.rel(p)
            other = known.get(src)
            if other:  # two records for one source: keep the newer, the other is a duplicate to retire
                if f.get("converted", "") <= other.get("converted", ""):
                    conflicts.append(p)
                    continue
                conflicts.append(L.kb / other["output"])
            known[src] = f
    for name in ("INDEX.md", "PLAYBOOK.md"):
        for p in L.kb.glob(f"*{Path(name).stem}*"):
            if p.is_file() and p.name != name and is_conflict_name(p.name):
                conflicts.append(p)
    return known, conflicts


def plan(L: Layout, full=False):
    known, conflicts = scan_records(L)
    disk, skipped = scan_sources(L, known, full)
    added = [p for p in disk if p not in known]
    removed = [p for p in known if p not in disk]
    changed = [p for p in disk if p in known and disk[p]["sha256"] != known[p]["sha256"]]
    moved = []
    for old in list(removed):
        for new in list(added):
            if known[old]["sha256"] == disk[new]["sha256"]:
                moved.append([old, new])
                removed.remove(old)
                added.remove(new)
                break
    attention = [p for p, e in known.items() if e.get("status") != "current" and p in disk and p not in changed]
    cutoff = dt.date.today().year - 2
    stale = [p for p, e in known.items() if re.match(r"\d{4}", e.get("effective_date", ""))
             and int(e["effective_date"][:4]) < cutoff]
    waiting = [p for p, e in known.items() if e.get("pages_read_by_claude") and e.get("status") == "current"
               and VISION_TAG in (L.kb / e["output"]).read_text(errors="replace")]
    unindexed = [p for p, e in known.items() if e.get("status") == "current" and e.get("indexed") != "yes"
                 and p in disk and p not in changed]
    proposals = sorted(x.name for x in L.proposals.glob("*.md")) if L.proposals.is_dir() else []
    playbook_conflicts = [L.rel(c) for c in conflicts if c.parent == L.kb and "PLAYBOOK" in c.name.upper()]
    legacy = (L.root / "Source files (you manage)").is_dir() or (L.admin / "MANIFEST.json").exists()
    return known, disk, {
        "added": added, "changed": changed, "removed": removed, "moved": moved,
        "unchanged": len(disk) - len(added) - len(changed) - len(moved),
        "needs_attention": attention, "older_than_two_years": stale,
        "pages_for_claude": waiting, "unindexed": unindexed,
        "proposals": proposals, "conflicts": [L.rel(c) for c in conflicts],
        "playbook_conflicts": playbook_conflicts, "skipped_sync_files": skipped,
        "legacy_layout": legacy,
    }


def retire(L: Layout, path: Path, reason: str):
    if not path.exists():
        return None
    L.retired.mkdir(parents=True, exist_ok=True)
    dest, n = L.retired / f"{path.stem}.{TODAY}.md", 2
    while dest.exists():
        dest, n = L.retired / f"{path.stem}.{TODAY}-{n}.md", n + 1
    path.rename(dest)  # a move, never a delete; the device shell cannot delete files
    if path.suffix == ".md" and reason:
        try:
            write_fields(dest, {"status": reason})
        except OSError:
            pass
    return L.rel(dest)


def mirror_path(L: Layout, rel: str, ok: bool, taken):
    base = (L.docs if ok else L.attention) / Path(rel).parent
    stem = slug(Path(rel).stem)
    out, n = base / f"{stem}.md", 2
    while L.rel(out) in taken:
        out, n = base / f"{stem}-{n}.md", n + 1
    return out


def doc_type_for(rel, assign, known_type=None):
    if rel in assign:
        return assign[rel]
    if known_type:
        return known_type
    first = rel.split("/")[0].lower() if "/" in rel else ""
    return TYPE_BY_FOLDER.get(first, "reference")


def resolve_conflicts(L: Layout, known, disk, emit):
    """Conflicted copies of generated files are never merged. A document copy is kept only if it is the
    one whose fingerprint matches the file in the folder; INDEX.md copies are regenerated anyway."""
    _, conflicts = scan_records(L)
    n = 0
    for c in conflicts:
        if c.parent == L.kb and "PLAYBOOK" in c.name.upper():
            continue  # a person edits the playbook; two versions need a person to merge them
        if c.suffix == ".md" and c.parent != L.kb:
            f = record_of(c)
            src = f.get("source_path")
            current = known.get(src)
            real = sha256(L.root / src) if src in disk else None  # fingerprint the file itself, not a record
            if real and f.get("sha256") == real and (not current or current.get("sha256") != real):
                # the conflicted copy is the right one and the canonical copy is stale: swap them
                canonical = L.kb / current["output"] if current else mirror_path(L, src, True, set())
                if canonical.exists():
                    retire(L, canonical, "superseded")
                c.rename(canonical)
                known[src] = record_of(canonical)
                known[src]["output"] = L.rel(canonical)
                emit({"action": "conflict-resolved", "kept": L.rel(canonical), "note": "kept the copy matching the source"})
                n += 1
                continue
        retire(L, c, "duplicate")
        emit({"action": "conflict-resolved", "retired": c.name, "note": "duplicate copy retired; nothing to merge"})
        n += 1
    return n


def apply(L: Layout, assign, full=False):
    L.add_skips([r for r, t in assign.items() if t == "skip"])
    assign = {r: t for r, t in assign.items() if t != "skip"}
    known, disk, p = plan(L, full)
    counts = {"added": 0, "changed": 0, "removed": 0, "moved": 0, "needs_attention": 0, "conflicts": 0}

    def emit(rec):
        print(json.dumps(rec))

    def taken(exclude=None):
        return {e["output"] for r, e in known.items() if e.get("output") and r != exclude}

    counts["conflicts"] = resolve_conflicts(L, known, disk, emit)
    if counts["conflicts"]:
        known, disk, p = plan(L, full)

    for old, new in p["moved"]:
        entry = known.pop(old)
        prev_out = L.kb / entry["output"]
        ok = entry.get("status") == "current"
        dest = mirror_path(L, new, ok, taken(old))
        dest.parent.mkdir(parents=True, exist_ok=True)
        if prev_out != dest:
            prev_out.rename(dest)
        entry = write_fields(dest, {"source_path": new, "mtime": disk[new]["mtime"], "size": disk[new]["size"]})
        entry["output"] = L.rel(dest)
        known[new] = entry
        counts["moved"] += 1
        emit({"action": "moved", "from": old, "to": new, "output": entry["output"],
              "next": "nothing to read; if the file name changed, update PLAYBOOK.md citations of the old name."})

    fixed = [r for r in p["changed"] if known[r].get("status") != "current"]
    p["changed"] = [r for r in p["changed"] if r not in fixed]

    for rel in p["added"] + p["needs_attention"] + fixed:
        prev = known.get(rel, {})
        typ = doc_type_for(rel, assign, prev.get("doc_type"))
        status, full_md, _, note, info = render(L.root / rel, rel, typ, disk[rel], keep=prev)
        if prev.get("output") and (L.kb / prev["output"]).exists():
            retire(L, L.kb / prev["output"], "replaced-conversion")
        if full_md is None or status != "ok":
            out = mirror_path(L, rel, False, taken(rel))
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(full_md if full_md else stub(rel, typ, disk[rel], status, note))
            known[rel] = dict(record_of(out), output=L.rel(out))
            counts["needs_attention"] += 1
            emit({"action": "needs_attention", "source": rel, "status": status, "note": note,
                  "next": "tell the person this file could not be converted and give them the rais-help note"})
            continue
        out = mirror_path(L, rel, True, taken(rel))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(full_md)
        known[rel] = dict(record_of(out), output=L.rel(out))
        counts["added"] += 1
        rec = {"action": "added", "source": rel, "output": L.rel(out), "note": note,
               "next": "read the output once, then --set-entry with its summary, consult-when, and key sections; "
                       "propose any PLAYBOOK.md additions as a proposal file."}
        if info.get("vision"):
            rec["claude_pages"] = info["vision"]
            rec["next"] = ("the pages in claude_pages have no text layer. Stage the source PDF, read only those pages "
                           "(Read tool, pages option), and replace each matching KB-VISION placeholder in the output with "
                           "that page's text, keeping headings and section numbers. If a page cannot be read, leave its "
                           "placeholder and tell the person which document and page. Then " + rec["next"])
        emit(rec)

    for rel in p["changed"]:
        prev = known[rel]
        status, full_md, body, note, info = render(L.root / rel, rel, prev.get("doc_type", "reference"), disk[rel], keep=prev)
        if full_md is None or status != "ok":
            counts["needs_attention"] += 1
            emit({"action": "needs_attention", "source": rel, "status": status, "note": note,
                  "next": "kept the previous copy; tell the person the new version did not convert cleanly"})
            continue
        old_path = L.kb / prev["output"]
        old_text = old_path.read_text(errors="replace") if old_path.exists() else ""
        diff = "".join(difflib.unified_diff(parse_front(old_text)[1].splitlines(True), body.lstrip("\n").splitlines(True),
                                            fromfile="previous", tofile="current", n=1))
        L.diffs.mkdir(parents=True, exist_ok=True)
        diff_path = L.diffs / f"{slug(Path(rel).stem)}.{TODAY}.diff"
        diff_path.write_text(diff or "No text differences (formatting or metadata only).\n")
        retired = retire(L, old_path, "superseded")
        old_path.parent.mkdir(parents=True, exist_ok=True)
        old_path.write_text(full_md)
        known[rel] = dict(record_of(old_path), output=L.rel(old_path))
        counts["changed"] += 1
        rec = {"action": "changed", "source": rel, "output": L.rel(old_path), "previous": retired,
               "diff": L.rel(diff_path), "diff_lines": diff.count("\n"),
               "next": "read only the diff; --set-entry if the summary, scope, or date changed; "
                       "search PLAYBOOK.md for lines citing this file and write a proposal for any the diff affects."}
        if info.get("vision"):
            rec["claude_pages"] = info["vision"]
            rec["next"] += (" Then stage the source PDF, read only the pages in claude_pages, and replace each matching "
                            "KB-VISION placeholder with that page's text.")
        emit(rec)

    for rel in p["removed"]:
        prev = known.pop(rel)
        retired = retire(L, L.kb / prev["output"], "retired")
        counts["removed"] += 1
        emit({"action": "removed", "source": rel, "retired_to": retired,
              "next": "search PLAYBOOK.md for lines citing this file and write a proposal for each (drop, recite, or keep)"})

    # files whose content is unchanged but whose modified time moved (opened and saved, copied back):
    # record the new time so the next check can skip fingerprinting them
    for rel, e in known.items():
        if rel in disk and e.get("sha256") == disk[rel]["sha256"] and (
                str(e.get("mtime")) != str(disk[rel]["mtime"]) or str(e.get("size")) != str(disk[rel]["size"])):
            write_fields(L.kb / e["output"], {"mtime": disk[rel]["mtime"], "size": disk[rel]["size"]})

    build_index(L)
    install_self(L)
    if any(counts.values()):
        L.admin.mkdir(parents=True, exist_ok=True)
        with open(L.changelog, "a") as f:
            f.write(f"- {TODAY} sync: {counts['added']} added, {counts['changed']} replaced, "
                    f"{counts['removed']} removed, {counts['moved']} moved, "
                    f"{counts['needs_attention']} need attention, {counts['conflicts']} duplicate copies tidied\n")
    print(json.dumps({"summary": counts, "skipped_sync_files": p["skipped_sync_files"]}), file=sys.stderr)


def install_self(L: Layout):
    """Keep a copy of this script next to the KB so any session can run the quick check."""
    try:
        me = Path(__file__).resolve()
        dest = L.admin / "kb_sync.py"
        L.admin.mkdir(parents=True, exist_ok=True)
        if me != dest.resolve() and (not dest.exists() or dest.read_bytes() != me.read_bytes()):
            dest.write_bytes(me.read_bytes())
    except OSError:
        pass


# ---------- index ----------

def build_index(L: Layout):
    known, _ = scan_records(L)
    groups = {}
    for src, e in known.items():
        if e.get("status") != "current":
            continue
        groups.setdefault(e.get("doc_type", "reference"), []).append(e)
    out = [INDEX_HEADER]
    for typ in sorted(groups, key=lambda t: (TYPE_ORDER.index(t) if t in TYPE_ORDER else 99, t)):
        out.append(f"\n## {typ.capitalize()}\n")
        for e in sorted(groups[typ], key=lambda x: x.get("title", "").lower()):
            out.append(f"\n### {e.get('title', Path(e['source_path']).stem)}\n"
                       f"- Path: {e['output']}\n"
                       f"- Source: {e['source_path']}\n"
                       f"- Type: {typ}, effective {e.get('effective_date', 'unknown')}\n")
            if e.get("indexed") == "yes":
                out.append(f"- Summary: {e.get('summary', '')}\n"
                           f"- Consult when: {e.get('consult_when', '')}\n"
                           f"- Key sections: {e.get('key_sections', '')}\n")
            else:
                out.append("- Summary: (not yet indexed)\n")
    text = "".join(out)
    if not L.index.exists() or L.index.read_text(errors="replace") != text:
        L.kb.mkdir(exist_ok=True)
        L.index.write_text(text)
        return True
    return False


def set_entry(L: Layout, output: str, summary, consult, sections, title=None, doc_type=None):
    path = L.kb / output
    if not path.exists():
        sys.exit(f"no such file: {output}")
    updates = {"summary": summary, "consult_when": consult, "key_sections": sections, "title": title, "doc_type": doc_type}
    fields = write_fields(path, {k: v for k, v in updates.items() if v})
    write_fields(path, {"indexed": "yes" if fields.get("summary") else "no"})
    build_index(L)
    print(json.dumps({"action": "entry-set", "output": output, "indexed": fields.get("summary") is not None}))


def archive_proposal(L: Layout, name: str, outcome: str):
    src = L.proposals / name
    if not src.exists():
        sys.exit(f"no such proposal: {name}")
    dest_dir = L.proposals / outcome
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    src.rename(dest)
    with open(L.changelog, "a") as f:
        f.write(f"- {TODAY} proposal {outcome}: {name}\n")
    print(json.dumps({"action": "proposal-" + outcome, "file": L.rel(dest)}))


# ---------- upgrade from version 0.9 ----------

def upgrade(L: Layout):
    """Version 0.9 kept documents in "Source files (you manage)" and records in _admin/MANIFEST.json,
    with index entries only in INDEX.md. Move the documents up into the folder, write each record and
    index entry into its document's front matter, and retire the manifest and the old index."""
    old_sources = L.root / "Source files (you manage)"
    moved, collisions = 0, []
    if old_sources.is_dir():
        for p in sorted(old_sources.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(old_sources)
            dest = L.root / rel
            if dest.exists():
                collisions.append(rel.as_posix())
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            p.rename(dest)
            moved += 1
    manifest_path = L.admin / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())["files"] if manifest_path.exists() else {}
    entries = {}
    if L.index.exists():
        for block in re.split(r"\n(?=### )", L.index.read_text(errors="replace")):
            m = re.search(r"^- Path:\s*(.+)$", block, re.M)
            if not m:
                continue
            e = {}
            for key, field in (("Summary", "summary"), ("Consult when", "consult_when"), ("Key sections", "key_sections")):
                mm = re.search(rf"^- {key}:\s*(.+)$", block, re.M)
                if mm:
                    e[field] = mm.group(1).strip()
            entries[m.group(1).strip()] = e
    records = 0
    for src, e in manifest.items():
        out = e.get("output")
        if not out:
            continue
        path = L.kb / out
        if not path.exists():
            continue
        updates = {"source_path": src, "sha256": e.get("sha256"), "size": e.get("size"), "mtime": e.get("mtime"),
                   "doc_type": e.get("doc_type"), "status": e.get("status", "current")}
        updates.update({k: v for k, v in entries.get(out, {}).items() if v and "not yet" not in v})
        fields = write_fields(path, updates)
        write_fields(path, {"indexed": "yes" if fields.get("summary") else "no"})
        records += 1
    if manifest_path.exists():
        retire(L, manifest_path, "")
    if L.index.exists():
        retire(L, L.index, "")
    if old_sources.is_dir() and not any(p.is_file() for p in old_sources.rglob("*")):
        L.retired.mkdir(parents=True, exist_ok=True)
        old_sources.rename(L.retired / "Source files (old layout)")  # empty, moved rather than deleted
    build_index(L)
    install_self(L)
    with open(L.changelog, "a") as f:
        f.write(f"- {TODAY} upgraded to the single-folder layout: {moved} files moved up, {records} records written\n")
    print(json.dumps({"action": "upgraded", "files_moved": moved, "records": records, "collisions": collisions,
                      "next": "if the old Source files folder is now empty it can be left or removed by the person; "
                              "rewrite CLAUDE.md and legal.local.md; then run --apply"}))


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="the connected folder (the knowledge base)")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true")
    mode.add_argument("--check", action="store_true", help="one-line summary for the start of a conversation")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--index", action="store_true", help="regenerate INDEX.md")
    mode.add_argument("--set-entry", metavar="OUTPUT", help="write a document's index entry into its front matter")
    mode.add_argument("--archive-proposal", metavar="NAME")
    mode.add_argument("--upgrade", action="store_true", help="convert a version 0.9 folder to this layout")
    ap.add_argument("--full", action="store_true", help="fingerprint every file even if size and date are unchanged")
    ap.add_argument("--assign", help="TSV of <path under the folder><TAB><doc_type> for new files")
    ap.add_argument("--summary")
    ap.add_argument("--consult")
    ap.add_argument("--sections")
    ap.add_argument("--title", help="with --set-entry: correct the document's title")
    ap.add_argument("--type", dest="doc_type", help="with --set-entry: correct the document type")
    ap.add_argument("--as", dest="outcome", choices=["applied", "declined"], default="applied")
    a = ap.parse_args()
    L = Layout(Path(a.root).resolve())
    if not L.root.is_dir():
        ap.error(f"no such folder: {L.root}")
    assign = {}
    if a.assign:
        for line in Path(a.assign).read_text().splitlines():
            parts = [x.strip() for x in line.split("\t")]
            if len(parts) >= 2 and parts[0] and not parts[0].startswith("#"):
                assign[parts[0]] = parts[-1]
    if a.check:
        if not L.docs.is_dir() and not L.attention.is_dir():
            legacy = (L.root / "Source files (you manage)").is_dir() or (L.admin / "MANIFEST.json").exists()
            print(json.dumps({"status": "legacy" if legacy else "no-kb"}))
            return
        r = plan(L, a.full)[2]
        n = len(r["added"]) + len(r["changed"]) + len(r["removed"]) + len(r["moved"])
        print(json.dumps({"status": "legacy" if r["legacy_layout"] else ("changed" if n else "current"),
                          "changes": n, "added": len(r["added"]), "replaced": len(r["changed"]),
                          "removed": len(r["removed"]), "moved": len(r["moved"]),
                          "needs_attention": len(r["needs_attention"]), "pages_for_claude": len(r["pages_for_claude"]),
                          "unindexed": len(r["unindexed"]), "proposals": len(r["proposals"]),
                          "conflicts": len(r["conflicts"]), "playbook_conflicts": r["playbook_conflicts"]}))
    elif a.plan:
        print(json.dumps(plan(L, a.full)[2], indent=2))
    elif a.index:
        print(json.dumps({"action": "index", "changed": build_index(L)}))
    elif a.set_entry:
        set_entry(L, a.set_entry, a.summary, a.consult, a.sections, a.title, a.doc_type)
    elif a.archive_proposal:
        archive_proposal(L, a.archive_proposal, a.outcome)
    elif a.upgrade:
        upgrade(L)
    else:
        L.kb.mkdir(exist_ok=True)
        apply(L, assign, a.full)


if __name__ == "__main__":
    main()
