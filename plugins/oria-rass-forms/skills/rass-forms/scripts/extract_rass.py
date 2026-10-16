"""
Extract the header fields for the Grant-IACUC Protocol Comparison Checklist
from RASS "Sponsored Research Protocol Application" PDF printouts.

Usage:
    python extract_rass.py                 # every PDF in this folder
    python extract_rass.py file1.pdf ...   # specific files

Writes/updates rass_extracted.json in this folder (one record per source PDF).

Rules (set by the IACUC Administrator):
  - Every field comes from RASS only.
  - Sponsor award number blank in RASS -> "Not in RASS".
  - Any other required field missing -> record is marked STOP and lists the
    missing fields; the checklist should not be generated from it.
  - Year suffixes on the grant title ("- yrs 4 - 5") are removed.
  - One protocol: number only ("2021-0018").
  - Several protocols: semicolon-separated, in RASS table order.
      iacuc_protocol_number: "2021-0018 (Smith); 2021-0109 (Jones)"
      iacuc_pi:              "Jane Smith; Robert Jones"
      iacuc_protocol_title:  "Title one; Title two"
  - NetIDs are dropped from all names.
  - Sponsor abbreviation = last parenthesized abbreviation in Awarding Sponsor.
  - Congruence items are not extracted (they stay "Y" on the template).
"""
import datetime
import json
import os
import re
import sys
from pathlib import Path

import pdfplumber

# Folder handling: the scripts can live apart from the user's data. The data folder
# (RASS PDFs, templates, outputs, JSON) is RASS_FORMS_DIR if set, else this script's folder.
HERE = Path(os.environ.get("RASS_FORMS_DIR") or Path(__file__).resolve().parent)
OUT = HERE / "rass_extracted.json"
VALUE_X = 295        # Award Details: labels left of this, values right of it
LEFT_MARGIN_X = 47   # in the Compliances section, question text starts left of this
NOT_IN_RASS = "Not in RASS"
REQUIRED = ["osp_number", "grant_pi", "grant_title", "sponsor_abbreviation",
            "iacuc_protocol_number", "iacuc_pi", "iacuc_protocol_title"]


def strip_netid(name):
    return re.sub(r"\s*\([a-z]{2,4}\d+\)\s*$", "", name.strip()).strip()


YEARS_SUFFIX = re.compile(
    r"\s*[-–—:,(]*\s*\b(?:yrs?|years?)\.?\s*\d+(?:\s*(?:-|–|—|to|&|and|,)\s*\d+)*\s*\)?\s*$",
    re.IGNORECASE)


def strip_years(title):
    """'... environment? - yrs 4 - 5' -> '... environment?'"""
    return YEARS_SUFFIX.sub("", title).strip()


def last_name(name):
    return name.split()[-1] if name.split() else name


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


def all_lines(pdf):
    """Text lines across all pages, with a running y offset so page breaks sort."""
    lines, offset = [], 0.0
    for pg in pdf.pages:
        for ln in pg.extract_text_lines():
            words = [w for w in pg.extract_words()
                     if abs(w["top"] - ln["top"]) < 3 and ln["x0"] - 1 <= w["x0"] <= ln["x1"] + 1]
            size = max((c["size"] for c in ln.get("chars", [])), default=0)
            lines.append({"text": ln["text"], "x0": ln["x0"], "top": ln["top"] + offset,
                          "size": size,
                          "words": [{"text": w["text"], "x0": w["x0"]} for w in words]})
        offset += pg.height
    return lines


# RASS section headings ("Award Details", "Compliances", "Subawards", ...) are printed
# at ~13.5 pt; body text is 9-12 pt and the page header is 18 pt.
def is_section_heading(ln):
    return 13.0 <= ln["size"] <= 15.0 and ln["text"].strip() != ""


def section_span(lines, name):
    """(start, end) line indexes of a RASS section; end = next section heading."""
    start = next((i for i, l in enumerate(lines)
                  if is_section_heading(l) and l["text"].strip() == name), None)
    if start is None:
        return None, None
    end = next((i for i in range(start + 1, len(lines)) if is_section_heading(lines[i])
                or lines[i]["size"] > 15.0), len(lines))
    return start, end


def page_header(lines):
    """'Sponsored Research Protocol Application #OSP, PI: Name (netid)' + 'Title: ...'"""
    osp = pi = title = None
    for i, ln in enumerate(lines):
        m = re.match(r"Sponsored Research Protocol Application #(\S+), PI: (.+)", ln["text"])
        if m and osp is None:
            osp, pi = m.group(1), strip_netid(m.group(2))
        if ln["text"].startswith("Title:") and title is None:
            parts = [ln["text"][len("Title:"):]]
            for nxt in lines[i + 1:]:
                if is_section_heading(nxt) or nxt["size"] < 15.0:
                    break
                parts.append(nxt["text"])
            title = clean(" ".join(parts))
    return osp, pi, title


def award_details(lines):
    """Map Award Details label -> value, assigning each value line to the nearest label line."""
    start, end = section_span(lines, "Award Details")
    if start is None:
        return {}
    labels, values = [], []
    for ln in lines[start + 1:end]:
        lw = [w["text"] for w in ln["words"] if w["x0"] < VALUE_X]
        vw = [w["text"] for w in ln["words"] if w["x0"] >= VALUE_X]
        if lw:
            labels.append({"text": " ".join(lw), "top": ln["top"]})
        if vw:
            values.append({"text": " ".join(vw), "top": ln["top"]})
    out = {}
    for v in values:
        if not labels:
            break
        lab = min(labels, key=lambda l: abs(l["top"] - v["top"]))
        out.setdefault(lab["text"], []).append(v["text"])
    return {l["text"]: clean(" ".join(out.get(l["text"], []))) for l in labels}


