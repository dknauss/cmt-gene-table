#!/usr/bin/env python3
"""Merge data/clingen-cmt.csv and data/subtype-names.csv into data/cmt-genes.csv.

ClinGen columns are copied unchanged. Subtype names, their MONDO IDs and the
OMIM phenotype IDs come from data/subtype-names.csv (Monarch/MONDO). Columns
for hand review are left blank.
"""
import csv
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FIELDS = [
    "gene", "hgnc_id", "clingen_disease_label", "mondo_id", "inheritance",
    "clingen_classification", "classification_date", "clingen_report",
    "type_named_in_label", "historical_subtype_names", "subtype_mondo_ids",
    "omim_phenotype_ids", "subtype_review_note", "phenotype", "genereviews",
    "panelapp", "therapy_programs", "plain_note",
]

base = list(csv.DictReader(open(os.path.join(D, "clingen-cmt.csv"), encoding="utf-8")))
sub = {r["gene"]: r for r in csv.DictReader(open(os.path.join(D, "subtype-names.csv"), encoding="utf-8"))}

with open(os.path.join(D, "cmt-genes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    for r in base:
        s = sub.get(r["gene"], {})
        out = {k: r.get(k, "") for k in FIELDS}
        out["historical_subtype_names"] = s.get("historical_subtype_names", "")
        out["subtype_mondo_ids"] = s.get("mondo_ids", "")
        out["omim_phenotype_ids"] = s.get("omim_phenotype_ids", "")
        out["subtype_review_note"] = s.get("notes", "")
        w.writerow(out)
print(f"{len(base)} rows written to data/cmt-genes.csv")
