"""Tests for LightRAGWrapper — the rag_core v2 interposer on LightRAG.

After Task 3.3 there are TWO surfaces under test:

  Phase C (live):  _process_extract_entities calls GraphRAGExtractor
                   directly, bypassing LightRAG's native extraction. Tests
                   in the "Phase C" section below cover this path using a
                   monkeypatched GraphRAGExtractor (no real LLM).

  Phase B (deprecated, kept for fall-back / legacy ingestion):
                   _apply_rag_core_v2 + its helpers still post-process
                   LightRAG-native chunk_results. Tests in the "Phase B
                   (deprecated)" section pin their behavior so the fall-back
                   path can't silently rot.

We avoid instantiating LightRAGWrapper directly because LightRAG requires
real storage backends to construct. Instead we use a ``_MockSelf`` shim
that exposes only ``llm_model_func`` — the single attribute the live
extraction path reads from ``self``.
"""

from __future__ import annotations

import logging

import pytest

from app.rag_core.lightrag_wrapper import (
    LightRAGWrapper,
    _canonicalize_entity_type_ci,
)
from app.rag_core.schemas import Entity, ExtractionResult, Relation


# ── Test fixtures / helpers ──────────────────────────────────────────────


class _MockSelf:
    """Minimal stand-in for a LightRAG instance.

    The phase-C ``_process_extract_entities`` only reads ``self.llm_model_func``.
    Using a fake-self avoids the heavy storage-backend init real LightRAG
    requires.
    """

    @staticmethod
    def llm_model_func(*_args, **_kwargs):  # pragma: no cover — never invoked
        raise AssertionError("llm_model_func should not be called in unit tests")


def _build_chunk(content: str, *, file_path: str | None = None) -> dict:
    """Build a TextChunkSchema-shaped dict for one chunk."""
    chunk = {
        "tokens": max(len(content), 1),
        "content": content,
        "full_doc_id": "doc-1",
        "chunk_order_index": 0,
    }
    if file_path is not None:
        chunk["file_path"] = file_path
    return chunk


# ═════════════════════════════════════════════════════════════════════════
# Structural tests (apply to both phases)
# ═════════════════════════════════════════════════════════════════════════


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


# ═════════════════════════════════════════════════════════════════════════
# Phase B (DEPRECATED) — pins the post-process helpers used as fall-back.
# These tests do NOT exercise the live extraction path; see the Phase-C
# section at the bottom for that. Kept to prevent silent rot of the
# fall-back helpers and the case-insensitive lookup that protects them.
# ═════════════════════════════════════════════════════════════════════════


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


# ═════════════════════════════════════════════════════════════════════════
# Phase C (LIVE) — wrapper routes every chunk through GraphRAGExtractor
# instead of LightRAG's native extraction. These tests monkeypatch the
# module-level GraphRAGExtractor name so no real LLM is invoked.
# ═════════════════════════════════════════════════════════════════════════


def _make_fake_extractor_cls(
    *,
    per_chunk_result: dict[str, ExtractionResult] | None = None,
    raise_for: set[str] | None = None,
    default_result: ExtractionResult | None = None,
    call_log: list | None = None,
):
    """Build a fake GraphRAGExtractor class for monkeypatching.

    - per_chunk_result: chunk_id → ExtractionResult to return.
    - raise_for: chunk_ids for which extract_chunk should raise ValueError.
    - default_result: returned for chunk_ids not covered by per_chunk_result.
    - call_log: optional list to append (text, chunk_id) tuples to per call.
    """
    per_chunk_result = per_chunk_result or {}
    raise_for = raise_for or set()
    default_result = default_result or ExtractionResult(entities=[], relations=[])

    class _FakeExtractor:
        def __init__(self, llm_func=None, config=None):
            self.llm_func = llm_func
            self.config = config

        async def extract_chunk(self, text, chunk_id=None):
            if call_log is not None:
                call_log.append((text, chunk_id))
            if chunk_id in raise_for:
                raise ValueError(f"simulated failure for {chunk_id}")
            return per_chunk_result.get(chunk_id, default_result)

    return _FakeExtractor


