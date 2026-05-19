#!/usr/bin/env python3
"""Validate the public multiformat benchmark manifest.

The benchmark commits only metadata. Raw public files live under ignored
`data/full_online_changsha_jingjia_eval_20260519/raw/` for local evaluation.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT_DIR / "benchmarks" / "changsha_jingjia_public_multiformat_200"
RAW_ROOT = ROOT_DIR / "data" / "full_online_changsha_jingjia_eval_20260519"

EXPECTED_FORMATS = {
    "pdf": 103,
    "csv": 44,
    "xlsx": 44,
    "doc": 3,
    "docx": 2,
    "xls": 1,
    "html": 3,
}

EXPECTED_CATEGORIES = {
    "table_ledger": 111,
    "policy_process": 40,
    "scan_diagram": 38,
    "technical_manual": 9,
    "api_config": 2,
}


def load_manifest() -> dict:
    return json.loads((DATASET_DIR / "manifest.json").read_text(encoding="utf-8"))


def main() -> None:
    manifest = load_manifest()
    documents = manifest["documents"]

    assert manifest["name"] == "changsha_jingjia_public_multiformat_200_v2_balanced"
    assert len(documents) == 200
    assert Counter(doc["format"] for doc in documents) == EXPECTED_FORMATS
    assert Counter(doc["category"] for doc in documents) == EXPECTED_CATEGORIES

    missing = []
    for doc in documents:
        raw_path = RAW_ROOT / doc["local_path"]
        if not raw_path.exists() or raw_path.stat().st_size <= 0:
            missing.append(str(raw_path))

    if missing:
        raise AssertionError(
            "Raw benchmark files are missing. Rebuild or restore ignored data first:\n"
            + "\n".join(missing[:20])
        )

    print("public multiformat benchmark validation passed")


if __name__ == "__main__":
    main()
