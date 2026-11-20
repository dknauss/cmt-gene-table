#!/usr/bin/env python3
"""Build the downloadable files and the static web page from data/cmt-genes.csv.

Writes to dist/ (not committed):

  dist/cmt-genes.csv        the table, unchanged
  dist/cmt-genes.xlsx       the table, a column guide and an About sheet
  dist/cmt-genes.json       one object per row
  dist/datapackage.json     Frictionless Data Package describing every column
  dist/index.html           the GitHub Pages site: searchable table and downloads
  dist/candidate-genes.csv  the separate candidate list, unchanged (also .json)
  dist/candidate-genes-excluded.csv  screened genes left out of it, with reasons

The column descriptions come from the column tables in README.md, so the
README stays the single place to edit them. The build stops if a gene is in
both the main table and the candidate list.

Usage: python3 tools/build-exports.py [--version v2026.10]
The version defaults to the VERSION environment variable, then to "dev".
"""
import csv, datetime, html, json, os, re, shutil, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DIST = os.path.join(ROOT, "dist")
REPO = "https://github.com/dknauss/cmt-gene-table"
PAGES = "https://dknauss.github.io/cmt-gene-table/"
BLOG = "https://cmt.blog/cmt-gene-table/"
TITLE = "Open CMT Gene Table"
CREDIT = "Open CMT Gene Table (cmt.blog), using ClinGen (CC0) and Mondo (CC BY 4.0)"
SCOPE = {
    "not curated": "Not curated",
    "other disease": "Curated for another disease",
    "refuted other disease": "Refuted for another disease",
    "neuropathy not scored": "Curated for another disease; neuropathy discussed, not scored",
    "includes neuropathy": "Curated for a broader disease that includes the neuropathy",
    "scope unresolved": "Curated for a broader disease; coverage of the neuropathy unresolved",
}
INH = {"AD": "Dominant", "AR": "Recessive", "SD": "Semidominant", "XL": "X-linked", "MT": "Mitochondrial"}


def version():
    if "--version" in sys.argv:
        return sys.argv[sys.argv.index("--version") + 1]
    return os.environ.get("VERSION") or "dev"


def column_guide(fields, start="## The Data", stop="## "):
    """Read a README column table: {column: (source, description)}.

    Only lines from the heading `start` to the next heading that begins with
    `stop` are read, so the main and candidate tables can share column names.
    """
    guide = {}
    text = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    lines, inside = [], False
    for line in text.splitlines():
        if line.strip() == start:
            inside = True
            continue
        if inside and line.startswith(stop) and not line.startswith(stop + "#"):
            break
        if inside:
            lines.append(line)
    for line in lines:
        m = re.match(r"^\|\s*(`[^|]+`)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|$", line)
        if not m:
            continue
        names = re.findall(r"`([^`]+)`", m.group(1))
        for n in names:
            desc = m.group(3).replace("`; `", "semicolons").replace(" below", " in the README")
            guide[n] = (m.group(2).strip(), re.sub(r"`([^`]+)`", r"\1", desc).strip())
    missing = [f for f in fields if f not in guide]
    if missing:
        sys.exit("README column table is missing: " + ", ".join(missing))
    return guide


def split_links(value):
    """'Label: https://…; Label: https://…' -> [(label, url)]."""
    out = []
    for part in [p.strip() for p in value.split("; ") if p.strip()]:
        m = re.match(r"^(.*?):\s+(https?://\S+)$", part)
        out.append((m.group(1), m.group(2)) if m else (part, None))
    return out


def links_html(value):
    items = []
    for label, url in split_links(value):
        label = html.escape(label)
        items.append(f'<a href="{html.escape(url)}">{label}</a>' if url else label)
    return "; ".join(items)


def names(value):
    return [x.strip() for x in value.split(";") if x.strip()]


