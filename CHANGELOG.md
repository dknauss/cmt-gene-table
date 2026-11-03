# Changelog

## 2026-11-03 (Monthly Refresh)

- KIF1B (CMT2A1): ClinGen reclassified the gene-disease link from Limited to Disputed on 2026-10-19 (curation CCID:005229). The panel's reasons: one affected family only, MFN2 (in the same 1p36.2 linkage region) was not excluded in that family, and two later reported variants were too common in the general population to support the link. The `plain_note` now says so. PanelApp still rates KIF1B Red on both panels.
- HSPB1 and PLEKHG5: ClinGen's curation pages now list the OMIM phenotypes they included (HSPB1: OMIM:606595, OMIM:608634; PLEKHG5: OMIM:615376, OMIM:611067), so `clingen_included_omim` is now filled for both.
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
