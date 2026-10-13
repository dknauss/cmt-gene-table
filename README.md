# Open CMT Gene Table

An open, downloadable table of the genes linked to Charcot-Marie-Tooth disease (CMT) and related inherited neuropathies. For each gene it gives:
- the ClinGen evidence rating;
- the disease and its MONDO ID;
- the conventional subtype names (CMT1A, CMT2N, CMTX1, HSAN1D…);
- the matching OMIM phenotype IDs;
- links to the GeneReviews chapter(s) and PanelApp gene pages, with PanelApp ratings;
- the neuropathy type, registered clinical trials, and a one-sentence plain-language note, each traced to a cited source.

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
| `genereviews` | NCBI GeneReviews report files | Chapter title and link for every GeneReviews chapter NCBI maps to the gene, separated by `; `. Starts `[overview only]` when every chapter is an overview |
| `panelapp` | PanelApp APIs | Rating (Green/Amber/Red), panel, version and gene-page link on Genomics England panel 846 and PanelApp Australia panel 3070 |
| `phenotype` | Hand-checked | One or more of axonal, demyelinating, intermediate, motor-predominant, sensory-predominant |
| `therapy_programs` | Hand-checked | Registered trials of drugs, biologics or gene therapies for the gene's neuropathy, with phase, status and link |
| `plain_note` | Hand-checked | One sentence in plain language, written for this table |

Supporting files:
- `data/clingen-cmt.csv` holds the ClinGen rows as downloaded.
- `data/subtype-names.csv` holds the subtype-name lookup, with source URLs for every gene.
- `data/links.csv` holds the GeneReviews and PanelApp links, built by `tools/fetch-links.py`.
- `data/hand-checked-sources.csv` holds every hand-checked value with its source URL, access date and a note. A value with two sources has two rows. `merge.py` refuses a row without a source URL.

### GeneReviews and PanelApp Links

