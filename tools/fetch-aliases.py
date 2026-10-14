#!/usr/bin/env python3
"""Write site/gene-aliases.json: previous official symbols from HGNC for
each gene in data/cmt-genes.csv, so the page search can find SEPTIN9 by
SEPT9, and so on. Source: https://rest.genenames.org/ (HGNC, CC0). Alias symbols are left out: many are
shared with other genes (GARS1 has the alias SMAD1, for example)."""
import csv, json, os, re, time, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
genes = sorted({r["hgnc_id"]: r["gene"] for r in csv.DictReader(open(os.path.join(ROOT, "data", "cmt-genes.csv"), encoding="utf-8"))}.items())
# Some old symbols were disease names (CMT1A for PMP22, SPG10 for KIF5A).
# The page search already matches disease names in the text, so skip them.
DISEASE = re.compile(r"^(CMT|HSN|SPG|ALS|SCAR|MYP|DYS)", re.I)
out = {}
for hid, sym in genes:
    req = urllib.request.Request(f"https://rest.genenames.org/fetch/hgnc_id/{hid}", headers={"Accept": "application/json"})
    for attempt in range(4):
        try:
            doc = json.load(urllib.request.urlopen(req, timeout=30))["response"]["docs"][0]
            break
        except OSError:
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))
    names = [n for n in doc.get("prev_symbol", []) if n.upper() != sym.upper() and not DISEASE.match(n)]
    if names:
        out[sym] = names
    time.sleep(0.2)
os.makedirs(os.path.join(ROOT, "site"), exist_ok=True)
json.dump(out, open(os.path.join(ROOT, "site", "gene-aliases.json"), "w"), indent=1, sort_keys=True)
print(f"{len(out)} genes with aliases")
