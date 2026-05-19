# Changsha Jingjia Public Multiformat 200 Benchmark

This benchmark records a local, public-source document set for validating
multiformat ingestion and retrieval behavior.

## Scope

- Documents: 200
- Source focus: Changsha Jingjia Microelectronics (`300474`) plus related public
  policy, project, API, and financial table materials.
- Raw file location: `data/full_online_changsha_jingjia_eval_20260519/raw/`
- Raw files are intentionally ignored by git. Commit the manifest and scripts,
  not the downloaded PDFs, Word files, spreadsheets, or CSV exports.

## Format Distribution

- PDF: 103
- CSV: 44
- XLSX: 44
- DOC: 3
- DOCX: 2
- XLS: 1
- HTML: 3

## Category Distribution

- `table_ledger`: 111
- `policy_process`: 40
- `scan_diagram`: 38
- `technical_manual`: 9
- `api_config`: 2

## Notes

- CNINFO PDFs are the company-specific announcement backbone.
- Financial CSV/XLSX files are exported from a public financial data API for
  format-level benchmark coverage; the data is public, but these exported files
  are generated local artifacts.
- This is not an internal enterprise corpus and should not be described as one.
