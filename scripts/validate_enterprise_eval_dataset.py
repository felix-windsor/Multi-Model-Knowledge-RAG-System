#!/usr/bin/env python3
"""Validate the generated enterprise_200x420 evaluation dataset."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT_DIR / "benchmarks" / "enterprise_200x420"

EXPECTED_DOC_TYPES = {
    "technical_manual": 70,
    "policy_process": 50,
    "api_config": 30,
    "table_ledger": 30,
    "scan_diagram": 20,
}

EXPECTED_QUERY_TYPES = {
    "fact_lookup": 130,
    "summary": 70,
    "entity_relation": 90,
    "multi_hop": 80,
    "table_chart": 50,
}


def main() -> None:
    manifest = json.loads((DATASET_DIR / "manifest.json").read_text(encoding="utf-8"))
    cases = json.loads(
        (DATASET_DIR / "eval_cases.enterprise_200x420.json").read_text(encoding="utf-8")
    )
    api_cases = json.loads(
        (DATASET_DIR / "api_benchmark_cases.enterprise_200x420.json").read_text(
            encoding="utf-8"
        )
    )
    documents = {doc["doc_id"]: doc for doc in manifest["documents"]}

    assert manifest["document_count"] == 200
    assert manifest["query_count"] == 420
    assert Counter(doc["type"] for doc in documents.values()) == EXPECTED_DOC_TYPES
    assert Counter(case["question_type"] for case in cases["cases"]) == EXPECTED_QUERY_TYPES
    assert len(api_cases["queries"]) == 420
    assert api_cases["document"] == "benchmarks/enterprise_200x420/combined_corpus.md"
    assert (DATASET_DIR / "combined_corpus.md").exists()

    for doc in documents.values():
        path = DATASET_DIR / doc["path"]
        assert path.exists(), f"missing document: {path}"
        assert "合成企业文档样例" in path.read_text(encoding="utf-8")

    for case in cases["cases"]:
        assert case["doc_id"] in documents
        assert case["expected_keywords"]

    print("enterprise_200x420 dataset validation passed")


if __name__ == "__main__":
    main()
