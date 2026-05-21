# Enterprise Project Docs Benchmark

This corpus is the current public benchmark anchor for the project. It replaces
the previous hand-written markdown dataset and keeps the source documents as
plain markdown files under `corpus/`.

## Scope

- Total documents: 200
- Total word count: 349,901
- Subsets:
  - `pure_srs`: 120 public software requirements documents
  - `github_prd`: 47 public PRD/spec documents from GitHub repositories
  - `tech_blog`: 33 public engineering blog articles
- Languages:
  - English: 163
  - Chinese: 37

## Files

- `manifest.json`: one entry per document with source URL, license, language,
  word count, category, local path, and SHA-256 hash.
- `summary.json`: aggregate counts used by tests and documentation.
- `download_corpus.py`: collector script for rebuilding the corpus subsets.
- `corpus/`: committed markdown documents used by local evaluation.

## Validation

Run from the repository root:

```bash
.venv/bin/python scripts/validate_enterprise_project_docs_dataset.py
```

The corresponding unit test is
`backend/tests/test_enterprise_project_docs_dataset.py`.
