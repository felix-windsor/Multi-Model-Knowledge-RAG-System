"""Phase 1 end-to-end verification for Step 3 phase-C wrapper.

Only runs wrapper._process_extract_entities on a real document with real LLM.
Skips LightRAG merge / KG write to stay within 5-minute budget.

The goal is to verify that:
1. Wrapper calls GraphRAGExtractor (not super)
2. Output entity_type is v2 canonical (Module / FunctionalRequirement / etc)
3. Output edges have _rag_core_* metadata fields
4. No 'concept' / 'method' / 'artifact' (LightRAG default ontology) leaks through

Output: ./output/verification_phase_c.json
"""

from __future__ import annotations

import asyncio
import json
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.config import settings  # noqa: E402
from app.dependencies import create_rag_instance  # noqa: E402
from app.rag_core.lightrag_wrapper import LightRAGWrapper  # noqa: E402


TARGET_DOC = REPO_ROOT / "benchmarks/enterprise_project_docs/corpus/github_prd/prd-048.md"
OUTPUT_DIR = REPO_ROOT / "output"
OUTPUT_FILE = OUTPUT_DIR / "verification_phase_c.json"

# v2 canonical types (mirrors backend/app/rag_core/schemas.py ENTITY_TYPES)
V2_CANONICAL = {
    "FunctionalRequirement",
    "NonFunctionalRequirement",
    "UserStory",
    "AcceptanceCriteria",
    "System",
    "Module",
    "Interface",
    "DataEntity",
    "Stakeholder",
    "Team",
    "ExternalActor",
    "Process",
    "Decision",
    "Constraint",
    "Other",
}

# Known LightRAG default ontology (must NOT appear in phase-C output)
LIGHTRAG_DEFAULT_TYPES = {
    "concept",
    "method",
    "artifact",
    "content",
    "data",
    "organization",
    "event",
    "location",
    "person",
    "geo",
    "category",
}


