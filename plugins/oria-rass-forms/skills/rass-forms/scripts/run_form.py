"""
One command to turn RASS printouts into a filled form PDF.

    python run_form.py --list                 # show available forms and the RASS sections each needs
    python run_form.py congruence             # process new RASS PDFs in this folder
    python run_form.py congruence a.pdf b.pdf # process specific PDFs (any location)
    python run_form.py congruence --all       # reprocess every PDF in this folder
    add  --dir "<data folder>"  to any command when the scripts live elsewhere

"New" = a PDF in this folder that is not yet in the form's data file.
Each PDF is first checked for the RASS sections the form needs; a PDF missing a
section is reported and not processed.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pdfplumber

CODE = Path(__file__).resolve().parent          # where the scripts live
# Data folder: --dir <folder>, else RASS_FORMS_DIR, else the scripts' own folder.
if "--dir" in sys.argv:
    i = sys.argv.index("--dir")
    os.environ["RASS_FORMS_DIR"] = str(Path(sys.argv[i + 1]).resolve())
    del sys.argv[i:i + 2]
HERE = Path(os.environ.get("RASS_FORMS_DIR") or CODE)
os.environ["RASS_FORMS_DIR"] = str(HERE)          # passed on to the sub-scripts
# A forms.json in the data folder (local additions) overrides the shipped one.
_reg = HERE / "forms.json" if (HERE / "forms.json").exists() else CODE / "forms.json"
REG = json.loads(_reg.read_text(encoding="utf-8"))["forms"]


def find_form(key):
    key = key.lower()
    for f in REG:
        if key == f["id"] or key in (a.lower() for a in f.get("aliases", [])):
            return f
    sys.exit(f"Unknown form '{key}'. Known: {', '.join(f['id'] for f in REG)}")


def list_forms():
    for f in REG:
        print(f"{f['id']}: {f['name']}")
        print("   Include these RASS sections when downloading the PDF:")
        for s in f["rass_sections"]:
            print(f"     - {s}")
        opt = f.get("optional_sections", [])
        if opt:
            print("   Also include, when it applies:")
            for o in opt:
                print(f"     - {o['section']}: {o.get('when', '')}")


def missing_sections(pdf_path, markers):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    return [m for m in markers if m not in text]


def main(argv):
    if not argv or argv[0] == "--list":
        list_forms()
        return
    form = find_form(argv[0])
    args = argv[1:]
    data_file = HERE / form["data_file"]
    done = set()
    if data_file.exists():
        done = {r["source_file"] for r in json.loads(data_file.read_text(encoding="utf-8"))}

    if args and args != ["--all"]:
        pdfs = [Path(a).resolve() for a in args]
    else:
        pdfs = sorted(HERE.glob("*.pdf"))
        if args != ["--all"]:
            pdfs = [p for p in pdfs if p.name not in done]
    if not pdfs:
        print("No new RASS PDFs found in the folder.")
        return

    ready = []
    for p in pdfs:
        gone = missing_sections(p, form["section_markers"])
        if gone:
            print(f"[STOP] {p.name}: RASS PDF is missing section(s): {', '.join(gone)}")
        else:
            ready.append(p)
            for o in form.get("optional_sections", []):
                found = not missing_sections(p, [o["marker"]])
                print(f"[INFO] {p.name}: optional section '{o['section']}' "
                      f"{'included' if found else 'not in RASS PDF'}")
    if not ready:
        return

    py = sys.executable
    if subprocess.run([py, str(CODE / form["extract_script"]), *map(str, ready)]).returncode != 0:
        sys.exit(1)
    recs = json.loads(data_file.read_text(encoding="utf-8"))
    names = {p.name for p in ready}
    osps = [r["osp_number"] for r in recs if r["source_file"] in names and r["osp_number"]]
    if subprocess.run([py, str(CODE / form["fill_script"]), *osps]).returncode != 0:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
