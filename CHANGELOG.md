# Changelog

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
