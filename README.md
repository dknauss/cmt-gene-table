# Open CMT Gene Table

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23371750.svg)](https://doi.org/10.5281/zenodo.23371750)

An open, downloadable table of the genes linked to Charcot-Marie-Tooth disease (CMT) and related inherited neuropathies. For each ClinGen gene-disease curation it gives:
- the ClinGen evidence rating;
- the disease and its Mondo ID;
- the conventional subtype names (CMT1A, CMT2N, CMTX1, HSAN1D…) that belong to that curation, kept apart from other names linked to the same gene;
- the matching OMIM phenotype IDs;
- links to the GeneReviews chapter(s) and PanelApp gene pages, with PanelApp ratings;
- the neuropathy type, clinical trials found in ClinicalTrials.gov for that disease, and a one-sentence plain-language note, each traced to a cited source.

It is maintained by Dan Knauss ([ORCID 0000-0001-7007-5807](https://orcid.org/0000-0001-7007-5807)) for [cmt.blog](https://cmt.blog). Releases are archived at [Zenodo](https://doi.org/10.5281/zenodo.23371750) and indexed by [OpenAIRE](https://explore.openaire.eu/search/dataset?datasetId=od______2659::1fd2a6686eb918f6fdca0646d8ee3f49).

**This is not medical advice and not a diagnostic tool.** It summarizes public curation data so that patients, families and writers can find their way around the gene names. Genetic results should be interpreted by a clinician or genetic counsellor. Follow the source links for the authoritative curation.

## Downloads

Browse, search and download the table at **[dknauss.github.io/cmt-gene-table](https://dknauss.github.io/cmt-gene-table/)**.

| Format | Latest version | Notes |
|---|---|---|
| Excel | [cmt-genes.xlsx](https://github.com/dknauss/cmt-gene-table/releases/latest/download/cmt-genes.xlsx) | The table, a Columns sheet explaining every column, and an About sheet |
| CSV | [cmt-genes.csv](https://github.com/dknauss/cmt-gene-table/releases/latest/download/cmt-genes.csv) | UTF-8, one row per ClinGen curation |
| JSON | [cmt-genes.json](https://github.com/dknauss/cmt-gene-table/releases/latest/download/cmt-genes.json) | One object per row, same fields as the CSV |
| Data Package | [datapackage.json](https://github.com/dknauss/cmt-gene-table/releases/latest/download/datapackage.json) | [Frictionless](https://frictionlessdata.io/) description of every column, for loading with types in R or Python |
| Additional genes | [candidate-genes.csv](https://github.com/dknauss/cmt-gene-table/releases/latest/download/candidate-genes.csv) | The separate list of genes reported with CMT-spectrum disease that are not in the main table; also on the Excel file's Candidates sheet and as `candidate-genes.json` on the site. See "Additional Neuropathy Genes Outside the Main Table" below |

Each monthly update is a [release](https://github.com/dknauss/cmt-gene-table/releases) tagged by year and month (`v2026.10`), with these files attached. The links above always point to the latest release; link to a tagged release when you need a fixed version. To cite the table, use GitHub's "Cite this repository" button (from `CITATION.cff`). Every release is archived at Zenodo: [10.5281/zenodo.23371750](https://doi.org/10.5281/zenodo.23371750) always resolves to the latest version, and each version has its own DOI (v2026.10 is [10.5281/zenodo.23371751](https://doi.org/10.5281/zenodo.23371751)).

You can also [open the CSV in Datasette Lite](https://lite.datasette.io/?csv=https://dknauss.github.io/cmt-gene-table/cmt-genes.csv) to filter and query it in your browser.

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
| `curation_subtype_names` | ClinGen + Mondo | Subtype names for the disease rated in this row, separated by `; `. See "Names Matched to Curations" below |
| `curation_names_basis` | Build notes | How those names were matched to the curation |
| `other_gene_names` | Mondo via Monarch | Other subtype names with a causal link to the gene that this curation does not cover. The rating in this row does not apply to them |
| `unverified_names` | Mondo via Monarch | Names that come only from Monarch correlated (not causal) associations. Kept for review, not presented as subtypes |
| `rejected_names` | Hand-checked | Names checked and found not to belong to the gene, from `data/name-reviews.csv` (each with a source URL). Left off the page |
| `clingen_included_omim`, `clingen_excluded_omim` | ClinGen curation page | The OMIM phenotypes ClinGen's panel included in, or excluded from, this curation |
| `historical_subtype_names` | Mondo via Monarch | Every subtype name linked to the gene, causal or correlated, separated by `; `. Gene-wide, so it is the same for every curation of a gene; use `curation_subtype_names` for the names that go with a rating |
| `subtype_mondo_ids` | Mondo via Monarch | The Mondo terms those names come from |
| `omim_phenotype_ids` | Mondo cross-references | IDs only; no OMIM text is reproduced |
| `subtype_review_note` | Build notes | Provenance and anything flagged for human review |
| `genereviews` | NCBI GeneReviews report files | Chapter title and link for every GeneReviews chapter NCBI maps to the gene, separated by `; `. Starts `[overview only]` when every chapter is an overview |
| `panelapp` | PanelApp APIs | Rating (Green/Amber/Red), panel, version and gene-page link on Genomics England panel 846 and PanelApp Australia panel 3070 |
| `phenotype` | Hand-checked | One or more of axonal, demyelinating, intermediate, motor-predominant, sensory-predominant |
| `therapy_programs` | Hand-checked | Trials of drugs, biologics or gene therapies for the disease in this row, found by the ClinicalTrials.gov searches in the source URL, with phase, status and link. "None found" means none found by that search, not that no research exists. A registered trial is not a promising or available treatment |
| `other_condition_trials` | Hand-checked | Trials that target the gene but in a different condition, such as LTX-002 for SPTLC1 in ALS |
| `plain_note` | Hand-checked | One sentence in plain language, written for this table |

Supporting files:
- `data/clingen-cmt.csv` holds the ClinGen rows as downloaded.
- `data/subtype-names.csv` holds the gene-wide subtype-name lookup, with source URLs for every gene.
- `data/subtype-terms.csv` has one row per Mondo term behind those names: its short names, OMIM IDs and whether Monarch links it to the gene causally or only by correlation.
- `data/clingen-phenotypes.csv` records the OMIM phenotypes each ClinGen curation includes and excludes, read from the curation pages by `tools/fetch-clingen-phenotypes.py`.
- `site/table-body.html`, `site/candidate-table-body.html`, and `site/gene-aliases.json` are built for the tables on cmt.blog by `tools/build-page-table.py` and `tools/fetch-aliases.py` (previous official HGNC symbols, so the page search finds SEPTIN9 by SEPT9).
- `site/pages/index.html` is the template for the GitHub Pages site. `tools/build-exports.py` fills it and writes the downloads to `dist/` (not committed); the column descriptions in the downloads and on the site come from the column table above.
- `data/links.csv` holds the GeneReviews and PanelApp links, built by `tools/fetch-links.py`.
- `data/candidate-genes.csv` and `data/candidate-genes-excluded.csv` hold the separate list of additional genes and the screened genes left out of it. See "Additional Neuropathy Genes Outside the Main Table" below.
- `data/hand-checked-sources.csv` holds every hand-checked value with its source URL, access date and a note. A value with two sources has two rows. A row with a `mondo_id` applies only to that curation; a blank `mondo_id` applies to every curation of the gene. `merge.py` refuses a row without a source URL.

### Names Matched to Curations

A gene can have more than one ClinGen curation, and a gene's historical names don't all belong to the disease ClinGen rated. PMP22 is the clearest case: ClinGen rates it separately for CMT1A (caused by a duplication) and for HNPP (usually a deletion or a variant that stops the gene working), and it excludes CMT1E and Dejerine-Sottas disease from both. So names are attached per curation:

1. If ClinGen lists the OMIM phenotypes it included, a name is attached when its Mondo term has one of those OMIM IDs.
2. Otherwise, the names of the curation's own Mondo term are used.
3. If neither works, the gene's causal names are used, and `curation_names_basis` says so.

Names from Monarch correlated associations only are never attached to a curation; they go in `unverified_names`. Some are wrong for the gene (HSAN2D belongs to SCN9A, not SCN11A). Others are historical names with some support in the literature (CMT5 for MFN2, HSAN5 for NTRK1). They need a person to check them before they are promoted. On the cmt.blog page they appear in italics as "older or unverified", apart from the main names. Names checked and found wrong for the gene are recorded in `data/name-reviews.csv` and left off the page.

### GeneReviews and PanelApp Links

These are built by script, so they can be regenerated.
- **GeneReviews:** NCBI's weekly gene-to-chapter files (`NBKid_shortname_genesymbol.txt` and `GRtitle_shortname_NBKid.txt` from [ftp.ncbi.nlm.nih.gov/pub/GeneReviews](https://ftp.ncbi.nlm.nih.gov/pub/GeneReviews/)). Gene-specific chapters are listed first. Some genes are mapped to chapters about other conditions (for example SETX to ataxia chapters); those are kept because NCBI maps them. 50 genes have at least one chapter; 30 of those have overviews only; 20 have none.
- **PanelApp:** [Genomics England panel 846](https://panelapp.genomicsengland.co.uk/panels/846/), "Hereditary neuropathy or pain disorder" (the NHS Genomic Medicine Service panel for test R78), and [PanelApp Australia panel 3070](https://panelapp-aus.org/panels/3070/), "Hereditary Neuropathy". The panel version at the time of the build is recorded in each value. This is the latest version, not necessarily the signed-off one: on October 13, 2026 the build used v8.38, and the latest signed-off version was v8.30 (August 12, 2026). PanelApp's own terms of use govern reuse of its data. Genomics England's legacy 100,000 Genomes panel 85 is not used for the main table; the screen for the additional list uses it alongside the other two. All 70 genes are on both panels. Genomics England links use its own gene symbols, which are older for some genes (AARS, GARS, MARS, WARS, YARS, SEPT9); matching is done by HGNC ID.

### Hand-Checked Columns

**Phenotype** values are taken, in this order of preference, from:
1. a gene-specific GeneReviews chapter that states the neuropathy type;
2. the GeneReviews [CMT overview](https://www.ncbi.nlm.nih.gov/books/NBK1358/), Table 4 (Ax/De/In marks), Table 3 (HSN/HSAN genes, recorded as sensory-predominant) and Table 4's comments and other designations (motor neuropathy, dHMN or DSMA, recorded as motor-predominant);
3. ClinGen's curated disease label when it names the type (for example "distal hereditary motor neuropathy");
4. a cited PubMed paper (GAN, MED25, PRX, SBF1, SLC25A46).

Nothing is inferred from subtype names. SEPTIN9 (neuralgic amyotrophy) is left blank because its condition fits none of the categories.

Where sources disagree, the value used and the disagreement are both recorded in `data/hand-checked-sources.csv` (the `note` column). The current cases:
- **SH3TC2:** GeneReviews' overview table (Table 4) marks it axonal, but the GeneReviews SH3TC2 chapter calls it demyelinating. The chapter is used.
- **PRX:** the overview marks it axonal. The cited review (Dubourg et al 2006) lists it among demyelinating recessive CMT genes, and that is used.
- **GJB1:** the overview marks it axonal, demyelinating and intermediate. The GeneReviews GJB1 chapter classes it as intermediate, and that is used.
- **MED25:** listed as axonal from Montecchiani et al 2016, but ClinGen rates the gene's link to CMT as Disputed.

**Therapy programs** come from the [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api). Every gene was searched by symbol, and CMT, HMSN, HSAN, HSN, dHMN, HNPP, familial dysautonomia, giant axonal neuropathy, SORD, SMARD and related conditions were searched as well. A trial is listed when:
- it tests a drug, biologic or gene therapy;
- it enrols by gene, or by a subtype tied to one gene (CMT1A for PMP22, for example).

Rehabilitation, device, biomarker and natural-history studies are left out. So are trials that enrol by broad CMT type, such as ACE-083 (CMT1 and CMTX) and NMD670 (CMT1 and CMT2). Status is as of the access date. "none found as of 2026-10-13" means the searches found nothing; it does not mean no research exists. Company and foundation pipeline pages have not been reviewed yet, so preclinical programs are not listed.

**Plain notes** are written for this table from the sources cited for them, usually the ClinGen report plus GeneReviews. No source text is copied, and the notes do not give clinical advice.

### How Subtype Names Are Derived

Names are converted mechanically from Mondo disease labels and exact synonyms. For example:
- "Charcot-Marie-Tooth disease axonal type 2N" becomes CMT2N.
- "neuropathy, hereditary sensory, type 1D" becomes HSN1D.
- "…X-linked dominant 1" becomes CMTX1.

Nothing is filled in from memory. Where Mondo has no lettered subtype name for a gene, the field is left blank. Eight genes are blank: ARHGEF10, GAN, KIF5A, MCM3AP, SCO2, SEPTIN9, SETX and SYT2.

Some names need human review before they are relied on. They are flagged in `subtype_review_note`:
- **MFN2:** Mondo writes CMT2A2; it is conventionally written CMT2A2A.
- **SORD:** the only Mondo name is a distal motor neuropathy symbol, HMNR8.
- **SCN11A:** HSAN2D comes only from a correlated association, which is probably spurious.
- **HINT1, FBLN5 and MED25:** each has an unusual or single-source name.

## Scope and Gaps

The table follows ClinGen's Charcot-Marie-Tooth Disease Gene Curation Expert Panel, so it also includes:
- hereditary sensory and autonomic neuropathies;
- distal hereditary motor neuropathies;
- a few genes outside CMT proper, such as SYT2 and SEPTIN9.

It leaves out genes the panel has not curated yet. Many of them, such as NDRG1, LMNA, and DHTKD1, are in the separate list of additional genes below. Do not read a gene's absence from the main table as a finding.

## Additional Neuropathy Genes Outside the Main Table

<a id="candidate-genes-not-yet-curated"></a>

[`data/candidate-genes.csv`](data/candidate-genes.csv) is a second, separate list: 59 genes reported with CMT or a related inherited neuropathy that are absent from the main table, which is drawn from ClinGen's CMT expert panel. The main table is unchanged, and the two lists never share a gene.

Evidence for these genes ranges from established disease associations to preliminary reports. Some have relevant ClinGen curations from other expert panels, including broader disorders that encompass the neuropathy; `clingen_scope` and `clingen_status` identify them. Absence from the main table is not an evidence rating. The evidence notes describe the listed publications, not the complete evidence for each gene. The screen used three specified PanelApp panels, with AKAP6 added separately, so this is not a complete list of inherited-neuropathy genes.

The ClinGen status concerns gene-disease validity only. Other ClinGen frameworks, such as dosage sensitivity, are mentioned where relevant (SPTAN1), but they are not validity ratings. The file and some column names still say "candidate," from the list's first version.

### The Rule

A gene is a candidate when both are true:
1. **Its reported disease is CMT-spectrum.** That means CMT (axonal, demyelinating, or intermediate), HMSN (including the Russe, Lom, Okinawa, and type 6 forms), distal hereditary motor neuropathy (dHMN), HSN or HSAN, congenital hypomyelinating neuropathy, giant axonal neuropathy, or a neuropathy reported on its own. The name comes from OMIM's numbered types, Mondo, PanelApp, or the key paper. When a named type comes with other features (HSN1E with dementia and hearing loss, HSAN9 with developmental delay), it still counts. A syndrome named for something else (an ataxia, a spastic paraplegia, a leukodystrophy, a metabolic disease) does not, even when neuropathy is one of its features. Neither does a motor neuron disease named as spinal muscular atrophy or ALS.
2. **It is not in the main table.** ClinGen curations by other panels do not keep a gene out. They are checked for every listed gene, by every panel, and shown in `clingen_status` and `clingen_scope`.

Before November 20, 2026, a gene was left out when another panel's curation named the CMT-spectrum disease in its title or among its included OMIM phenotypes. That hid the best-curated genes: AIFM1 (Cowchock syndrome, CMTX4), PRPS1 (CMTX5), and SPG11 (CMT2X). They are now listed, marked `includes neuropathy`. A fact-check the same day found that three lumped curations listing no OMIM phenotypes also include the neuropathy evidence: mitochondrial disease for COX6A1 (Strong) and MPV17 (Definitive), and the autosomal dominant POLR3B-related disorder (Definitive, September 3, 2025). None of these genes moves into the main table, which follows the CMT panel only.

`clingen_status` says "not curated" or names each curation the gene has, with its classification, inheritance, panel, and date, and a note on its scope. Where the curation page says which OMIM phenotypes the panel included or excluded, the note says whether the neuropathy was left out (as it was for LMNA, JAG1, and VCP, among others). `clingen_scope` sums this up as one of:
- `not curated`: no gene-validity curation.
- `other disease`: curated for a different disease, not for the neuropathy.
- `refuted other disease`: the gene's only curation is Refuted, for a different disease (HARS1 for Usher syndrome type 3, SCN9A for epilepsy). That rating says nothing about the neuropathy.
- `neuropathy not scored`: the curation discusses the neuropathy study but does not score it (PCK2).
- `includes neuropathy`: a broader curation that includes the neuropathy among its OMIM phenotypes (AIFM1, PRPS1, SPG11) or in its evidence (COX6A1, MPV17, POLR3B).
- `scope unresolved`: a broader curation that may or may not cover the neuropathy (SURF1, MT-TV).

### How the List Was Built

1. **Screen.** Every gene rated Green or Amber on any of three PanelApp panels and not in the main table: Genomics England panel 85 "Hereditary neuropathy" (v1.513), Genomics England panel 846 "Hereditary neuropathy or pain disorder" (v8.38), and PanelApp Australia panel 3070 "Hereditary Neuropathy" (v3.5). That is 255 genes. AKAP6 was added by hand from a 2026 paper; it is on none of these three panels. Other PanelApp panels were not searched.
2. **Decide.** Each gene's reported diseases were read from PanelApp, Mondo (through the Monarch API), and ClinGen. For each candidate, the key paper's PubMed abstract was read. Evidence notes come from those abstracts and say only what they report.
3. **Check ClinGen.** ClinGen's gene-validity download of November 17, 2026, plus each candidate's ClinGen gene page for the OMIM phenotypes included or excluded.
4. **Fact-check.** On November 20, 2026, every row was checked against ClinGen's current curations and the primary papers. That check corrected the ClinGen scope notes, the POLR3B citation, and several evidence notes, and added later papers to `more_pmids`. It did not re-run the screen: the union of the three PanelApp panels was not rebuilt.

Of the 256 genes screened, 59 are listed and 197 are left out. Every gene left out is in [`data/candidate-genes-excluded.csv`](data/candidate-genes-excluded.csv) with a reason, so the decisions can be checked. The `category` column there is one of:
- `mnd` (8): a motor neuron disease named as spinal muscular atrophy or ALS, not as dHMN (BICD2 and CHCHD10, for example).
- `other` (187): a syndrome or another main disease, in which neuropathy is one feature.
- `unconfirmed` (2): no CMT-spectrum report was found in the sources read (ARPC3 and PRPH).

Red-rated genes were not screened unless another panel rates them Green or Amber, and genes on none of the three panels were not screened, apart from AKAP6. The list is therefore not complete.

### Candidate Columns

| Column | Source | Notes |
|---|---|---|
| `gene`, `hgnc_id` | HGNC via PanelApp | Current HGNC symbol and ID. CFAP276 was C1orf194 |
| `reported_disease` | PanelApp, Mondo, or key paper | The CMT-spectrum disease reported for the gene, in plain words. "Provisional in OMIM" marks a link OMIM itself treats as unconfirmed |
| `omim_phenotype` | PanelApp or ClinGen | OMIM phenotype ID(s) where one exists. IDs only |
| `inheritance` | Key paper | AD, AR, XL, or MT (mitochondrial) for the reported neuropathy, which can differ from the gene's other diseases |
| `panelapp` | PanelApp APIs | Rating and version on Genomics England panels 85 and 846 and PanelApp Australia panel 3070, or "not listed" |
| `clingen_status` | ClinGen | "not curated", or each gene-disease validity curation with classification, inheritance, panel, and date, plus a note on its scope and on included or excluded OMIM phenotypes |
| `clingen_scope` | ClinGen | How the gene's curations relate to the neuropathy: not curated, other disease, refuted other disease, neuropathy not scored, includes neuropathy, or scope unresolved |
| `key_source` | PubMed | First author, year, journal, volume, and pages of the first or main report (the original article, with any erratum noted) |
| `key_pmid`, `key_doi` | PubMed | PubMed ID and DOI of the key source |
| `more_pmids` | PubMed | Other papers used for the evidence note, such as later families, separated by `; `. The page links them after the key source |
| `evidence_note` | Key source abstract | One plain sentence on how much evidence there is |
| `date_checked` | Build notes | When PanelApp, ClinGen, and the sources were checked |

The excluded file has `gene`, `hgnc_id`, `panelapp`, `category`, `reason`, `clingen_curations` (every ClinGen gene-disease validity curation the gene has, as "disease (classification, inheritance, panel, date)" separated by `; `, or "not curated"), and `date_checked`. `tools/fill-excluded-curations.py` fills `clingen_curations` from ClinGen's download, matching by HGNC ID.

The additional list is checked by hand, not rebuilt by the monthly job. Instead, the monthly job runs `tools/check-candidate-drift.py`, which compares both files with ClinGen's current download and opens an issue (or comments on the open one) when a listed or excluded gene's curations change. `tools/build-exports.py` refuses to build if a gene appears in both lists, so a listed gene that ClinGen's CMT panel curates must be moved to the main table and given a dated changelog entry.

## Rebuilding

The data tools need only Python 3 and its standard library. `tools/build-exports.py` also needs `openpyxl` for the Excel file.

```bash
python3 tools/build-clingen.py    # download ClinGen's file, keep the CMT panel's rows
python3 tools/fetch-monarch.py    # cache Monarch/Mondo lookups in cache/
python3 tools/build-subtypes.py   # derive subtype names (writes subtype-names.csv and subtype-terms.csv)
python3 tools/fetch-clingen-phenotypes.py  # included/excluded OMIM phenotypes per curation (add --refresh)
python3 tools/fetch-links.py      # GeneReviews and PanelApp links (add --refresh to bypass cache/)
python3 tools/merge.py            # write data/cmt-genes.csv, adding data/hand-checked-sources.csv
python3 tools/fetch-aliases.py    # previous HGNC symbols for the page search
python3 tools/fill-excluded-curations.py  # ClinGen curations for the excluded genes (add --refresh, or --check)
python3 tools/check-candidate-drift.py  # report ClinGen changes for the listed and excluded genes (add --refresh)
python3 tools/build-page-table.py # site/table-body.html and site/candidate-table-body.html for cmt.blog
python3 tools/build-exports.py    # dist/: Excel, CSV, JSON, Data Package and the Pages site
```

A monthly GitHub Actions job is configured to run these steps and open a pull request when ClinGen, Mondo, GeneReviews or PanelApp data change. As of October 13, 2026 it has not completed a run. The published table on cmt.blog is updated separately from `site/table-body.html`. Hand-checked values are not refreshed automatically. Re-check trial statuses by hand. Changes are reviewed by hand before merging.

### Publishing

Every push to `main` that changes the data rebuilds the [GitHub Pages site](https://dknauss.github.io/cmt-gene-table/) (`.github/workflows/publish.yml`). To publish a version, add a dated entry to `CHANGELOG.md`, update `version` and `date-released` in `CITATION.cff`, then push a tag:

```bash
git tag v2026.11 && git push origin v2026.11
```

The workflow creates the GitHub release with the four files attached, and Zenodo archives the release with a DOI.

## Sources and Licences

- **ClinGen** gene-disease validity curations: public domain (CC0). Data from [search.clinicalgenome.org](https://search.clinicalgenome.org/kb/gene-validity).
- **Mondo** disease ontology (Mondo Disease Ontology), CC BY 4.0, retrieved through the [Monarch Initiative API](https://api-v3.monarchinitiative.org/) (CC BY 4.0). Cite: Vasilevsky NA et al., "Mondo: integrating disease terminology across communities," *Genetics* 232, no. 4 (2026): iyaf215, [doi:10.1093/genetics/iyaf215](https://doi.org/10.1093/genetics/iyaf215). (The 2022 medRxiv preprint, [doi:10.1101/2022.04.13.22273750](https://doi.org/10.1101/2022.04.13.22273750), is superseded.) Mondo is a name, not an acronym: it comes from the Latin *mundus*, "world." Only its IDs are written in capitals, with the prefix `MONDO:`, as in `MONDO:0007309`; column names such as `mondo_id` stay lower case.
- **OMIM**: identifiers only. OMIM's terms do not allow its content to be redistributed.
- **GeneReviews®**: © 1993–2026 University of Washington, Seattle. GeneReviews permits noncommercial research reproduction only, with credit and a link. This table links to chapters and records their titles. It does not copy chapter text. Neuropathy types and other facts drawn from GeneReviews are cited per row in `data/hand-checked-sources.csv`. See the [GeneReviews Copyright Notice and Usage Disclaimer](https://www.ncbi.nlm.nih.gov/books/n/gene/GRcopyright_permiss/).
- **PanelApp** ([Genomics England](https://panelapp.genomicsengland.co.uk/) and [PanelApp Australia](https://panelapp-aus.org/)): the table records a link, the panel version and each gene's public traffic-light rating. It does not copy evidence text or reviews. Check each site's terms before reuse. Genomics England's terms restrict commercial and diagnostic use, and this table must not be used for diagnosis.
- **ClinicalTrials.gov**: US National Library of Medicine; public data.
- **PubMed** abstracts are cited by link only.

The data in `data/` is released under [CC BY 4.0](LICENSE-DATA). Credit "Open CMT Gene Table (cmt.blog), using ClinGen (CC0) and Mondo (CC BY 4.0)". The scripts in `tools/` are under the [MIT License](LICENSE).

## Corrections

Open an issue or [contact cmt.blog](https://cmt.blog/contact/). Corrections are logged with dates in [CHANGELOG.md](CHANGELOG.md).