def build_xlsx(rows, fields, guide, ver, path, cand=None):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "CMT genes"
    ws.append(fields)
    for r in rows:
        ws.append([r[f] for f in fields])
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions
    for i, f in enumerate(fields, 1):
        longest = max([len(f)] + [len(r[f]) for r in rows])
        ws.column_dimensions[get_column_letter(i)].width = min(max(10, longest + 2), 60)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(vertical="top", wrap_text=len(str(c.value or "")) > 60)

    cg = wb.create_sheet("Columns")
    cg.append(["column", "source", "description"])
    for f in fields:
        cg.append([f, guide[f][0], guide[f][1]])
    for c in cg[1]:
        c.font = Font(bold=True)
    cg.column_dimensions["A"].width = 28
    cg.column_dimensions["B"].width = 26
    cg.column_dimensions["C"].width = 100
    for row in cg.iter_rows(min_row=2):
        row[2].alignment = Alignment(wrap_text=True, vertical="top")

    if cand:
        cs = wb.create_sheet("Candidates")
        cs.append(cand["fields"])
        for r in cand["rows"]:
            cs.append([r[f] for f in cand["fields"]])
        for c in cs[1]:
            c.font = Font(bold=True)
        cs.freeze_panes = "B2"
        cs.auto_filter.ref = cs.dimensions
        for i, f in enumerate(cand["fields"], 1):
            longest = max([len(f)] + [len(r[f]) for r in cand["rows"]])
            cs.column_dimensions[get_column_letter(i)].width = min(max(10, longest + 2), 60)
        for row in cs.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(vertical="top", wrap_text=len(str(c.value or "")) > 60)
        for f in cand["fields"]:
            cg.append([f"Candidates: {f}", cand["guide"][f][0], cand["guide"][f][1]])

    ab = wb.create_sheet("About")
    for line in [
        [TITLE],
        ["Version", ver],
        ["Built", datetime.date.today().isoformat()],
        ["Rows", f"{len(rows)} ClinGen curations covering {len({r['gene'] for r in rows})} genes"],
        ["Candidates sheet", f"{len(cand['rows'])} genes reported with CMT-spectrum disease but not curated by ClinGen for it. A separate list; see the README" if cand else ""],
        ["Explained and footnoted at", BLOG],
        ["Source code, history and every hand-checked source", REPO],
        ["Licence", "Data: CC BY 4.0. Credit: " + CREDIT],
        ["Not medical advice", "A registered trial is not a promising or available treatment. Talk to a clinician or genetic counsellor about any result."],
    ]:
        ab.append(line)
    ab["A1"].font = Font(bold=True, size=14)
    ab.column_dimensions["A"].width = 44
    ab.column_dimensions["B"].width = 110
    wb.save(path)