@pytest.mark.asyncio
async def test_wrapper_phase_c_uses_graph_rag_extractor_not_super(monkeypatch):
    """The live path must invoke ``GraphRAGExtractor.extract_chunk`` for
    every non-empty chunk and must NOT call ``super()._process_extract_entities``
    (which is what triggers LightRAG's native LLM prompt)."""
    from app.rag_core import lightrag_wrapper as wrapper_mod

    call_log: list = []
    fake_cls = _make_fake_extractor_cls(call_log=call_log)
    monkeypatch.setattr(wrapper_mod, "GraphRAGExtractor", fake_cls)

    # Tripwire: if super() were called we'd be told.
    super_called = []

    async def _tripwire(*_a, **_kw):
        super_called.append(True)
        return []

    monkeypatch.setattr(
        "lightrag.lightrag.LightRAG._process_extract_entities", _tripwire
    )

    chunks = {
        "c1": _build_chunk("alpha"),
        "c2": _build_chunk("beta"),
    }
    result = await LightRAGWrapper._process_extract_entities(_MockSelf(), chunks)

    assert len(result) == 2
    assert [cid for _, cid in call_log] == ["c1", "c2"]
    assert super_called == [], "super()._process_extract_entities must NOT be invoked"


@pytest.mark.asyncio
async def test_wrapper_phase_c_output_uses_v2_canonical_entity_type(monkeypatch):
    """v2 canonical type from the extractor must survive into the LightRAG
    dict shape unchanged — the whole point of phase C."""
    from app.rag_core import lightrag_wrapper as wrapper_mod

    fake_cls = _make_fake_extractor_cls(
        per_chunk_result={
            "c1": ExtractionResult(
                entities=[
                    Entity(
                        name="LoginFlow",
                        type="FunctionalRequirement",
                        raw_type="FunctionalRequirement",
                        canonical_type="FunctionalRequirement",
                        description="user login flow",
                    )
                ],
                relations=[],
            )
        }
    )
    monkeypatch.setattr(wrapper_mod, "GraphRAGExtractor", fake_cls)

    chunks = {"c1": _build_chunk("user logs in via SSO")}
    result = await LightRAGWrapper._process_extract_entities(_MockSelf(), chunks)
    nodes, _edges = result[0]

    entity_dict = nodes["LoginFlow"][0]
    assert entity_dict["entity_type"] == "FunctionalRequirement"
    assert entity_dict["_rag_core_canonical_type"] == "FunctionalRequirement"
    assert entity_dict["_rag_core_drift_reason"] is None


@pytest.mark.asyncio
async def test_wrapper_phase_c_one_chunk_failure_does_not_crash_batch(
    monkeypatch, caplog
):
    """Per-chunk fault isolation: a ValueError on chunk c2 must not stop
    c1 / c3 from being processed normally."""
    from app.rag_core import lightrag_wrapper as wrapper_mod

    def _ent(name):
        return Entity(name=name, type="Module", canonical_type="Module")

    fake_cls = _make_fake_extractor_cls(
        per_chunk_result={
            "c1": ExtractionResult(entities=[_ent("E_c1")], relations=[]),
            "c3": ExtractionResult(entities=[_ent("E_c3")], relations=[]),
        },
        raise_for={"c2"},
    )
    monkeypatch.setattr(wrapper_mod, "GraphRAGExtractor", fake_cls)

    chunks = {
        "c1": _build_chunk("alpha"),
        "c2": _build_chunk("beta"),
        "c3": _build_chunk("gamma"),
    }
    with caplog.at_level(logging.ERROR, logger=wrapper_mod.logger.name):
        result = await LightRAGWrapper._process_extract_entities(_MockSelf(), chunks)

    assert len(result) == 3
    assert "E_c1" in result[0][0]
    assert result[1] == ({}, {})  # c2 yields empty after failure
    assert "E_c3" in result[2][0]
    assert any(
        "GraphRAGExtractor failed" in r.message for r in caplog.records
    )


