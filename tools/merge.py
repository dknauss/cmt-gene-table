#!/usr/bin/env python3
"""Merge the source files into data/cmt-genes.csv.

- ClinGen columns are copied unchanged from data/clingen-cmt.csv.
- Subtype names, their Mondo IDs and the OMIM phenotype IDs come from
  data/subtype-names.csv (Monarch/Mondo).
- genereviews and panelapp come from data/links.csv (tools/fetch-links.py).
- phenotype, therapy_programs and plain_note come from
  data/hand-checked-sources.csv, where every value carries its source URL.
  Several rows for one gene and column are joined with "; ". A column with
  no hand-checked row is left blank.
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
links = {}
if os.path.exists(os.path.join(D, "links.csv")):
    links = {r["gene"]: r for r in csv.DictReader(open(os.path.join(D, "links.csv"), encoding="utf-8"))}
HAND = ("phenotype", "therapy_programs", "plain_note")
hand = {}
if os.path.exists(os.path.join(D, "hand-checked-sources.csv")):
    for h in csv.DictReader(open(os.path.join(D, "hand-checked-sources.csv"), encoding="utf-8")):
        if h["column"] not in HAND:
            raise SystemExit(f"hand-checked-sources.csv: unknown column {h['column']!r}")
        if not h["source_url"].startswith("http"):
            raise SystemExit(f"hand-checked-sources.csv: {h['gene']} {h['column']} has no source URL")
        vals = hand.setdefault((h["gene"], h["column"]), [])
        if h["value"] not in vals:
            vals.append(h["value"])

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
        l = links.get(r["gene"], {})
        out["genereviews"] = l.get("genereviews", "")
        out["panelapp"] = l.get("panelapp", "")
        for c in HAND:
            out[c] = "; ".join(hand.get((r["gene"], c), []))
        w.writerow(out)
print(f"{len(base)} rows written to data/cmt-genes.csv")