def build_datapackage(rows, fields, guide, ver, cand):
    types = {"classification_date": "date"}
    return {
        "name": "open-cmt-gene-table",
        "title": TITLE,
        "description": "Genes linked to Charcot-Marie-Tooth disease and related inherited neuropathies, one row per ClinGen gene-disease curation, with subtype names, sources and plain-language notes.",
        "version": ver,
        "created": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "homepage": PAGES,
        "licenses": [{"name": "CC-BY-4.0", "title": "Creative Commons Attribution 4.0", "path": "https://creativecommons.org/licenses/by/4.0/"}],
        "contributors": [{"title": "Dan Knauss", "role": "author", "path": "https://cmt.blog/"}],
        "sources": [
            {"title": "ClinGen Gene-Disease Validity", "path": "https://search.clinicalgenome.org/kb/gene-validity"},
            {"title": "Mondo Disease Ontology via the Monarch Initiative", "path": "https://monarchinitiative.org/"},
            {"title": "GeneReviews", "path": "https://www.ncbi.nlm.nih.gov/books/NBK1116/"},
            {"title": "Genomics England PanelApp and PanelApp Australia", "path": "https://panelapp.genomicsengland.co.uk/"},
            {"title": "ClinicalTrials.gov", "path": "https://clinicaltrials.gov/"},
        ],
        "resources": [{
            "name": "cmt-genes",
            "path": "cmt-genes.csv",
            "format": "csv",
            "mediatype": "text/csv",
            "encoding": "utf-8",
            "schema": {
                "fields": [{"name": f, "type": types.get(f, "string"), "description": f"{guide[f][1]} (Source: {guide[f][0]}.)"} for f in fields],
                "primaryKey": ["gene", "mondo_id"],
            },
        }, {
            "name": "candidate-genes",
            "path": "candidate-genes.csv",
            "format": "csv",
            "mediatype": "text/csv",
            "encoding": "utf-8",
            "description": "Genes reported to cause CMT-spectrum disease that ClinGen has not curated for it. A separate list from cmt-genes; no gene is in both.",
            "schema": {
                "fields": [{"name": f, "type": "date" if f == "date_checked" else "string", "description": f"{cand['guide'][f][1]} (Source: {cand['guide'][f][0]}.)"} for f in cand["fields"]],
                "primaryKey": ["gene"],
            },
        }, {
            "name": "candidate-genes-excluded",
            "path": "candidate-genes-excluded.csv",
            "format": "csv",
            "mediatype": "text/csv",
            "encoding": "utf-8",
            "description": "Genes screened for the candidate list and left out, with a category and reason.",
            "schema": {
                "fields": [{"name": f, "type": "date" if f == "date_checked" else "string"} for f in cand["excluded_fields"]],
                "primaryKey": ["gene"],
            },
        }],
    }


def jsonld(rows, ver):
    """schema.org Dataset, for Google Dataset Search and link previews."""
    files = [("cmt-genes.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"), ("cmt-genes.csv", "text/csv"), ("cmt-genes.json", "application/json")]
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": TITLE,
        "description": "Genes linked to Charcot-Marie-Tooth disease (CMT) and related inherited neuropathies, one row per ClinGen gene-disease curation, with the subtype names that go with each rating, inheritance, GeneReviews and PanelApp links, registered drug trials and a plain-language note. Every hand-checked value carries a source URL.",
        "url": PAGES,
        "sameAs": [BLOG, REPO],
        "identifier": "https://doi.org/10.5281/zenodo.23371750",
        "version": ver,
        "dateModified": datetime.date.today().isoformat(),
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "isAccessibleForFree": True,
        "keywords": ["Charcot-Marie-Tooth disease", "inherited neuropathy", "ClinGen", "gene-disease validity", "Mondo", "rare disease"],
        "creator": {"@type": "Person", "name": "Dan Knauss", "url": "https://cmt.blog/", "sameAs": "https://orcid.org/0000-0001-7007-5807"},
        "isBasedOn": ["https://search.clinicalgenome.org/kb/gene-validity", "https://mondo.monarchinitiative.org/"],
        "distribution": [{"@type": "DataDownload", "encodingFormat": t, "contentUrl": PAGES + n} for n, t in files],
        "variableMeasured": ["gene", "inheritance", "ClinGen classification", "subtype names", "Mondo ID"],
        "size": f"{len(rows)} rows",
    }


