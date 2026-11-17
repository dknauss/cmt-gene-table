# Changelog

## 2026-11-17 (Candidate Genes Not Yet Curated)

- New, separate list: `data/candidate-genes.csv`, 56 genes reported to cause CMT or a related inherited neuropathy (CMT, HMSN, dHMN, HSN or HSAN, and similar) that ClinGen has not curated for that disease. 28 have no ClinGen curation at all; 28 are curated only for another disease. The main table is unchanged: still 72 curations covering 70 genes, and no gene is in both lists.
- How it was built: all 255 genes rated Green or Amber on Genomics England PanelApp panel 85 (v1.513), panel 846 (v8.38), or PanelApp Australia panel 3070 (v3.5) and not in the main table were checked against their reported diseases (PanelApp, Mondo, ClinGen) and against ClinGen's gene-validity download of 2026-11-17 and gene pages. AKAP6 was added by hand from Moghadam et al. 2026 (PMID 42993336). Each candidate cites a key paper whose PubMed abstract was read.
- `data/candidate-genes-excluded.csv` lists the 200 screened genes left out, each with a category and a reason: 187 syndromes or other main diseases, 8 motor neuron diseases named as SMA or ALS, 3 already covered by another ClinGen panel's curation (AIFM1, PRPS1, and SPG11), and 2 with no CMT report found in the sources read (ARPC3 and PRPH).
- README: new section explaining the rule, the screen, and the columns. The Scope and Gaps note now points to the candidate list.
- Downloads and site: the Excel file has a Candidates sheet; `candidate-genes.csv`, `candidate-genes.json`, and `candidate-genes-excluded.csv` are published on the site and attached to releases; the Data Package describes both new files; the web page shows the list below the main table. `tools/build-page-table.py` also writes `site/candidate-table-body.html` for cmt.blog. `tools/build-exports.py` stops the build if a gene is in more than one list.

## 2026-11-03 (Monthly Refresh)

- KIF1B (CMT2A1): ClinGen reclassified the gene-disease link from Limited to Disputed on 2026-10-19 (curation CCID:005229). The panel's reasons: one affected family only, MFN2 (in the same 1p36.2 linkage region) was not excluded in that family, and two later reported variants were too common in the general population to support the link. The `plain_note` now says so. PanelApp still rates KIF1B Red on both panels.
- HSPB1 and PLEKHG5: ClinGen's curation pages now list the OMIM phenotypes they included (HSPB1: OMIM:606595, OMIM:608634; PLEKHG5: OMIM:615376, OMIM:611067), so `clingen_included_omim` is now filled for both.
- Site: the table page now carries a short "Latest change" note about the KIF1B reclassification, with a link to this changelog. The record behind it: ClinGen's file as downloaded on 2026-10-13 (`data/clingen-cmt.csv`) has KIF1B as Limited, classified 2026-06-12; ClinGen's own site shows only the current Disputed record.
- BSCL2: the GeneReviews chapter is now titled "BSCL2-Related Motor Neuron Disorders / Seipinopathy"; the link is unchanged.
- No other rows changed. Still 72 curations covering 70 genes.

## 2026-10-14 (Downloads and Web Page) — v2026.10

- New [web page](https://dknauss.github.io/cmt-gene-table/) for the table: search (including previous gene symbols), sorting, per-row notes, trials and sources, and a guide to every column.
- The table can now be downloaded as Excel (with Columns and About sheets), CSV, JSON and a Frictionless Data Package, built by `tools/build-exports.py`. Each monthly update will be a tagged release with these files attached.
- Added `CITATION.cff` and `.zenodo.json` so the table can be cited and archived with a DOI.

## 2026-10-13 (Names and Trials Matched to Curations)

Prompted by an independent review of the table.
- Subtype names are now attached to the ClinGen curation they belong to (`curation_subtype_names`), using the OMIM phenotypes each curation includes. Other names for the gene go in `other_gene_names`; names from correlated associations only go in `unverified_names`. New columns: `curation_names_basis`, `clingen_included_omim`, `clingen_excluded_omim`, `other_condition_trials`. `historical_subtype_names` is unchanged and still gene-wide.
- Corrected rows on the page: PMP22 (CMT1A and HNPP no longer share names), NEFL (CMT1F with the dominant curation, CMT2E with the recessive one), SCN11A (HSAN2D removed; it belongs to SCN9A), NTRK1 (HSAN5 removed), MFN2 (HMSN6A and CMT5 moved out of the main names), GDAP1 (CMT2H removed: correlated only), and others where the names changed.
- Trials: the 13 CMT1A trials now appear only on the PMP22 CMT1A row; HNPP has none found. LTX-002 for SPTLC1 in ALS moved to `other_condition_trials`. `hand-checked-sources.csv` has a new `mondo_id` column for values that belong to one curation.
- The monthly workflow is configured but has not completed a run yet. PanelApp notes now give the signed-off version.

## 2026-10-13 (Mondo Spelled as a Name)

- Prose, source labels and notes now write the ontology's name as Mondo, its own spelling. IDs keep the `MONDO:` prefix, and column names and ClinGen's own `DISEASE ID (MONDO)` header are unchanged, so nothing that parses the files needs updating.

## 2026-10-13 (Source Disagreements Documented)

- SH3TC2, PRX, GJB1 and MED25 phenotype values: reviewed and kept. Where sources disagree, the note now says "Sources disagree" and names both sources, and the README lists all four cases.
- README cites the peer-reviewed Mondo paper (*Genetics*, 2026).

## 2026-10-13 (Links and Hand-Checked Columns)

- Added `genereviews` and `panelapp`, built by the new `tools/fetch-links.py` from NCBI's GeneReviews report files and the PanelApp APIs: Genomics England panel 846 v8.38 and PanelApp Australia panel 3070 v3.1. 50 genes have a GeneReviews chapter (30 overview-only) and 20 have none. All 70 genes are on both panels. The monthly workflow now rebuilds these columns.
- Filled `phenotype` for 69 genes, `therapy_programs` for 70 (10 with registered trials, 60 "none found as of 2026-10-13") and `plain_note` for 70. Every value is cited in the new `data/hand-checked-sources.csv`.
- SEPTIN9's phenotype is left blank. SH3TC2 and PRX are flagged for review, because GeneReviews' overview table disagrees with another source.

## 2026-10-13

- First draft: 72 ClinGen curations (70 genes) from the Charcot-Marie-Tooth Disease Gene Curation Expert Panel, ClinGen file of October 13, 2026.
- Added subtype names, Mondo IDs and OMIM phenotype IDs from Mondo via the Monarch API. 62 genes have names; 8 do not.
