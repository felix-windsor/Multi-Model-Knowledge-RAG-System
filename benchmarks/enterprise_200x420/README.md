# Enterprise 200x420 RAG Evaluation Dataset

This dataset is synthetic and desensitized. It is designed to simulate enterprise
intranet documents for RAG pipeline evaluation without containing confidential data.

## Scale

- Documents: 200
- Query cases: 420
- Document types: technical manuals, policy/process docs, API/config docs, table ledgers, scan/diagram-style docs
- Query types: fact lookup, summary, entity relation, multi-hop, table/chart understanding

## Files

- `manifest.json`: document inventory and distribution
- `eval_cases.enterprise_200x420.json`: query cases and expected keywords
- `api_benchmark_cases.enterprise_200x420.json`: compatible input for `scripts/run_api_benchmark.py`
- `combined_corpus.md`: all 200 documents concatenated for one-shot API benchmark runs
- `documents/`: markdown documents grouped by type

## Intended Metrics

- document processing time
- average query latency and P95 latency
- answer keyword hit rate
- entity/relation counts
- schema drift and invalid relation rates for the custom extraction core