def candidate_body(cand):
    body = []
    for r in cand["rows"]:
        status = SCOPE[r["clingen_scope"]]
        more = [f"<p><strong>ClinGen:</strong> {html.escape(r['clingen_status'])}</p>",
                f"<p><strong>PanelApp:</strong> {html.escape(r['panelapp'])}</p>"]
        if r["omim_phenotype"]:
            more.append(f"<p><strong>OMIM:</strong> {html.escape(r['omim_phenotype'])}</p>")
        src = f'<a href="https://pubmed.ncbi.nlm.nih.gov/{html.escape(r["key_pmid"])}/">{html.escape(r["key_source"])}</a>'
        later = [p.strip() for p in r["more_pmids"].split(";") if p.strip()]
        if later:
            src += "; also " + ", ".join(f'<a href="https://pubmed.ncbi.nlm.nih.gov/{html.escape(p)}/">PMID {html.escape(p)}</a>' for p in later)
        search = " ".join([r["gene"], r["hgnc_id"], r["reported_disease"], r["omim_phenotype"], INH.get(r["inheritance"], r["inheritance"]), status])
        body.append(
            f'<tr data-search="{html.escape(search.lower())}">'
            f'<th scope="row">{html.escape(r["gene"])}</th>'
            f"<td>{html.escape(r['reported_disease'])}</td>"
            f"<td>{INH.get(r['inheritance'], html.escape(r['inheritance']))}</td>"
            f'<td><a href="https://search.clinicalgenome.org/kb/genes/{html.escape(r["hgnc_id"])}">{status}</a></td>'
            f"<td>{html.escape(r['evidence_note'])}<br><span class=\"minor\">{src}</span></td>"
            f"<td><details><summary>More<span class=\"sr\"> about {html.escape(r['gene'])}</span></summary>{''.join(more)}</details></td>"
            "</tr>"
        )
    return "\n".join(body)


def build_page(rows, fields, guide, ver, sizes, cand):
    body = []
    for r in rows:
        main = names(r["curation_subtype_names"])
        other = names(r["other_gene_names"])
        older = names(r["unverified_names"])
        cell = html.escape(", ".join(main)) if main else "—"
        extra = []
        if other:
            extra.append("Other names, not rated here: " + html.escape(", ".join(other)) + ".")
        if older:
            extra.append("Older or unverified: " + html.escape(", ".join(older)) + ".")
        if extra:
            cell += '<br><span class="minor">' + " ".join(extra) + "</span>"
        more = [f"<p>{html.escape(r['plain_note'])}</p>"] if r["plain_note"] else []
        for label, key in [("Trials", "therapy_programs"), ("Trials in other conditions", "other_condition_trials"), ("GeneReviews", "genereviews"), ("PanelApp", "panelapp")]:
            if r[key]:
                more.append(f"<p><strong>{label}:</strong> {links_html(r[key])}</p>")
        details = f"<details><summary>More<span class=\"sr\"> about {html.escape(r['gene'])}</span></summary>{''.join(more)}</details>" if more else ""
        search = " ".join([r["gene"], r["hgnc_id"], r["mondo_id"], r["clingen_disease_label"], r["historical_subtype_names"], r["unverified_names"], r["phenotype"], INH.get(r["inheritance"], r["inheritance"])])
        body.append(
            f'<tr data-search="{html.escape(search.lower())}">'
            f'<th scope="row">{html.escape(r["gene"])}</th>'
            f"<td>{cell}</td>"
            f"<td>{html.escape(r['clingen_disease_label'])}<br><span class=\"minor\">{html.escape(r['mondo_id'])}</span></td>"
            f"<td>{INH.get(r['inheritance'], html.escape(r['inheritance']))}</td>"
            f'<td data-sort="{html.escape(r["clingen_classification"])}"><a href="{html.escape(r["clingen_report"])}">{html.escape(r["clingen_classification"])}</a> ({r["classification_date"][:4]})</td>'
            f"<td>{html.escape(r['phenotype'].replace(';', ','))}</td>"
            f"<td>{details}</td>"
            "</tr>"
        )
    aliases = "{}"
    ap = os.path.join(ROOT, "site", "gene-aliases.json")
    if os.path.exists(ap):
        aliases = json.dumps(json.load(open(ap, encoding="utf-8")), separators=(",", ":"))
    genes = len({r["gene"] for r in rows})
    kb = lambda n: f"{max(1, round(sizes[n] / 1024))} KB"
    tpl = open(os.path.join(ROOT, "site", "pages", "index.html"), encoding="utf-8").read()
    columns_html = "\n".join(f"<tr><th scope=\"row\"><code>{html.escape(f)}</code></th><td>{html.escape(guide[f][0])}</td><td>{html.escape(guide[f][1])}</td></tr>" for f in fields)
    return (tpl.replace("{{VERSION}}", html.escape(ver))
               .replace("{{BUILT}}", datetime.date.today().isoformat())
               .replace("{{ROWS}}", str(len(rows)))
               .replace("{{GENES}}", str(genes))
               .replace("{{TBODY}}", "\n".join(body))
               .replace("{{CAND_TBODY}}", candidate_body(cand))
               .replace("{{CAND_GENES}}", str(len(cand["rows"])))
               .replace("{{CAND_EXCLUDED}}", str(len(cand["excluded"])))
               .replace("{{ALIASES}}", aliases)
               .replace("{{COLUMNS}}", columns_html)
               .replace("{{JSONLD}}", json.dumps(jsonld(rows, ver), ensure_ascii=False, indent=1).replace("</", "<\\/"))
               .replace("{{REPO}}", REPO)
               .replace("{{BLOG}}", BLOG)
               .replace("{{CREDIT}}", html.escape(CREDIT))
               .replace("{{SIZE_XLSX}}", kb("cmt-genes.xlsx"))
               .replace("{{SIZE_CSV}}", kb("cmt-genes.csv"))
               .replace("{{SIZE_JSON}}", kb("cmt-genes.json"))
               .replace("{{SIZE_CAND}}", kb("candidate-genes.csv")))


