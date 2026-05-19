import json
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DATASET_DIR = ROOT_DIR / "benchmarks" / "changsha_jingjia_public_multiformat_200"


def test_public_multiformat_manifest_has_expected_distribution():
    manifest = json.loads((DATASET_DIR / "manifest.json").read_text(encoding="utf-8"))
    documents = manifest["documents"]

    assert manifest["name"] == "changsha_jingjia_public_multiformat_200_v2_balanced"
    assert len(documents) == 200
    assert Counter(doc["format"] for doc in documents) == {
        "pdf": 103,
        "csv": 44,
        "xlsx": 44,
        "doc": 3,
        "docx": 2,
        "xls": 1,
        "html": 3,
    }
    assert Counter(doc["category"] for doc in documents) == {
        "table_ledger": 111,
        "policy_process": 40,
        "scan_diagram": 38,
        "technical_manual": 9,
        "api_config": 2,
    }


def test_public_multiformat_manifest_tracks_sources_without_committing_raw_files():
    manifest = json.loads((DATASET_DIR / "manifest.json").read_text(encoding="utf-8"))

    for doc in manifest["documents"]:
        assert doc["doc_id"]
        assert doc["title"]
        assert doc["source"]
        assert doc["source_url"].startswith("http")
        assert doc["local_path"].startswith("raw/")
