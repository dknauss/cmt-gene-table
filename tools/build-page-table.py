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
"""
import csv, html, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INH = {"AD": "Dominant", "AR": "Recessive", "SD": "Semidominant", "XL": "X-linked"}
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
