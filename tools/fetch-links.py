#!/usr/bin/env python3
"""Build the GeneReviews and PanelApp link columns: data/links.csv.

GeneReviews: NCBI's weekly gene-to-chapter report files
(https://ftp.ncbi.nlm.nih.gov/pub/GeneReviews/). Every chapter the files map
to a gene is listed, gene-specific chapters first. When a gene's only chapters
are overviews (title contains "Overview"), the value starts "[overview only]".
Only chapter titles and links are recorded; no GeneReviews text is copied.

PanelApp: the public APIs of Genomics England PanelApp and PanelApp Australia.
For each gene we record its rating (Green/Amber/Red) on one panel from each
instance, the panel id and version, and a link to the gene's page there. No
PanelApp evidence text is copied.

Downloads are cached in cache/links/. Pass --refresh to fetch them again.
Uses only the Python 3 standard library.
"""
import csv
import json
import os
import sys
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CACHE = os.path.join(ROOT, "cache", "links")
DATA = os.path.join(ROOT, "data")
UA = {"User-Agent": "Open CMT Gene Table (https://github.com/dknauss/cmt-gene-table)",
      "Accept": "application/json, text/plain"}

GR_FTP = "https://ftp.ncbi.nlm.nih.gov/pub/GeneReviews/"
GR_GENES = "NBKid_shortname_genesymbol.txt"
GR_TITLES = "GRtitle_shortname_NBKid.txt"
GR_BOOK = "https://www.ncbi.nlm.nih.gov/books/{}/"

# (label, API base, site base, panel id). Genomics England panel 846 is the
# signed-off NHS Genomic Medicine Service panel for test R78; PanelApp
# Australia panel 3070 is its "Hereditary Neuropathy" panel.
PANELS = [
    ("Genomics England PanelApp", "https://panelapp.genomicsengland.co.uk/api/v1/",
     "https://panelapp.genomicsengland.co.uk/", 846),
    ("PanelApp Australia", "https://panelapp-aus.org/api/v1/",
     "https://panelapp-aus.org/", 3070),
]
RATING = {"3": "Green", "2": "Amber", "1": "Red", "0": "Red"}
REFRESH = "--refresh" in sys.argv


def fetch(url, name):
    path = os.path.join(CACHE, name)
    if REFRESH or not os.path.exists(path):
        os.makedirs(CACHE, exist_ok=True)
        req = urllib.request.Request(url, headers=UA)
        body = urllib.request.urlopen(req, timeout=120).read()
        with open(path, "wb") as f:
            f.write(body)
    raw = open(path, "rb").read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:  # NCBI's title file is Latin-1
        return raw.decode("latin-1")


def genereviews():
    titles = {}
    for line in fetch(GR_FTP + GR_TITLES, GR_TITLES).splitlines():
        if line.startswith("#") or not line.strip():
            continue
        p = line.split("\t")
        titles[p[2].strip()] = " ".join(p[1].split())
    chapters = {}
    for line in fetch(GR_FTP + GR_GENES, GR_GENES).splitlines():
        if line.startswith("#") or not line.strip():
            continue
        nbk, _short, sym = (x.strip() for x in line.split("\t"))
        if nbk and sym and nbk not in chapters.setdefault(sym, []):
            chapters[sym].append(nbk)
    out = {}
    for sym, nbks in chapters.items():
        items = [(titles.get(n, n), n) for n in nbks]
        items.sort(key=lambda t: ("overview" in t[0].lower(), t[0]))
        text = "; ".join(f"{t}: {GR_BOOK.format(n)}" for t, n in items)
        if all("overview" in t.lower() for t, _ in items):
            text = "[overview only] " + text
        out[sym] = text
    return out


def panelapp():
    out = {}
    for label, api, site, pid in PANELS:
        d = json.loads(fetch(f"{api}panels/{pid}/", f"panelapp_{pid}.json"))
        name, ver = d["name"], d["version"]
        for g in d["genes"]:
            gd = g["gene_data"]
            rating = RATING.get(str(g.get("confidence_level")), "Unrated")
            text = (f"{rating} — {name} ({label} panel {pid}, v{ver}): "
                    f"{site}panels/{pid}/gene/{gd['gene_symbol']}/")
            for key in (gd.get("hgnc_id"), gd["gene_symbol"]):
                if key:
                    out.setdefault(key, []).append(text)
        out.setdefault("_panels", []).append(f"{label} panel {pid} '{name}' v{ver}")
    return out


def main():
    rows = list(csv.DictReader(open(os.path.join(DATA, "clingen-cmt.csv"), encoding="utf-8")))
    gr = genereviews()
    pa = panelapp()
    seen = set()
    n_gr = n_pa = 0
    with open(os.path.join(DATA, "links.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["gene", "hgnc_id", "genereviews", "panelapp"], lineterminator="\n")
        w.writeheader()
        for r in rows:
            if r["gene"] in seen:
                continue
            seen.add(r["gene"])
            g = gr.get(r["gene"], "")
            p = pa.get(r["hgnc_id"]) or pa.get(r["gene"]) or []
            # Note panels the gene is absent from, so "not listed" is explicit.
            parts = []
            for label, _api, _site, pid in PANELS:
                hit = [t for t in p if f"panel {pid}," in t]
                parts += hit or [f"Not listed — {label} panel {pid}"]
            n_gr += bool(g)
            n_pa += bool(p)
            w.writerow({"gene": r["gene"], "hgnc_id": r["hgnc_id"],
                        "genereviews": g, "panelapp": "; ".join(parts)})
    print(f"{len(seen)} genes: {n_gr} with GeneReviews chapters, {n_pa} on a PanelApp panel")
    print("Panels: " + "; ".join(pa["_panels"]))


if __name__ == "__main__":
    main()
