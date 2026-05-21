import json
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DATASET_DIR = ROOT_DIR / "benchmarks" / "enterprise_project_docs"


def test_enterprise_project_docs_manifest_has_expected_distribution():
    documents = json.loads((DATASET_DIR / "manifest.json").read_text(encoding="utf-8"))
    summary = json.loads((DATASET_DIR / "summary.json").read_text(encoding="utf-8"))

    assert len(documents) == 200
    assert summary["total"] == 200
    assert Counter(doc["subset"] for doc in documents) == {
        "pure_srs": 120,
        "github_prd": 47,
        "tech_blog": 33,
    }
    assert Counter(doc["category"] for doc in documents) == {
        "functional_req": 87,
        "non_functional_req": 33,
        "prd": 47,
        "tech_blog": 33,
    }
    assert Counter(doc["language"] for doc in documents) == {
        "en": 163,
        "zh": 37,
    }


def test_enterprise_project_docs_manifest_tracks_sources_and_local_files():
    documents = json.loads((DATASET_DIR / "manifest.json").read_text(encoding="utf-8"))

    for doc in documents:
        assert doc["doc_id"]
        assert doc["title"]
        assert doc["source_url"].startswith("http")
        assert doc["local_path"].startswith("corpus/")
        assert doc["sha256"]
        assert (DATASET_DIR / doc["local_path"]).is_file()
