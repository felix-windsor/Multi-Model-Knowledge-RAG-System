"""Tests for LightRAGWrapper — the rag_core v2 interposer on LightRAG.

We test the pure-transform staticmethods (``_apply_rag_core_v2``,
``_to_*``, ``_canonicalize_entity_type_ci``) rather than the async
``_process_extract_entities`` override, because:

  - LightRAG requires real storage backends to instantiate, which would
    turn unit tests into integration tests.
  - The override is a 3-line shim: ``super().call → _apply_rag_core_v2``.
    Its only logic is verified via the staticmethod tests.
  - The wire-up itself (subclass relationship, that the override exists
    and calls super correctly) is verified by the ``test_wrapper_*``
    structural tests below.

Test surface:
  1. Subclass relationship is correct.
  2. v1-style Chinese type names get canonicalized to v2 English canonicals.
  3. LightRAG's lowercased English types still match v2 canonicals
     (case-insensitive lookup fix).
  4. Homonym entities are preserved as separate disambiguated nodes.
  5. Empty input passes through.
  6. rag_core exceptions fall back to the raw chunk (no crash).
"""

from __future__ import annotations

import logging

import pytest

from app.rag_core.lightrag_wrapper import (
    LightRAGWrapper,
    _canonicalize_entity_type_ci,
)


# ── 1. Subclass relationship ─────────────────────────────────────────────


def test_wrapper_is_lightrag_subclass():
    """Inheritance is the *whole* hook mechanism — without this we have no
    way to interpose on _process_extract_entities."""
    from lightrag.lightrag import LightRAG

    assert issubclass(LightRAGWrapper, LightRAG)


def test_wrapper_overrides_process_extract_entities_directly():
    """The override must live on the wrapper class itself; if Python's MRO
    silently fell back to LightRAG's version the interposer would be inert."""
    from lightrag.lightrag import LightRAG

    assert (
        LightRAGWrapper._process_extract_entities
        is not LightRAG._process_extract_entities
    )
    assert "_process_extract_entities" in LightRAGWrapper.__dict__


# ── 2. Type canonicalization (v1 Chinese → v2 English) ───────────────────


def test_wrapper_canonicalizes_chinese_entity_type_to_v2_english():
    """v1-style Chinese types in raw chunk_results must come out as v2
    English canonicals (Chinese is not lowercased by LightRAG's parser)."""
    chunk = (
        {
            "信息系统": [
                {
                    "entity_name": "信息系统",
                    "entity_type": "平台",  # v2 alias → System
                    "description": "core information platform",
                    "source_id": "chunk-1",
                    "file_path": "doc.md",
                    "timestamp": 1,
                }
            ]
        },
        {},
    )

    result = LightRAGWrapper._apply_rag_core_v2([chunk])

    nodes, _edges = result[0]
    flattened = [d for dups in nodes.values() for d in dups]
    assert len(flattened) == 1
    assert flattened[0]["entity_type"] == "System"
    assert flattened[0]["_rag_core_raw_type"] == "平台"
    assert flattened[0]["_rag_core_drift_reason"] == "mapped_alias"


def test_wrapper_canonicalizes_lightrag_lowercased_english_type():
    """LightRAG's parser lowercases entity_type before our wrapper sees it,
    so 'System' arrives as 'system'. The case-insensitive lookup must still
    canonicalize it to 'System' (NOT fall through to 'Other')."""
    chunk = (
        {
            "LoginSystem": [
                {
                    "entity_name": "LoginSystem",
                    "entity_type": "system",  # lowercased by LightRAG
                    "description": "auth gateway",
                    "source_id": "chunk-1",
                    "file_path": "doc.md",
                    "timestamp": 1,
                }
            ]
        },
        {},
    )

    result = LightRAGWrapper._apply_rag_core_v2([chunk])
    nodes, _ = result[0]
    assert nodes["LoginSystem"][0]["entity_type"] == "System"
    # Direct canonical hit (case-insensitive) → no drift reason.
    assert nodes["LoginSystem"][0]["_rag_core_drift_reason"] is None


