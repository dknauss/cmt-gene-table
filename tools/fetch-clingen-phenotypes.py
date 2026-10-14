#!/usr/bin/env python3
"""Record which OMIM phenotypes each ClinGen curation includes and excludes.

ClinGen's expert panels decide, for every gene-disease curation, which OMIM
(MIM) phenotypes it covers ("Included MIM Phenotypes") and which it leaves
out ("Excluded MIM Phenotypes"). merge.py uses this to attach subtype names
to the curation they belong to, instead of to the whole gene.

Reads data/clingen-cmt.csv, fetches each curation's report page (cached in
cache/clingen/), and writes data/clingen-phenotypes.csv.
"""
import csv, html, os, re, sys, time, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D, C = os.path.join(ROOT, "data"), os.path.join(ROOT, "cache", "clingen")
os.makedirs(C, exist_ok=True)
REFRESH = "--refresh" in sys.argv
MIM = re.compile(r"MIM:(\d+)\s*-\s*(.+?)(?=\s+MIM:\d+\s*-|$)")


def page(url):
    key = re.sub(r"[^A-Za-z0-9]+", "_", url.rsplit("/", 1)[-1])[:120] + ".html"
    path = os.path.join(C, key)
    if REFRESH or not os.path.exists(path):
        req = urllib.request.Request(url, headers={"User-Agent": "cmt-gene-table (https://cmt.blog/cmt-gene-table/)"})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    body = r.read()
                break
            except OSError:
                if attempt == 4:
                    raise
                time.sleep(3 * (attempt + 1))
        open(path, "wb").write(body)
        time.sleep(0.5)
    return open(path, encoding="utf-8", errors="replace").read()


def text(h):
    h = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))


def section(t, label, stop):
    m = re.search(label + r"\s*:\s*(.*?)\s*(?:" + stop + r")", t)
    if not m:
        return []
    return [(f"OMIM:{a}", b.strip()) for a, b in MIM.findall(m.group(1).strip())]


rows = list(csv.DictReader(open(os.path.join(D, "clingen-cmt.csv"), encoding="utf-8")))
out = []
for r in rows:
    t = text(page(r["clingen_report"]))
    inc = section(t, "Included MIM Phenotypes", r"Excluded MIM Phenotypes|Evaluation Date")
    exc = section(t, "Excluded MIM Phenotypes", r"Evaluation Date")
    out.append({
        "gene": r["gene"], "mondo_id": r["mondo_id"], "clingen_report": r["clingen_report"],
        "included_omim": "; ".join(i for i, _ in inc), "included_labels": "; ".join(n for _, n in inc),
        "excluded_omim": "; ".join(i for i, _ in exc), "excluded_labels": "; ".join(n for _, n in exc),
    })
with open(os.path.join(D, "clingen-phenotypes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
    w.writeheader()
    w.writerows(out)
print(f"{len(out)} curations; {sum(1 for o in out if o['included_omim'])} list included MIM phenotypes")
