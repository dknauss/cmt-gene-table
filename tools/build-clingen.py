#!/usr/bin/env python3
"""Build the draft Open CMT Gene Table from ClinGen's gene-disease validity data.

Downloads ClinGen's public CSV (CC0), keeps the curations made by the
Charcot-Marie-Tooth Disease Gene Curation Expert Panel, and writes
data/clingen-cmt.csv. Columns that ClinGen does not supply are left
blank for hand review, so nothing in the output is guessed.

Usage: python3 tools/build-gene-table.py [path-to-downloaded-clingen.csv]
"""
import csv
import os
import re
import sys
import urllib.request

SOURCE = "https://search.clinicalgenome.org/kb/gene-validity/download"
PANEL = "Charcot-Marie-Tooth Disease Gene Curation Expert Panel"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "clingen-cmt.csv")

FIELDS = [
    "gene", "hgnc_id", "clingen_disease_label", "mondo_id", "inheritance",
    "clingen_classification", "classification_date", "clingen_report",
    "type_named_in_label", "historical_subtype_names", "phenotype",
    "genereviews", "panelapp", "omim_id", "therapy_programs", "plain_note",
]


def subtype_from_label(label):
    """Return the CMT subtype a ClinGen label names explicitly, else ''."""
    m = re.search(r"Charcot-Marie-Tooth disease,?\s+(?:axonal,?\s+|demyelinating,?\s+)?type\s+([0-9][A-Z0-9]*)", label, re.I)
    if m:
        return "CMT" + m.group(1).upper()
    m = re.search(r"Charcot-Marie-Tooth disease X-linked (?:dominant|recessive) (\d+)", label, re.I)
    if m:
        return "CMTX" + m.group(1)
    m = re.search(r"Charcot-Marie-Tooth disease dominant intermediate ([A-Z])", label, re.I)
    if m:
        return "CMTDI" + m.group(1).upper()
    m = re.search(r"Charcot-Marie-Tooth disease (?:recessive|autosomal recessive) intermediate ([A-Z])", label, re.I)
    if m:
        return "CMTRI" + m.group(1).upper()
    return ""


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if path:
        text = open(path, encoding="utf-8").read()
    else:
        req = urllib.request.Request(SOURCE, headers={"User-Agent": "cmt.blog gene table builder"})
        text = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
    rows = list(csv.reader(text.splitlines()))
    created = next((r[0] for r in rows if r and r[0].startswith("FILE CREATED")), "")
    header_i = next(i for i, r in enumerate(rows) if r and r[0] == "GENE SYMBOL")
    head = rows[header_i]
    idx = {name: head.index(name) for name in head}
    out = []
    for r in rows[header_i + 1:]:
        if len(r) != len(head) or r[idx["GCEP"]] != PANEL:
            continue
        label = r[idx["DISEASE LABEL"]]
        out.append({
            "gene": r[idx["GENE SYMBOL"]],
            "hgnc_id": r[idx["GENE ID (HGNC)"]],
            "clingen_disease_label": label,
            "mondo_id": r[idx["DISEASE ID (MONDO)"]],
            "inheritance": r[idx["MOI"]],
            "clingen_classification": r[idx["CLASSIFICATION"]],
            "classification_date": r[idx["CLASSIFICATION DATE"]][:10],
            "clingen_report": r[idx["ONLINE REPORT"]],
            "type_named_in_label": subtype_from_label(label),
        })
    out.sort(key=lambda x: (x["gene"], x["clingen_disease_label"]))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        for row in out:
            w.writerow({k: row.get(k, "") for k in FIELDS})
    print(f"{len(out)} curations, {len({r['gene'] for r in out})} genes; ClinGen {created}")


if __name__ == "__main__":
    main()
