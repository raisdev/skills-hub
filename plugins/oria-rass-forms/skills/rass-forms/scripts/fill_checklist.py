"""
Fill the Grant-IACUC Protocol Comparison Checklist template from rass_extracted.json
and save a PDF for each record whose status is OK.

Usage:
    python fill_checklist.py            # every OK record in rass_extracted.json
    python fill_checklist.py 203892     # only the given OSP numbers

Output: Checklists/<OSP> to <protocol numbers>.pdf  (in this folder)
STOP records are skipped and reported. Congruence items, Corrective Action ("No")
and Follow Up ("None") are left exactly as in the template.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

# Folder handling: the scripts can live apart from the user's data. The data folder
# (RASS PDFs, templates, outputs, JSON) is RASS_FORMS_DIR if set, else this script's folder.
HERE = Path(os.environ.get("RASS_FORMS_DIR") or Path(__file__).resolve().parent)
TEMPLATE = HERE / "OSP to IACUC Template GCC.dotx"
DATA = HERE / "rass_extracted.json"
OUTDIR = HERE / "Checklists"

# Label in the left header cell -> JSON field
HEADER_FIELDS = {
    "Comparison Date": "comparison_date",
    "OSP#": "osp_number",
    "Proposal/Grant PI": "grant_pi",
    "Proposal/Grant Title": "grant_title",
    "Sponsor Abbreviation": "sponsor_abbreviation",
    "Grant Sponsor #": "grant_sponsor_number",
    "IACUC Protocol #": "iacuc_protocol_number",
    "IACUC PI": "iacuc_pi",
    "IACUC Protocol Title": "iacuc_protocol_title",
}
RUN = '<w:r><w:rPr><w:sz w:val="15"/></w:rPr><w:t xml:space="preserve">{}</w:t></w:r>'


def text_of(xml):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", xml)).strip()


def set_cell_text(cell, value):
    """Replace all runs in the cell's (single) paragraph with one run holding value."""
    cell = re.sub(r"<w:r>.*?</w:r>|<w:r [^>]*>.*?</w:r>", "", cell, flags=re.S)
    return re.sub(r"(<w:p [^>]*>.*?</w:pPr>|<w:p [^>]*>)(.*?)(</w:p>)",
                  lambda m: m.group(1) + RUN.format(escape(value)) + m.group(3),
                  cell, count=1, flags=re.S)


def fill(xml, rec):
    protos = [p["protocol"] for p in rec.get("iacuc_protocols", [])]
    title_line = f"{rec['osp_number']} to {rec['iacuc_protocol_number']}"

    # Document title
    xml = xml.replace("&lt;OSP #&gt; to &lt;IACUC Protocol #&gt;", escape(title_line), 1)

    # Header rows: label cell, value cell
    def fix_row(m):
        row = m.group(0)
        cells = re.findall(r"<w:tc>.*?</w:tc>", row, re.S)
        if len(cells) != 2:
            return row
        field = HEADER_FIELDS.get(text_of(cells[0]))
        if not field:
            return row
        return row.replace(cells[1], set_cell_text(cells[1], rec[field]), 1)
    first_table = re.search(r"<w:tbl>.*?</w:tbl>", xml, re.S)
    filled = re.sub(r"<w:tr[ >].*?</w:tr>", fix_row, first_table.group(0), flags=re.S)
    xml = xml[:first_table.start()] + filled + xml[first_table.end():]

    # Comment sentence: replace the two yellow-highlighted placeholders, remove highlight
    proto_word = "protocols" if len(protos) > 1 else "protocol"
    xml = xml.replace("<w:t>OSP#XX</w:t>", f"<w:t>OSP# {escape(rec['osp_number'])}</w:t>", 1)
    xml = xml.replace("<w:t>protocol XX</w:t>",
                      f"<w:t>{proto_word} {escape(rec['iacuc_protocol_number'])}</w:t>", 1)
    if len(protos) > 1:
        xml = xml.replace("IACUC protocol are </w:t>", "IACUC protocols are </w:t>", 1)
    xml = xml.replace('<w:highlight w:val="yellow"/>', "")
    return xml, title_line


def safe_name(s):
    return re.sub(r'[\\/:*?"<>|]', "-", s).strip()


def build(rec, workdir):
    out_docx = workdir / "checklist.docx"
    with zipfile.ZipFile(TEMPLATE) as zin, zipfile.ZipFile(out_docx, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                xml, title_line = fill(data.decode("utf-8"), rec)
                data = xml.encode("utf-8")
            elif item.filename == "[Content_Types].xml":   # template -> document
                data = data.replace(b"wordprocessingml.template.main+xml",
                                    b"wordprocessingml.document.main+xml")
            zout.writestr(item, data)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(workdir),
                    str(out_docx)], check=True, capture_output=True, timeout=180)
    pdf_name = safe_name(f"{rec['osp_number']} to " +
                         ", ".join(p["protocol"] for p in rec["iacuc_protocols"])) + ".pdf"
    OUTDIR.mkdir(exist_ok=True)
    dest = OUTDIR / pdf_name
    n = 2
    while True:
        try:
            shutil.copyfile(workdir / "checklist.pdf", dest)
            break
        except PermissionError:   # existing PDF is open/locked -> save a numbered copy
            dest = OUTDIR / f"{Path(pdf_name).stem} ({n}).pdf"
            n += 1
            if n > 20:
                raise
    return dest, title_line


def main(argv):
    if not TEMPLATE.exists():
        sys.exit(f"[STOP] Template not found: '{TEMPLATE.name}' must be saved in {HERE}")
    records = json.loads(DATA.read_text(encoding="utf-8"))
    if argv:
        records = [r for r in records if r["osp_number"] in argv]
    for rec in records:
        if rec["status"] != "OK":
            print(f"[SKIP] {rec['source_file']}: STOP, missing {', '.join(rec['missing_fields'])}")
            continue
        with tempfile.TemporaryDirectory() as td:
            dest, title = build(rec, Path(td))
        print(f"[DONE] {title}  ->  {dest.relative_to(HERE)}")


if __name__ == "__main__":
    main(sys.argv[1:])
