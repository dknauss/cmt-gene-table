#!/usr/bin/env python3
"""Fill the clingen_curations column of data/candidate-genes-excluded.csv.

For each excluded gene, lists every ClinGen gene-disease validity curation
(any panel), matched by HGNC ID, as
"disease (classification, inheritance, panel, date)", separated by "; ".
A gene with none gets "not curated". Every other column is left as it is.

ClinGen's download is read from cache/clingen-gene-validity.csv, or fetched
when that file is missing (add --refresh to fetch it again). Pass --check to
report rows that would change without writing the file.

Usage: python3 tools/fill-excluded-curations.py [--refresh] [--check]
"""
import csv
import os
import sys
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SOURCE = "https://search.clinicalgenome.org/kb/gene-validity/download"
CACHE = os.path.join(ROOT, "cache", "clingen-gene-validity.csv")
EXCLUDED = os.path.join(ROOT, "data", "candidate-genes-excluded.csv")
SEP = "; "


def load_clingen(refresh=False):
    if refresh or not os.path.exists(CACHE):
        req = urllib.request.Request(SOURCE, headers={"User-Agent": "cmt.blog gene table builder"})
        text = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        open(CACHE, "w", encoding="utf-8").write(text)
    rows = list(csv.reader(open(CACHE, encoding="utf-8")))
    header_i = next(i for i, r in enumerate(rows) if r and r[0] == "GENE SYMBOL")
    head = rows[header_i]
    idx = {name: head.index(name) for name in head}
    by_hgnc = {}
    for r in rows[header_i + 1:]:
        if len(r) != len(head) or not r[idx["GENE ID (HGNC)"]].startswith("HGNC:"):
            continue
        by_hgnc.setdefault(r[idx["GENE ID (HGNC)"]], []).append({
            "disease": r[idx["DISEASE LABEL"]],
            "classification": r[idx["CLASSIFICATION"]],
            "moi": r[idx["MOI"]],
            "panel": panel_name(r[idx["GCEP"]]),
            "date": r[idx["CLASSIFICATION DATE"]][:10],
        })
    return by_hgnc


def panel_name(gcep):
    """'Mitochondrial Diseases Gene Curation Expert Panel' -> 'Mitochondrial Diseases panel'."""
    for suffix in (" Gene Curation Expert Panel", " Expert Panel", " GCEP"):
        if gcep.endswith(suffix):
            return gcep[: -len(suffix)] + " panel"
    return gcep


def curations_text(curations):
    """Join a list of curation dicts. Takes a list, never a string."""
    if isinstance(curations, str):
        raise TypeError("curations must be a list of curation records, not a string")
    if not curations:
        return "not curated"
    items = sorted(curations, key=lambda c: (c["disease"], c["date"]))
    return SEP.join(
        f'{c["disease"]} ({c["classification"]}, {c["moi"]}, {c["panel"]}, {c["date"]})' for c in items
    )


def main():
    refresh = "--refresh" in sys.argv
    check = "--check" in sys.argv
    by_hgnc = load_clingen(refresh)
    with open(EXCLUDED, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = reader.fieldnames
        rows = list(reader)
    changed = []
    for row in rows:
        new = curations_text(by_hgnc.get(row["hgnc_id"], []))
        if new != row["clingen_curations"]:
            changed.append((row["gene"], row["clingen_curations"], new))
            row["clingen_curations"] = new
    if check:
        for gene, old, new in changed:
            print(f"{gene}\n  old: {old}\n  new: {new}")
        print(f"{len(changed)} of {len(rows)} rows would change")
        return
    with open(EXCLUDED, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(changed)} of {len(rows)} rows updated in data/candidate-genes-excluded.csv")


if __name__ == "__main__":
    main()