def test_canonicalize_entity_type_ci_unknown_falls_back_to_other():
    """Unknown types must still land in the 'Other' bucket with the
    rag_core-standard drift reason (consistency with canonicalize_entity_type)."""
    canonical, drift = _canonicalize_entity_type_ci("totally_made_up_type")
    assert canonical == "Other"
    assert drift == "unknown_entity_type"


# ── 3. Homonym handling ──────────────────────────────────────────────────


def test_wrapper_preserves_homonym_entities_through_normalization():
    """Three 'agent' entities of different types must survive as three
    disambiguated nodes after the wrapper post-processes them."""
    chunk = (
        {
            "agent": [
                {
                    "entity_name": "agent",
                    "entity_type": "module",  # → Module
                    "description": "software agent module",
                    "source_id": "chunk-1",
                    "file_path": "doc.md",
                    "timestamp": 1,
                },
                {
                    "entity_name": "agent",
                    "entity_type": "stakeholder",  # → Stakeholder
                    "description": "human reviewer",
                    "source_id": "chunk-1",
                    "file_path": "doc.md",
                    "timestamp": 1,
                },
                {
                    "entity_name": "agent",
                    "entity_type": "externalactor",  # → ExternalActor
                    "description": "third-party service",
                    "source_id": "chunk-1",
                    "file_path": "doc.md",
                    "timestamp": 1,
                },
            ]
        },
        {},
    )

    result = LightRAGWrapper._apply_rag_core_v2([chunk])
    nodes, _ = result[0]

    assert set(nodes.keys()) == {
        "agent[Module]",
        "agent[Stakeholder]",
        "agent[ExternalActor]",
    }
    # The disambiguated key must hold exactly one entity each.
    for key in nodes:
        assert len(nodes[key]) == 1
        assert nodes[key][0]["entity_name"] == key


def test_wrapper_flags_relation_endpoint_to_homonym_as_ambiguous():
    """A relation whose source matches a homonym must be tagged
    drift_reason='homonym_ambiguous' so downstream can audit it."""
    nodes_in = {
        "agent": [
            {
                "entity_name": "agent",
                "entity_type": "module",
                "description": "x",
                "source_id": "c1",
                "file_path": "d.md",
                "timestamp": 1,
            },
            {
                "entity_name": "agent",
                "entity_type": "stakeholder",
                "description": "y",
                "source_id": "c1",
                "file_path": "d.md",
                "timestamp": 1,
            },
        ],
        "LoginSystem": [
            {
                "entity_name": "LoginSystem",
                "entity_type": "module",
                "description": "auth",
                "source_id": "c1",
                "file_path": "d.md",
                "timestamp": 1,
            }
        ],
    }
    edges_in = {
        ("agent", "LoginSystem"): [
            {
                "src_id": "agent",
                "tgt_id": "LoginSystem",
                "weight": 1.0,
                "description": "depends on",
                "keywords": "depends_on",  # → DependsOn
                "source_id": "c1",
                "file_path": "d.md",
                "timestamp": 1,
            }
        ]
    }

    result = LightRAGWrapper._apply_rag_core_v2([(nodes_in, edges_in)])
    _, edges_out = result[0]

    # Source endpoint should be rewritten to one of the disambiguated names.
    edge_list = [e for v in edges_out.values() for e in v]
    assert len(edge_list) == 1
    assert edge_list[0]["src_id"].startswith("agent[")
    assert edge_list[0]["_rag_core_drift_reason"] == "homonym_ambiguous"


# ── 4. Empty input ────────────────────────────────────────────────────────


def test_wrapper_handles_empty_chunk_results_list():
    """Empty list comes from LightRAG when nothing was extracted; wrapper
    must not crash and must not call rag_core."""
    assert LightRAGWrapper._apply_rag_core_v2([]) == []


