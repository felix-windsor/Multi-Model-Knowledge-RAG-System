import json
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DATASET_DIR = ROOT_DIR / "benchmarks" / "synthetic_controlled_200x420"


def test_synthetic_controlled_eval_dataset_has_expected_scale_and_distribution():
    manifest = json.loads((DATASET_DIR / "manifest.json").read_text(encoding="utf-8"))
    cases = json.loads(
        (DATASET_DIR / "eval_cases.synthetic_controlled_200x420.json").read_text(encoding="utf-8")
    )
    api_cases = json.loads(
        (DATASET_DIR / "api_benchmark_cases.synthetic_controlled_200x420.json").read_text(
            encoding="utf-8"
        )
    )

    assert manifest["document_count"] == 200
    assert manifest["query_count"] == 420
    assert len(manifest["documents"]) == 200
    assert len(cases["cases"]) == 420
    assert len(api_cases["queries"]) == 420
    assert api_cases["document"] == "benchmarks/synthetic_controlled_200x420/combined_corpus.md"
    assert (DATASET_DIR / "combined_corpus.md").exists()

    doc_type_counts = Counter(doc["type"] for doc in manifest["documents"])
    assert doc_type_counts == {
        "technical_manual": 70,
        "policy_process": 50,
        "api_config": 30,
        "table_ledger": 30,
        "scan_diagram": 20,
    }

    query_type_counts = Counter(case["question_type"] for case in cases["cases"])
    assert query_type_counts == {
        "fact_lookup": 130,
        "summary": 70,
        "entity_relation": 90,
        "multi_hop": 80,
        "table_chart": 50,
    }


def test_synthetic_controlled_eval_cases_reference_existing_documents():
    manifest = json.loads((DATASET_DIR / "manifest.json").read_text(encoding="utf-8"))
    cases = json.loads(
        (DATASET_DIR / "eval_cases.synthetic_controlled_200x420.json").read_text(encoding="utf-8")
    )
    documents = {doc["doc_id"]: doc for doc in manifest["documents"]}

    for case in cases["cases"]:
        assert case["doc_id"] in documents
        doc_path = DATASET_DIR / documents[case["doc_id"]]["path"]
        assert doc_path.exists()
        assert case["expected_keywords"]
        assert case["question"].endswith("？")
