#!/usr/bin/env python3
"""Build the <tbody> for the table on https://cmt.blog/cmt-gene-table/.

Reads data/cmt-genes.csv and writes site/table-body.html. Each row shows the
subtype names attached to that curation. Other names linked to the gene, but
not covered by the rating in that row, follow in italics. Rows that need a
note get a [[FN:KEY]] placeholder, which the page's footnote IDs replace.
"""
import csv, html, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INH = {"AD": "Dominant", "AR": "Recessive", "SD": "Semidominant", "XL": "X-linked"}
NOTE = {"FBLN5", "HINT1", "MED25", "MFN2", "SCN11A", "SORD", "NEFL", "PMP22", "NTRK1"}

rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "cmt-genes.csv"), encoding="utf-8")))
out = []
for r in rows:
    names = [x.strip() for x in r["curation_subtype_names"].split(";") if x.strip()]
    other = [x.strip() for x in r["other_gene_names"].split(";") if x.strip()]
    cell = html.escape(", ".join(names)) if names else "—"
    if r["gene"] in NOTE:
        cell += f"[[FN:{r['gene']}]]"
    if other:
        cell += "<br><em>Also linked to this gene: " + html.escape(", ".join(other)) + "</em>"
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
