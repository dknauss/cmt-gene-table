#!/usr/bin/env python3
"""Merge the source files into data/cmt-genes.csv, one row per ClinGen curation.

- ClinGen columns are copied unchanged from data/clingen-cmt.csv.
- curation_subtype_names are attached to the curation they belong to, using
  the OMIM phenotypes ClinGen says the curation includes
  (data/clingen-phenotypes.csv, from tools/fetch-clingen-phenotypes.py) and
  the Mondo terms behind each name (data/subtype-terms.csv, from
  tools/build-subtypes.py). curation_names_basis says how they were matched.
- other_gene_names are causal subtype names for the gene that this curation
  does not cover. unverified_names come only from Monarch correlated (not
  causal) associations; they are kept for review, not presented as subtypes.
- historical_subtype_names, subtype_mondo_ids and omim_phenotype_ids are the
  gene-wide lists from data/subtype-names.csv, kept for compatibility.
- genereviews and panelapp come from data/links.csv (tools/fetch-links.py).
- phenotype, therapy_programs, other_condition_trials and plain_note come
  from data/hand-checked-sources.csv, where every value carries its source
  URL. A row with a mondo_id applies only to that curation; a blank mondo_id
  applies to every curation of the gene. A column with no hand-checked row is
  left blank.
"""
import csv
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
FIELDS = [
    "gene", "hgnc_id", "clingen_disease_label", "mondo_id", "inheritance",
    "clingen_classification", "classification_date", "clingen_report",
    "type_named_in_label", "curation_subtype_names", "curation_names_basis",
    "other_gene_names", "unverified_names", "clingen_included_omim",
    "clingen_excluded_omim", "historical_subtype_names", "subtype_mondo_ids",
    "omim_phenotype_ids", "subtype_review_note", "phenotype", "genereviews",
    "panelapp", "therapy_programs", "other_condition_trials", "plain_note",
]
HAND = ("phenotype", "therapy_programs", "other_condition_trials", "plain_note")


def read(name):
    path = os.path.join(D, name)
    return list(csv.DictReader(open(path, encoding="utf-8"))) if os.path.exists(path) else []


def split(v):
    return [x.strip() for x in v.split(";") if x.strip()]


def add(lst, names):
    for n in names:
        if n not in lst:
            lst.append(n)


base = read("clingen-cmt.csv")
sub = {r["gene"]: r for r in read("subtype-names.csv")}
links = {r["gene"]: r for r in read("links.csv")}
pheno = {(r["gene"], r["mondo_id"]): r for r in read("clingen-phenotypes.csv")}
terms = {}
for t in read("subtype-terms.csv"):
    terms.setdefault(t["gene"], []).append(t)

hand = {}
for h in read("hand-checked-sources.csv"):
    if h["column"] not in HAND:
        raise SystemExit(f"hand-checked-sources.csv: unknown column {h['column']!r}")
    if not h["source_url"].startswith("http"):
        raise SystemExit(f"hand-checked-sources.csv: {h['gene']} {h['column']} has no source URL")
    vals = hand.setdefault((h["gene"], h.get("mondo_id", ""), h["column"]), [])
    if h["value"] not in vals:
        vals.append(h["value"])


def curation_names(r):
    gt = terms.get(r["gene"], [])
    p = pheno.get((r["gene"], r["mondo_id"]), {})
    inc = set(split(p.get("included_omim", "")))
    cur, basis = [], ""
    if inc:
        for t in gt:
            if inc & set(split(t["omim_ids"])):
                add(cur, split(t["short_names"]))
        matched = {o for t in gt for o in split(t["omim_ids"]) if o in inc}
        basis = "ClinGen included MIM phenotypes"
        if inc - matched:
            basis += " (unmatched: " + ", ".join(sorted(inc - matched)) + ")"
    elif any(t["mondo_id"] == r["mondo_id"] for t in gt):
        for t in gt:
            if t["mondo_id"] == r["mondo_id"]:
                add(cur, split(t["short_names"]))
        basis = "ClinGen disease term"
    else:
        for t in gt:
            if t["association"] != "correlated":
                add(cur, split(t["short_names"]))
        basis = "gene-wide: this curation lists no MIM phenotypes" if cur else ""
    if not cur and any(t["mondo_id"] == r["mondo_id"] for t in gt):
        for t in gt:
            if t["mondo_id"] == r["mondo_id"]:
                add(cur, split(t["short_names"]))
        basis = (basis + "; " if basis else "") + "names from the ClinGen disease term"
    other, unverified = [], []
    for t in gt:
        names = [n for n in split(t["short_names"]) if n not in cur]
        add(unverified if t["association"] == "correlated" else other, names)
    return cur, basis, other, unverified, p


with open(os.path.join(D, "cmt-genes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    for r in base:
        s = sub.get(r["gene"], {})
        out = {k: r.get(k, "") for k in FIELDS}
        cur, basis, other, unverified, p = curation_names(r)
        out["curation_subtype_names"] = "; ".join(cur)
        out["curation_names_basis"] = basis
        out["other_gene_names"] = "; ".join(other)
        out["unverified_names"] = "; ".join(unverified)
        out["clingen_included_omim"] = p.get("included_omim", "")
        out["clingen_excluded_omim"] = p.get("excluded_omim", "")
        out["historical_subtype_names"] = s.get("historical_subtype_names", "")
        out["subtype_mondo_ids"] = s.get("mondo_ids", "")
        out["omim_phenotype_ids"] = s.get("omim_phenotype_ids", "")
        out["subtype_review_note"] = s.get("notes", "")
        l = links.get(r["gene"], {})
        out["genereviews"] = l.get("genereviews", "")
        out["panelapp"] = l.get("panelapp", "")
        for c in HAND:
            specific = hand.get((r["gene"], r["mondo_id"], c))
            out[c] = "; ".join(specific if specific else hand.get((r["gene"], "", c), []))
        w.writerow(out)
print(f"{len(base)} rows written to data/cmt-genes.csv")