def test_wrapper_handles_chunk_with_no_entities_or_relations():
    """A chunk with empty nodes + empty edges is valid (LLM extracted
    nothing). Must pass through to a (dict, dict) tuple of empties."""
    result = LightRAGWrapper._apply_rag_core_v2([({}, {})])
    assert len(result) == 1
    nodes, edges = result[0]
    assert nodes == {}
    assert edges == {}


# ── 5. Defensive: rag_core failure must not crash the wrapper ────────────


def test_wrapper_falls_back_to_raw_chunk_when_rag_core_raises(monkeypatch, caplog):
    """If normalize_entities_and_relations explodes for any reason, the
    wrapper must log the error and return the raw chunk so the LightRAG
    pipeline keeps moving. A crash here would take down the whole insert."""
    from app.rag_core import lightrag_wrapper

    def _boom(*_a, **_kw):
        raise ValueError("simulated rag_core failure")

    monkeypatch.setattr(
        lightrag_wrapper, "normalize_entities_and_relations", _boom
    )

    raw_nodes = {
        "x": [
            {
                "entity_name": "x",
                "entity_type": "module",
                "description": "d",
                "source_id": "c1",
                "file_path": "f",
                "timestamp": 1,
            }
        ]
    }
    raw_edges: dict = {}
    raw_chunk = (raw_nodes, raw_edges)

    with caplog.at_level(logging.ERROR, logger=lightrag_wrapper.logger.name):
        result = LightRAGWrapper._apply_rag_core_v2([raw_chunk])

    # Fall-back: the raw chunk passes through untouched.
    assert result == [raw_chunk]
    # And an error was logged (no silent swallowing).
    assert any(
        "rag_core normalization failed" in record.message
        for record in caplog.records
    )


def test_wrapper_passes_through_unexpected_top_level_shape(caplog):
    """If LightRAG someday returns a dict instead of a list (e.g. major
    version bump), don't crash — log a warning and pass through."""
    from app.rag_core import lightrag_wrapper

    weird_input = {"not": "a list"}
    with caplog.at_level(logging.WARNING, logger=lightrag_wrapper.logger.name):
        result = LightRAGWrapper._apply_rag_core_v2(weird_input)  # type: ignore[arg-type]

    assert result is weird_input
    assert any(
        "unexpected chunk_results type" in record.message
        for record in caplog.records
    )


# ── 6. Round-trip integrity ──────────────────────────────────────────────


def test_wrapper_preserves_lightrag_metadata_through_round_trip():
    """file_path / timestamp / weight must survive the model conversion
    so LightRAG's downstream code still sees them."""
    nodes_in = {
        "Foo": [
            {
                "entity_name": "Foo",
                "entity_type": "module",
                "description": "a foo",
                "source_id": "chunk-xyz",
                "file_path": "/some/path.md",
                "timestamp": 1759872000,
            }
        ]
    }
    edges_in = {
        ("Foo", "Bar"): [
            {
                "src_id": "Foo",
                "tgt_id": "Bar",
                "weight": 0.73,
                "description": "Foo depends on Bar",
                "keywords": "depends_on, requires",  # multi-keyword
                "source_id": "chunk-xyz",
                "file_path": "/some/path.md",
                "timestamp": 1759872000,
            }
        ]
    }

    result = LightRAGWrapper._apply_rag_core_v2([(nodes_in, edges_in)])
    nodes_out, edges_out = result[0]

    foo = nodes_out["Foo"][0]
    assert foo["file_path"] == "/some/path.md"
    assert foo["timestamp"] == 1759872000
    assert foo["source_id"] == "chunk-xyz"

    # Bar isn't in entities; relation endpoint stays as-is (downstream
    # relation_scorer will mark it invalid via missing-endpoint logic).
    edge = list(edges_out.values())[0][0]
    assert edge["weight"] == 0.73
    assert edge["file_path"] == "/some/path.md"
    assert edge["timestamp"] == 1759872000
    # Original keyword string preserved for LightRAG keyword retrieval.
    assert edge["keywords"] == "depends_on, requires"
    # Canonical v2 type exposed separately.
    assert edge["_rag_core_canonical_type"] == "DependsOn"