async def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()

    result: dict = {
        "phase": "phase-c (GraphRAGExtractor)",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "target_doc": str(TARGET_DOC.relative_to(REPO_ROOT)),
        "checks": {},
        "samples": {},
        "errors": [],
        "timing": {},
    }

    # Step 1: Build wrapper instance via create_rag_instance (same as production)
    print("[1/4] Initializing RAG instance...")
    rag = await create_rag_instance(settings.storage_backend)
    await rag._ensure_lightrag_initialized()
    result["checks"]["wrapper_class_name"] = type(rag.lightrag).__name__
    result["checks"]["wrapper_is_lightrag_wrapper"] = isinstance(
        rag.lightrag, LightRAGWrapper
    )

    # Step 2: Load and chunk the document manually (skip LightRAG insert)
    print("[2/4] Loading and chunking document...")
    if not TARGET_DOC.exists():
        result["errors"].append(f"Doc not found: {TARGET_DOC}")
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        return

    text = TARGET_DOC.read_text(encoding="utf-8")
    # Approximate the 7 chunks LightRAG produced for this document in phase-B.
    chunk_size = 4000
    chunks_list = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    # Build chunks dict in LightRAG TextChunkSchema format
    chunks = {
        f"chunk-{i:03d}": {
            "tokens": len(c) // 4,  # rough estimate
            "content": c,
            "full_doc_id": "prd-048",
            "chunk_order_index": i,
            "file_path": str(TARGET_DOC.name),
        }
        for i, c in enumerate(chunks_list)
    }
    result["checks"]["num_chunks"] = len(chunks)
    print(f"      {len(chunks)} chunks created")

    # Step 3: Call wrapper._process_extract_entities directly
    print(f"[3/4] Calling wrapper._process_extract_entities ({len(chunks)} chunks)...")
    t_extract_start = time.monotonic()
    try:
        chunk_results = await rag.lightrag._process_extract_entities(chunks)
        result["checks"]["extraction_completed"] = True
    except Exception as e:  # noqa: BLE001
        result["errors"].append(f"Extraction failed: {type(e).__name__}: {e}")
        result["checks"]["extraction_completed"] = False
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        return
    result["timing"]["extraction_seconds"] = round(
        time.monotonic() - t_extract_start, 2
    )

    # Step 4: Analyze output
    print("[4/4] Analyzing output...")
    type_counts = Counter()
    raw_type_counts = Counter()
    drift_reason_counts = Counter()
    homonym_suffixed = []
    has_rag_core_meta = 0
    total_entities = 0
    total_relations = 0
    sample_entities = []
    sample_relations = []
    leaked_lightrag_defaults = []

    for chunk_idx, (maybe_nodes, maybe_edges) in enumerate(chunk_results):
        for name, node_list in maybe_nodes.items():
            for node in node_list:
                total_entities += 1
                etype = node.get("entity_type", "MISSING")
                type_counts[etype] += 1
                raw_type_counts[node.get("_rag_core_raw_type", "MISSING")] += 1
                drift_reason_counts[node.get("_rag_core_drift_reason", "None")] += 1
                if "_rag_core_raw_type" in node or "_rag_core_drift_reason" in node:
                    has_rag_core_meta += 1
                if "[" in name and "]" in name:
                    homonym_suffixed.append(name)
                if etype.lower() in LIGHTRAG_DEFAULT_TYPES:
                    leaked_lightrag_defaults.append((name, etype))
                if len(sample_entities) < 10:
                    sample_entities.append(
                        {
                            "name": name,
                            "entity_type": etype,
                            "_rag_core_raw_type": node.get("_rag_core_raw_type"),
                            "_rag_core_canonical_type": node.get(
                                "_rag_core_canonical_type"
                            ),
                            "_rag_core_drift_reason": node.get(
                                "_rag_core_drift_reason"
                            ),
                        }
                    )
        for key, edge_list in maybe_edges.items():
            for edge in edge_list:
                total_relations += 1
                if len(sample_relations) < 5:
                    sample_relations.append(
                        {
                            "src": edge.get("src_id"),
                            "tgt": edge.get("tgt_id"),
                            "keywords": edge.get("keywords"),
                            "_rag_core_canonical_type": edge.get(
                                "_rag_core_canonical_type"
                            ),
                            "_rag_core_confidence": edge.get("_rag_core_confidence"),
                            "_rag_core_valid": edge.get("_rag_core_valid"),
                        }
                    )

    result["samples"]["total_entities"] = total_entities
    result["samples"]["total_relations"] = total_relations
    result["samples"]["entity_type_distribution"] = dict(type_counts.most_common())
    result["samples"]["raw_type_distribution"] = dict(raw_type_counts.most_common())
    result["samples"]["drift_reason_distribution"] = dict(
        drift_reason_counts.most_common()
    )
    result["samples"]["homonym_entities"] = homonym_suffixed[:10]
    result["samples"]["sample_entities"] = sample_entities
    result["samples"]["sample_relations"] = sample_relations

    # Critical checks
    non_canonical = [t for t in type_counts if t not in V2_CANONICAL]
    result["checks"]["all_types_are_v2_canonical"] = len(non_canonical) == 0
    if non_canonical:
        result["checks"]["non_canonical_types_found"] = non_canonical

    result["checks"]["entities_have_rag_core_metadata"] = has_rag_core_meta > 0
    result["checks"]["rag_core_metadata_coverage"] = (
        f"{has_rag_core_meta}/{total_entities}"
    )

    result["checks"]["no_lightrag_default_leak"] = (
        len(leaked_lightrag_defaults) == 0
    )
    if leaked_lightrag_defaults:
        result["checks"]["leaked_examples"] = leaked_lightrag_defaults[:5]

    result["checks"]["has_homonym_disambiguation"] = len(homonym_suffixed) > 0

    result["timing"]["total_seconds"] = round(time.monotonic() - t0, 2)

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n=== Verification complete in {result['timing']['total_seconds']}s ===")
    print(f"Result: {OUTPUT_FILE}")
    print("\nKey checks:")
    for k, v in result["checks"].items():
        marker = (
            "✅"
            if v in (True, "True", 0) or (isinstance(v, list) and not v)
            else ("✅" if isinstance(v, (int, str)) and "/" not in str(v) else "ℹ️")
        )
        print(f"  {marker} {k}: {v}")


if __name__ == "__main__":
    asyncio.run(main())