def main():
    ver = version()
    src = os.path.join(ROOT, "data", "cmt-genes.csv")
    with open(src, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = reader.fieldnames
        rows = list(reader)
    guide = column_guide(fields)

    cpath = os.path.join(ROOT, "data", "candidate-genes.csv")
    with open(cpath, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        cand = {"fields": reader.fieldnames, "rows": list(reader)}
    epath = os.path.join(ROOT, "data", "candidate-genes-excluded.csv")
    with open(epath, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        cand["excluded_fields"], cand["excluded"] = reader.fieldnames, list(reader)
    cand["guide"] = column_guide(cand["fields"], start="### Candidate Columns")
    both = {r["hgnc_id"] for r in rows} & {r["hgnc_id"] for r in cand["rows"]}
    both |= {r["hgnc_id"] for r in cand["rows"]} & {r["hgnc_id"] for r in cand["excluded"]}
    if both:
        sys.exit("Genes in more than one list (main, candidate, excluded): " + ", ".join(sorted(both)))

    shutil.rmtree(DIST, ignore_errors=True)
    os.makedirs(DIST)
    shutil.copyfile(src, os.path.join(DIST, "cmt-genes.csv"))
    build_xlsx(rows, fields, guide, ver, os.path.join(DIST, "cmt-genes.xlsx"), cand)
    shutil.copyfile(cpath, os.path.join(DIST, "candidate-genes.csv"))
    shutil.copyfile(epath, os.path.join(DIST, "candidate-genes-excluded.csv"))
    with open(os.path.join(DIST, "candidate-genes.json"), "w", encoding="utf-8") as fh:
        json.dump(cand["rows"], fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    with open(os.path.join(DIST, "cmt-genes.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    with open(os.path.join(DIST, "datapackage.json"), "w", encoding="utf-8") as fh:
        json.dump(build_datapackage(rows, fields, guide, ver, cand), fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    sizes = {n: os.path.getsize(os.path.join(DIST, n)) for n in ("cmt-genes.csv", "cmt-genes.xlsx", "cmt-genes.json", "candidate-genes.csv")}
    with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(build_page(rows, fields, guide, ver, sizes, cand))
    for name in os.listdir(os.path.join(ROOT, "site", "pages")):
        if name.endswith((".svg", ".png")):
            shutil.copyfile(os.path.join(ROOT, "site", "pages", name), os.path.join(DIST, name))
    open(os.path.join(DIST, ".nojekyll"), "w").close()
    print(f"{len(rows)} rows, version {ver}: " + ", ".join(sorted(os.listdir(DIST))))


if __name__ == "__main__":
    main()
