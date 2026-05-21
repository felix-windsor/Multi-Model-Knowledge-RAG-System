"""Small JSON extraction/repair helpers for LLM responses."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class JsonRepairResult:
    success: bool
    payload: dict[str, Any]
    error: str | None
    raw_text: str
    repaired_text: str


def repair_json_payload(raw: Any) -> JsonRepairResult:
    """Extract and parse one JSON object from an LLM response."""
    if isinstance(raw, dict):
        return JsonRepairResult(True, raw, None, json.dumps(raw, ensure_ascii=False), "")

    raw_text = str(raw or "").strip()
    candidates = _candidate_json_strings(raw_text)
    last_error: str | None = None

    for candidate in candidates:
        repaired = _repair_common_json_issues(candidate)
        try:
            payload = json.loads(repaired)
        except json.JSONDecodeError as exc:
            last_error = str(exc)
            continue

        if isinstance(payload, dict):
            return JsonRepairResult(True, payload, None, raw_text, repaired)
        last_error = "parsed JSON is not an object"

    return JsonRepairResult(False, {}, last_error or "no JSON object found", raw_text, "")


def _candidate_json_strings(raw_text: str) -> list[str]:
    candidates: list[str] = []

    for match in re.finditer(r"```(?:json)?\s*(.*?)```", raw_text, flags=re.DOTALL | re.IGNORECASE):
        fenced = match.group(1).strip()
        if fenced:
            candidates.append(fenced)

    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start != -1 and end != -1 and start < end:
        candidates.append(raw_text[start : end + 1])

    if raw_text:
        candidates.append(raw_text)

    unique: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate not in seen:
            unique.append(candidate)
            seen.add(candidate)
    return unique


def _repair_common_json_issues(text: str) -> str:
    repaired = text.strip().lstrip("\ufeff")
    repaired = re.sub(r",\s*([}\]])", r"\1", repaired)
    return repaired
