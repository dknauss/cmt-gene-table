# Open CMT Gene Table

An open, downloadable table of the genes linked to Charcot-Marie-Tooth disease (CMT) and related inherited neuropathies. For each gene it gives:
- the ClinGen evidence rating;
- the disease and its MONDO ID;
- the conventional subtype names (CMT1A, CMT2N, CMTX1, HSAN1D…);
- the matching OMIM phenotype IDs.

It is maintained by Dan Knauss for [cmt.blog](https://cmt.blog).

**This is not medical advice and not a diagnostic tool.** It summarizes public curation data so that patients, families and writers can find their way around the gene names. Genetic results should be interpreted by a clinician or genetic counsellor. Follow the source links for the authoritative curation.

## The Data

[`data/cmt-genes.csv`](data/cmt-genes.csv) is the table. It has one row per ClinGen curation: 72 rows covering 70 genes. NEFL and PMP22 each have two curations.

| Column | Source | Notes |
|---|---|---|
| `gene`, `hgnc_id` | ClinGen | HGNC symbol and ID |
| `clingen_disease_label`, `mondo_id` | ClinGen | The disease the gene was curated for |
| `inheritance` | ClinGen | AD, AR, XL or SD (semidominant) |
| `clingen_classification`, `classification_date` | ClinGen | Definitive, Strong, Moderate, Limited, Disputed… |
| `clingen_report` | ClinGen | Link to the full curation |
| `type_named_in_label` | Derived | The CMT type named in ClinGen's own label, if any |
| `historical_subtype_names` | MONDO via Monarch | Conventional subtype names, separated by `; ` |
| `subtype_mondo_ids` | MONDO via Monarch | The MONDO terms those names come from |
| `omim_phenotype_ids` | MONDO cross-references | IDs only; no OMIM text is reproduced |
| `subtype_review_note` | Build notes | Provenance and anything flagged for human review |
| `phenotype`, `genereviews`, `panelapp`, `therapy_programs`, `plain_note` | — | Blank for now; to be filled by hand from cited sources |

Supporting files:
- `data/clingen-cmt.csv` holds the ClinGen rows as downloaded.
- `data/subtype-names.csv` holds the subtype-name lookup, with source URLs for every gene.

### How Subtype Names Are Derived

Names are converted mechanically from MONDO disease labels and exact synonyms. For example:
- "Charcot-Marie-Tooth disease axonal type 2N" becomes CMT2N.
- "neuropathy, hereditary sensory, type 1D" becomes HSN1D.
- "…X-linked dominant 1" becomes CMTX1.

Nothing is filled in from memory. Where MONDO has no lettered subtype name for a gene, the field is left blank. Eight genes are blank: ARHGEF10, GAN, KIF5A, MCM3AP, SCO2, SEPTIN9, SETX and SYT2.

Some names need human review before they are relied on. They are flagged in `subtype_review_note`:
- **MFN2:** MONDO writes CMT2A2; it is conventionally written CMT2A2A.
- **SORD:** the only MONDO name is a distal motor neuropathy symbol, HMNR8.
- **SCN11A:** HSAN2D comes only from a correlated association, which is probably spurious.
- **HINT1, FBLN5 and MED25:** each has an unusual or single-source name.

## Scope and Gaps

The table follows ClinGen's Charcot-Marie-Tooth Disease Gene Curation Expert Panel, so it also includes:
- hereditary sensory and autonomic neuropathies;
- distal hereditary motor neuropathies;
- a few genes outside CMT proper, such as SYT2 and SEPTIN9.

It leaves out genes the panel has not curated yet. NDRG1, LMNA, PRPS1, DHTKD1 and AIFM1 are among those reported with CMT that are not in this file. Do not read their absence as a finding.

## Rebuilding

The tools need only Python 3 and its standard library:

```bash
python3 tools/build-clingen.py    # download ClinGen's file, keep the CMT panel's rows
python3 tools/fetch-monarch.py    # cache Monarch/MONDO lookups in cache/
python3 tools/build-subtypes.py   # derive subtype names
python3 tools/merge.py            # write data/cmt-genes.csv
```

A monthly GitHub Actions job runs these steps and opens a pull request when ClinGen or MONDO data change. Changes are reviewed by hand before merging.

## Sources and Licences

- **ClinGen** gene-disease validity curations: public domain (CC0). Data from [search.clinicalgenome.org](https://search.clinicalgenome.org/kb/gene-validity).
- **MONDO** disease ontology, CC BY 4.0, retrieved through the [Monarch Initiative API](https://api-v3.monarchinitiative.org/) (CC BY 4.0). Cite: Vasilevsky NA et al., "Mondo: Unifying diseases for the world, by the world," *medRxiv* (2022), [doi:10.1101/2022.04.13.22273750](https://doi.org/10.1101/2022.04.13.22273750).
- **OMIM**: identifiers only. OMIM's terms do not allow its content to be redistributed.
- **GeneReviews** and **PanelApp**, when added, are linked only. Their text is not copied.

The data in `data/` is released under [CC BY 4.0](LICENSE-DATA). Credit "Open CMT Gene Table (cmt.blog), using ClinGen (CC0) and MONDO (CC BY 4.0)". The scripts in `tools/` are under the [MIT License](LICENSE).

## Corrections

Open an issue or [contact cmt.blog](https://cmt.blog/contact/). Corrections are logged with dates in [CHANGELOG.md](CHANGELOG.md).