@pytest.mark.asyncio
async def test_wrapper_phase_c_output_shape_matches_lightrag_merge_contract(
    monkeypatch,
):
    """Smoke-check the dict shape — every required LightRAG field is present.

    Locks the contract with ``merge_nodes_and_edges`` downstream so a future
    refactor that drops a field is caught here, not in production.
    """
    from app.rag_core import lightrag_wrapper as wrapper_mod

    fake_cls = _make_fake_extractor_cls(
        per_chunk_result={
            "c1": ExtractionResult(
                entities=[
                    Entity(
                        name="A",
                        type="Module",
                        canonical_type="Module",
                        description="a",
                    ),
                    Entity(
                        name="B",
                        type="System",
                        canonical_type="System",
                        description="b",
                    ),
                ],
                relations=[
                    Relation(
                        source="A",
                        target="B",
                        type="DependsOn",
                        canonical_type="DependsOn",
                        description="A depends on B",
                        evidence="A uses B",
                        confidence=0.85,
                        valid=True,
                    )
                ],
            )
        }
    )
    monkeypatch.setattr(wrapper_mod, "GraphRAGExtractor", fake_cls)

    chunks = {"c1": _build_chunk("...", file_path="/path/x.md")}
    result = await LightRAGWrapper._process_extract_entities(_MockSelf(), chunks)
    nodes, edges = result[0]

    required_node_keys = {
        "entity_name", "entity_type", "description",
        "source_id", "file_path", "timestamp",
    }
    for name, dups in nodes.items():
        for d in dups:
            missing = required_node_keys - d.keys()
            assert not missing, f"entity {name!r} missing LightRAG keys: {missing}"

    required_edge_keys = {
        "src_id", "tgt_id", "weight", "description", "keywords",
        "source_id", "file_path", "timestamp",
    }
    for key, edges_list in edges.items():
        for e in edges_list:
            missing = required_edge_keys - e.keys()
            assert not missing, f"edge {key} missing LightRAG keys: {missing}"

    # chunk_data['file_path'] propagates to every entity/edge dict.
    assert nodes["A"][0]["file_path"] == "/path/x.md"
    assert list(edges.values())[0][0]["file_path"] == "/path/x.md"
    # Source id is the chunk id.
    assert nodes["A"][0]["source_id"] == "c1"
    # Confidence becomes edge weight.
    assert list(edges.values())[0][0]["weight"] == pytest.approx(0.85)
    # keywords = canonical relation type (for LightRAG's keyword retrieval).
    assert list(edges.values())[0][0]["keywords"] == "DependsOn"


@pytest.mark.asyncio
async def test_wrapper_phase_c_skips_extraction_for_empty_chunk_content(
    monkeypatch,
):
    """If a chunk has empty content the wrapper must yield ({}, {}) WITHOUT
    calling the extractor (saves an LLM round-trip)."""
    from app.rag_core import lightrag_wrapper as wrapper_mod

    call_log: list = []
    fake_cls = _make_fake_extractor_cls(call_log=call_log)
    monkeypatch.setattr(wrapper_mod, "GraphRAGExtractor", fake_cls)

    chunks = {
        "c1": _build_chunk(""),  # empty content
        "c2": _build_chunk("real content"),
    }
    result = await LightRAGWrapper._process_extract_entities(_MockSelf(), chunks)

    assert result[0] == ({}, {})  # c1: empty content → no extraction call
    assert call_log == [("real content", "c2")]  # only c2 reached the extractor
    assert len(result) == 2


@pytest.mark.asyncio
async def test_wrapper_phase_c_propagates_homonym_disambiguation(monkeypatch):
    """When ``GraphRAGExtractor`` returns entities whose names already carry
    a ``[type]`` homonym suffix (because normalize_entities_and_relations ran
    inside extract_chunk), the wrapper keeps them as separate node dicts."""
    from app.rag_core import lightrag_wrapper as wrapper_mod

    fake_cls = _make_fake_extractor_cls(
        per_chunk_result={
            "c1": ExtractionResult(
                entities=[
                    Entity(name="agent[Module]", type="Module", canonical_type="Module"),
                    Entity(name="agent[Stakeholder]", type="Stakeholder",
                           canonical_type="Stakeholder"),
                ],
                relations=[],
            )
        }
    )
    monkeypatch.setattr(wrapper_mod, "GraphRAGExtractor", fake_cls)

    chunks = {"c1": _build_chunk("...")}
    result = await LightRAGWrapper._process_extract_entities(_MockSelf(), chunks)
    nodes, _ = result[0]

    assert set(nodes.keys()) == {"agent[Module]", "agent[Stakeholder]"}
    assert nodes["agent[Module]"][0]["entity_type"] == "Module"
    assert nodes["agent[Stakeholder]"][0]["entity_type"] == "Stakeholder"
