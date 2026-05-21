#!/usr/bin/env python3
"""Validate the public enterprise project-document benchmark corpus."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT_DIR / "benchmarks" / "enterprise_project_docs"

EXPECTED_SUBSETS = {
    "pure_srs": 120,
    "github_prd": 47,
    "tech_blog": 33,
}

EXPECTED_CATEGORIES = {
    "functional_req": 87,
    "non_functional_req": 33,
    "prd": 47,
    "tech_blog": 33,
}

EXPECTED_LANGUAGES = {
    "en": 163,
    "zh": 37,
}


def load_manifest() -> list[dict]:
    return json.loads((DATASET_DIR / "manifest.json").read_text(encoding="utf-8"))


def main() -> None:
    documents = load_manifest()
    summary = json.loads((DATASET_DIR / "summary.json").read_text(encoding="utf-8"))

    assert len(documents) == 200
    assert summary["total"] == 200
    assert Counter(doc["subset"] for doc in documents) == EXPECTED_SUBSETS
    assert Counter(doc["category"] for doc in documents) == EXPECTED_CATEGORIES
    assert Counter(doc["language"] for doc in documents) == EXPECTED_LANGUAGES

    missing = []
    for doc in documents:
        corpus_path = DATASET_DIR / doc["local_path"]
        if not corpus_path.exists() or corpus_path.stat().st_size <= 0:
            missing.append(str(corpus_path))

    if missing:
        raise AssertionError(
            "Enterprise project-document corpus files are missing:\n"
            + "\n".join(missing[:20])
        )

    print("enterprise_project_docs dataset validation passed")


if __name__ == "__main__":
    main()
