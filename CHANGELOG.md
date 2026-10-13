# Changelog

## 2026-10-13 (Source Disagreements Documented)

- SH3TC2, PRX, GJB1 and MED25 phenotype values: reviewed and kept. Where sources disagree, the note now says "Sources disagree" and names both sources, and the README lists all four cases.
- README cites the peer-reviewed MONDO paper (*Genetics*, 2026).

## 2026-10-13 (Links and Hand-Checked Columns)

- Added `genereviews` and `panelapp`, built by the new `tools/fetch-links.py` from NCBI's GeneReviews report files and the PanelApp APIs: Genomics England panel 846 v8.38 and PanelApp Australia panel 3070 v3.1. 50 genes have a GeneReviews chapter (30 overview-only) and 20 have none. All 70 genes are on both panels. The monthly workflow now rebuilds these columns.
- Filled `phenotype` for 69 genes, `therapy_programs` for 70 (10 with registered trials, 60 "none found as of 2026-10-13") and `plain_note` for 70. Every value is cited in the new `data/hand-checked-sources.csv`.
- SEPTIN9's phenotype is left blank. SH3TC2 and PRX are flagged for review, because GeneReviews' overview table disagrees with another source.

## 2026-10-13

- First draft: 72 ClinGen curations (70 genes) from the Charcot-Marie-Tooth Disease Gene Curation Expert Panel, ClinGen file of October 13, 2026.
- Added subtype names, MONDO IDs and OMIM phenotype IDs from MONDO via the Monarch API. 62 genes have names; 8 do not.
