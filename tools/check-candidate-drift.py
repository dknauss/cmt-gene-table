#!/usr/bin/env python3
"""Report ClinGen changes that affect the additional-genes list.

The list (data/candidate-genes.csv) and the screened genes left out of it
(data/candidate-genes-excluded.csv) are checked by hand, so the monthly job
does not rewrite them. This script compares both files with ClinGen's current
gene-disease validity download, matched by HGNC ID, and reports:

- a listed or excluded gene that ClinGen's CMT panel now curates (it belongs
  in the main table);
- a listed gene whose curations differ from those named in clingen_status
  (new, removed, or changed classification, inheritance, panel, or date);
- an excluded gene whose clingen_curations no longer matches ClinGen
  (fix with tools/fill-excluded-curations.py).

It changes no files. With --report PATH it writes a Markdown report there
when anything changed. It always exits 0 unless the inputs cannot be read,
so the monthly job can open an issue rather than fail.

Usage: python3 tools/check-candidate-drift.py [--refresh] [--report PATH]
"""
import csv
import importlib.util
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CMT_PANEL = "Charcot-Marie-Tooth Disease panel"

# Reuse the download, panel naming, and formatting of the fill tool.
_spec = importlib.util.spec_from_file_location(
    "fill_excluded_curations", os.path.join(ROOT, "tools", "fill-excluded-curations.py"))
fill = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fill)

# "disease (Classification, MOI, Some panel, YYYY-MM-DD)" as written in clingen_status.
ENTRY = re.compile(
    r"([^;:()]+?) \(([A-Z][A-Za-z ]+?), ([A-Za-z]+), ([^,()]+? panel), (\d{4}-\d{2}-\d{2})\)")


def stated(status):
    """Curations named in a clingen_status note, as a set of tuples."""
    out = set()
    for m in ENTRY.finditer(status):
        disease = m.group(1).strip()
        # Drop lead-in prose such as "Also curated for" or "A separate recessive curation,".
        disease = re.split(r"(?:curated for|curation,|Also)\s+", disease)[-1].strip()
        out.add((disease, m.group(2), m.group(3), m.group(4), m.group(5)))
    return out


def current(curations):
    return {(c["disease"], c["classification"], c["moi"], c["panel"], c["date"]) for c in curations}


def fmt(t):
    return f"{t[0]} ({t[1]}, {t[2]}, {t[3]}, {t[4]})"


def main():
    refresh = "--refresh" in sys.argv
    report = sys.argv[sys.argv.index("--report") + 1] if "--report" in sys.argv else None
    by_hgnc = fill.load_clingen(refresh)

    listed = list(csv.DictReader(open(os.path.join(ROOT, "data", "candidate-genes.csv"), encoding="utf-8")))
    excluded = list(csv.DictReader(open(os.path.join(ROOT, "data", "candidate-genes-excluded.csv"), encoding="utf-8")))

    moves, listed_changes, excluded_changes = [], [], []
    for r in listed + excluded:
        cmt = [c for c in by_hgnc.get(r["hgnc_id"], []) if c["panel"] == CMT_PANEL]
        if cmt:
            moves.append(f"- **{r['gene']}** ({r['hgnc_id']}): " + "; ".join(fmt(t) for t in sorted(current(cmt))))

    for r in listed:
        now = current(by_hgnc.get(r["hgnc_id"], []))
        was = stated(r["clingen_status"])
        if r["clingen_scope"] == "not curated" and not now:
            continue
        added, removed = sorted(now - was), sorted(was - now)
        if added or removed:
            lines = [f"- **{r['gene']}** ({r['hgnc_id']}, `clingen_scope`: {r['clingen_scope']})"]
            lines += [f"  - now in ClinGen: {fmt(t)}" for t in added]
            lines += [f"  - no longer in ClinGen as written: {fmt(t)}" for t in removed]
            listed_changes.append("\n".join(lines))

    for r in excluded:
        new = fill.curations_text(by_hgnc.get(r["hgnc_id"], []))
        if new != r["clingen_curations"]:
            excluded_changes.append(f"- **{r['gene']}**: `{r['clingen_curations']}` → `{new}`")

    sections = []
    if moves:
        sections.append("### Now curated by ClinGen's CMT panel\n\nMove these into the main table, with a dated changelog entry.\n\n" + "\n".join(moves))
    if listed_changes:
        sections.append("### Listed genes whose ClinGen curations changed\n\nRe-read each curation, then update `clingen_status` and `clingen_scope` by hand.\n\n" + "\n".join(listed_changes))
    if excluded_changes:
        sections.append("### Excluded genes whose curations changed\n\nRun `python3 tools/fill-excluded-curations.py`, and check whether the change affects the exclusion.\n\n" + "\n".join(excluded_changes))

    counts = f"{len(moves)} to move, {len(listed_changes)} listed, {len(excluded_changes)} excluded"
    if not sections:
        print(f"No ClinGen changes for the {len(listed)} listed and {len(excluded)} excluded genes.")
        return
    text = ("ClinGen's gene-disease validity download differs from the additional-genes files "
            f"({counts}).\n\n" + "\n\n".join(sections) + "\n")
    print(text)
    if report:
        open(report, "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    main()