def iacuc_table(lines):
    """Rows of the IACUC protocol table (the one after the live vertebrate animals question)."""
    c_start, c_end = section_span(lines, "Compliances")
    if c_start is None:
        return None
    q = next((i for i in range(c_start, c_end)
              if "live vertebrate animals (IACUC)" in lines[i]["text"]), None)
    if q is None:
        return None
    lines = lines[:c_end]   # never read past the Compliances section
    hdr = next((i for i in range(q, len(lines))
                if lines[i]["text"].startswith("Protocol #") and " PI " in f" {lines[i]['text']} "), None)
    if hdr is None or hdr - q > 3:
        return []   # question answered but no table
    hw = {w["text"]: w["x0"] for w in lines[hdr]["words"]}
    bounds = [("protocol", 0), ("title", hw["Title"] - 4), ("pi", hw["PI"] - 4),
              ("department", hw["Department"] - 4), ("status", hw["Status"] - 4),
              ("expiration", hw.get("Expiration", 9999) - 4)]
    rows, cur = [], None
    for ln in lines[hdr + 1:]:
        text = re.sub(r"[-]", "", ln["text"]).strip()   # drop expand/collapse icons
        if not ln["words"] or not text:
            continue
        if ln["x0"] < LEFT_MARGIN_X or is_section_heading(ln):   # next question/section
            break
        if ln["words"][0]["text"] == "Congruency":
            continue
        cols = {}
        for w in ln["words"]:
            name = [n for n, x in bounds if w["x0"] >= x][-1]
            cols.setdefault(name, []).append(w["text"])
        if "protocol" in cols:                 # a new protocol row starts
            cur = {n: [] for n, _ in bounds}
            rows.append(cur)
        if cur is not None:
            for n, ws in cols.items():
                cur[n] += ws
    return [{k: clean(" ".join(v)) for k, v in r.items()} for r in rows]


def extract(path):
    with pdfplumber.open(path) as pdf:
        lines = all_lines(pdf)
    h_osp, h_pi, h_title = page_header(lines)
    ad = award_details(lines)
    table = iacuc_table(lines)
    notes = []

    osp = ad.get("OSP #") or h_osp
    if h_osp and ad.get("OSP #") and h_osp != ad["OSP #"]:
        notes.append(f"OSP # differs: header {h_osp} vs Award Details {ad['OSP #']}")
    title = ad.get("Title") or h_title
    if h_title and ad.get("Title") and clean(h_title) != clean(ad["Title"]):
        title = h_title   # header line holds the full text if the table cell was clipped
        notes.append("Title in header and Award Details differ; header used")

    sponsor_full = ad.get("Awarding Sponsor", "")
    abbrs = re.findall(r"\(([^()]+)\)", sponsor_full)
    sponsor_abbr = abbrs[-1].strip() if abbrs else ""
    sponsor_no = ad.get("Sponsor Award Number", "") or NOT_IN_RASS

    rec = {
        "source_file": Path(path).name,
        "extracted_on": datetime.date.today().isoformat(),
        "comparison_date": datetime.date.today().isoformat(),
        "osp_number": osp or "",
        "grant_pi": h_pi or "",
        "grant_title": strip_years(title or ""),
        "sponsor_abbreviation": sponsor_abbr,
        "grant_sponsor_number": sponsor_no,
        "iacuc_protocol_number": "",
        "iacuc_pi": "",
        "iacuc_protocol_title": "",
        "awarding_sponsor_full": sponsor_full,
        "iacuc_protocols": [],
    }
    if table:
        pis = [strip_netid(r["pi"]) for r in table]
        if len(table) == 1:   # one protocol: number only
            rec["iacuc_protocol_number"] = table[0]["protocol"]
        else:                 # several: number (PI last name); ...
            rec["iacuc_protocol_number"] = "; ".join(f"{r['protocol']} ({last_name(p)})"
                                                     for r, p in zip(table, pis))
        rec["iacuc_pi"] = "; ".join(pis)
        rec["iacuc_protocol_title"] = "; ".join(r["title"] for r in table)
        rec["iacuc_protocols"] = [{"protocol": r["protocol"], "title": r["title"], "pi": p,
                                   "status": r["status"], "expiration": r["expiration"]}
                                  for r, p in zip(table, pis)]
        not_approved = [r["protocol"] for r in table if r["status"].lower() != "approved"]
        if not_approved:
            notes.append("Protocol status not 'Approved': " + ", ".join(not_approved))

    missing = [f for f in REQUIRED if not rec[f]]
    rec["status"] = "STOP" if missing else "OK"
    rec["missing_fields"] = missing
    rec["notes"] = notes
    return rec


def main(argv):
    files = [Path(a) for a in argv] or sorted(HERE.glob("*.pdf"))
    data = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else []
    by_file = {r["source_file"]: r for r in data}
    for f in files:
        rec = extract(f)
        by_file[rec["source_file"]] = rec
        flag = "OK  " if rec["status"] == "OK" else "STOP"
        extra = f"  missing: {', '.join(rec['missing_fields'])}" if rec["missing_fields"] else ""
        print(f"[{flag}] {rec['source_file']}  OSP {rec['osp_number']}{extra}")
        for n in rec["notes"]:
            print(f"       note: {n}")
    OUT.write_text(json.dumps(list(by_file.values()), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {OUT.name} ({len(by_file)} record(s))")


if __name__ == "__main__":
    main(sys.argv[1:])
