#!/usr/bin/env python3
"""Build the <tbody> for the table on https://cmt.blog/cmt-gene-table/.

Reads data/cmt-genes.csv and writes site/table-body.html. Each row shows the
subtype names attached to that curation. Other names linked to the gene, but
not covered by the rating in that row, follow in italics, as do older or
unverified names (from correlated associations only). Names rejected in
data/name-reviews.csv are left out. Rows that need a
note get a [[FN:KEY]] placeholder, which the page's footnote IDs replace.
A gene with more than one curation gets one key per row ([[FN:PMP22:MONDO:0007309]]),
because WordPress core footnotes cannot point two markers at one note: the
block editor duplicates the note on save.

It also writes site/candidate-table-body.html from data/candidate-genes.csv,
for the separate list of genes reported with CMT-spectrum disease that ClinGen
has not curated for it. Its ClinGen cell gives the clingen_scope label and,
for a curated gene, the curation details; later papers in more_pmids are
linked after the key source.
"""
import csv, html, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INH = {"AD": "Dominant", "AR": "Recessive", "SD": "Semidominant", "XL": "X-linked", "MT": "Mitochondrial"}
# Labels for clingen_scope in data/candidate-genes.csv (gene-disease validity only).
SCOPE = {
    "not curated": "Not curated",
    "other disease": "Curated for another disease",
    "refuted other disease": "Refuted for another disease",
    "neuropathy not scored": "Curated for another disease; neuropathy discussed, not scored",
    "includes neuropathy": "Curated for a broader disease that includes the neuropathy",
    "scope unresolved": "Curated for a broader disease; coverage of the neuropathy unresolved",
}
NOTE = {"FBLN5", "HINT1", "MED25", "MFN2", "SCN11A", "SORD", "NEFL", "PMP22", "NTRK1"}

rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "cmt-genes.csv"), encoding="utf-8")))
per_gene = {}
for r in rows:
    per_gene[r["gene"]] = per_gene.get(r["gene"], 0) + 1
out = []
for r in rows:
    names = [x.strip() for x in r["curation_subtype_names"].split(";") if x.strip()]
    other = [x.strip() for x in r["other_gene_names"].split(";") if x.strip()]
    older = [x.strip() for x in r["unverified_names"].split(";") if x.strip()]
    cell = html.escape(", ".join(names)) if names else "—"
    if r["gene"] in NOTE:
        key = r["gene"] if per_gene[r["gene"]] == 1 else f"{r['gene']}:{r['mondo_id']}"
        cell += f"[[FN:{key}]]"
    extra = []
    if other:
        extra.append("Other names, not rated here: " + html.escape(", ".join(other)) + ".")
    if older:
        extra.append("Older or unverified: " + html.escape(", ".join(older)) + ".")
    if extra:
        cell += "<br><em>" + " ".join(extra) + "</em>"
    year = r["classification_date"][:4]
    out.append(
        "<tr>"
        f"<td><strong>{html.escape(r['gene'])}</strong></td>"
        f"<td>{cell}</td>"
        f"<td>{html.escape(r['clingen_disease_label'])}</td>"
        f"<td>{INH.get(r['inheritance'], html.escape(r['inheritance']))}</td>"
        f"<td><a href=\"https://search.clinicalgenome.org/kb/genes/{r['hgnc_id']}\">{html.escape(r['clingen_classification'])}</a> ({year})</td>"
        "</tr>"
    )
os.makedirs(os.path.join(ROOT, "site"), exist_ok=True)
open(os.path.join(ROOT, "site", "table-body.html"), "w", encoding="utf-8").write("<tbody>" + "".join(out) + "</tbody>")
print(f"{len(out)} rows written to site/table-body.html")

cand = list(csv.DictReader(open(os.path.join(ROOT, "data", "candidate-genes.csv"), encoding="utf-8")))
out = []
for r in cand:
    status = SCOPE[r["clingen_scope"]]
    detail = ""
    if r["clingen_scope"] != "not curated":
        detail = "<br><em>" + html.escape(r["clingen_status"].split(": ", 1)[1]) + "</em>"
    src = f"<a href=\"https://pubmed.ncbi.nlm.nih.gov/{r['key_pmid']}/\">{html.escape(r['key_source'])}</a>"
    more = [p.strip() for p in r["more_pmids"].split(";") if p.strip()]
    if more:
        src += "; also " + ", ".join(f"<a href=\"https://pubmed.ncbi.nlm.nih.gov/{p}/\">PMID {p}</a>" for p in more)
    out.append(
        "<tr>"
        f"<td><strong>{html.escape(r['gene'])}</strong></td>"
        f"<td>{html.escape(r['reported_disease'])}</td>"
        f"<td>{INH.get(r['inheritance'], html.escape(r['inheritance']))}</td>"
        f"<td><a href=\"https://search.clinicalgenome.org/kb/genes/{r['hgnc_id']}\">{status}</a>{detail}</td>"
        f"<td>{html.escape(r['evidence_note'])}<br><em>{src}</em></td>"
        "</tr>"
    )
open(os.path.join(ROOT, "site", "candidate-table-body.html"), "w", encoding="utf-8").write("<tbody>" + "".join(out) + "</tbody>")
print(f"{len(out)} rows written to site/candidate-table-body.html")