These are built by script, so they can be regenerated.
- **GeneReviews:** NCBI's weekly gene-to-chapter files (`NBKid_shortname_genesymbol.txt` and `GRtitle_shortname_NBKid.txt` from [ftp.ncbi.nlm.nih.gov/pub/GeneReviews](https://ftp.ncbi.nlm.nih.gov/pub/GeneReviews/)). Gene-specific chapters are listed first. Some genes are mapped to chapters about other conditions (for example SETX to ataxia chapters); those are kept because NCBI maps them. 50 genes have at least one chapter; 30 of those have overviews only; 20 have none.
- **PanelApp:** [Genomics England panel 846](https://panelapp.genomicsengland.co.uk/panels/846/), "Hereditary neuropathy or pain disorder" (the signed-off NHS Genomic Medicine Service panel for test R78), and [PanelApp Australia panel 3070](https://panelapp-aus.org/panels/3070/), "Hereditary Neuropathy". The panel version at the time of the build is recorded in each value. Genomics England's legacy 100,000 Genomes panel 85 is not used. All 70 genes are on both panels. Genomics England links use its own gene symbols, which are older for some genes (AARS, GARS, MARS, WARS, YARS, SEPT9); matching is done by HGNC ID.

### Hand-Checked Columns

**Phenotype** values are taken, in this order of preference, from:
1. a gene-specific GeneReviews chapter that states the neuropathy type;
2. the GeneReviews [CMT overview](https://www.ncbi.nlm.nih.gov/books/NBK1358/), Table 4 (Ax/De/In marks), Table 3 (HSN/HSAN genes, recorded as sensory-predominant) and Table 4's comments and other designations (motor neuropathy, dHMN or DSMA, recorded as motor-predominant);
3. ClinGen's curated disease label when it names the type (for example "distal hereditary motor neuropathy");
4. a cited PubMed paper (GAN, MED25, PRX, SBF1, SLC25A46).

Nothing is inferred from subtype names. SEPTIN9 (neuralgic amyotrophy) is left blank because its condition fits none of the categories.

Two values need review, because GeneReviews' overview table disagrees with another source:
- **SH3TC2:** the overview's Table 4 marks it axonal, but the GeneReviews SH3TC2 chapter calls it demyelinating. The chapter is used.
- **PRX:** the overview marks it axonal. The cited review (Dubourg et al 2006) lists it among demyelinating recessive CMT genes, and that is used.

**Therapy programs** come from the [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api). Every gene was searched by symbol, and CMT, HMSN, HSAN, HSN, dHMN, HNPP, familial dysautonomia, giant axonal neuropathy, SORD, SMARD and related conditions were searched as well. A trial is listed when:
- it tests a drug, biologic or gene therapy;
- it enrols by gene, or by a subtype tied to one gene (CMT1A for PMP22, for example).

Rehabilitation, device, biomarker and natural-history studies are left out. So are trials that enrol by broad CMT type, such as ACE-083 (CMT1 and CMTX) and NMD670 (CMT1 and CMT2). Status is as of the access date. "none found as of 2026-10-13" means the searches found nothing; it does not mean no research exists. Company and foundation pipeline pages have not been reviewed yet, so preclinical programs are not listed.

**Plain notes** are written for this table from the sources cited for them, usually the ClinGen report plus GeneReviews. No source text is copied, and the notes do not give clinical advice.

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
python3 tools/fetch-links.py      # GeneReviews and PanelApp links (add --refresh to bypass cache/)
python3 tools/merge.py            # write data/cmt-genes.csv, adding data/hand-checked-sources.csv
```

A monthly GitHub Actions job runs these steps and opens a pull request when ClinGen, MONDO, GeneReviews or PanelApp data change. Hand-checked values are not refreshed automatically. Re-check trial statuses by hand. Changes are reviewed by hand before merging.

## Sources and Licences

- **ClinGen** gene-disease validity curations: public domain (CC0). Data from [search.clinicalgenome.org](https://search.clinicalgenome.org/kb/gene-validity).
- **MONDO** disease ontology, CC BY 4.0, retrieved through the [Monarch Initiative API](https://api-v3.monarchinitiative.org/) (CC BY 4.0). Cite: Vasilevsky NA et al., "Mondo: Unifying diseases for the world, by the world," *medRxiv* (2022), [doi:10.1101/2022.04.13.22273750](https://doi.org/10.1101/2022.04.13.22273750).
- **OMIM**: identifiers only. OMIM's terms do not allow its content to be redistributed.
- **GeneReviews®**: © 1993–2026 University of Washington, Seattle. GeneReviews permits noncommercial research reproduction only, with credit and a link. This table links to chapters and records their titles. It does not copy chapter text. Neuropathy types and other facts drawn from GeneReviews are cited per row in `data/hand-checked-sources.csv`. See the [GeneReviews Copyright Notice and Usage Disclaimer](https://www.ncbi.nlm.nih.gov/books/n/gene/GRcopyright_permiss/).
- **PanelApp** ([Genomics England](https://panelapp.genomicsengland.co.uk/) and [PanelApp Australia](https://panelapp-aus.org/)): the table records a link, the panel version and each gene's public traffic-light rating. It does not copy evidence text or reviews. Check each site's terms before reuse. Genomics England's terms restrict commercial and diagnostic use, and this table must not be used for diagnosis.
- **ClinicalTrials.gov**: US National Library of Medicine; public data.
- **PubMed** abstracts are cited by link only.

The data in `data/` is released under [CC BY 4.0](LICENSE-DATA). Credit "Open CMT Gene Table (cmt.blog), using ClinGen (CC0) and MONDO (CC BY 4.0)". The scripts in `tools/` are under the [MIT License](LICENSE).

## Corrections

Open an issue or [contact cmt.blog](https://cmt.blog/contact/). Corrections are logged with dates in [CHANGELOG.md](CHANGELOG.md).
