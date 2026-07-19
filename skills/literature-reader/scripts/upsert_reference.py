#!/usr/bin/env python3
"""Safely merge one paper object into a MENTOR references.json library."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


ACCESS_RANK = {"unknown": 0, "waiting_user_pdf": 1, "abstract_only": 2, "fulltext": 3}
REQUIRED_NEW_FIELDS = ("id", "title", "authors", "year", "venue", "access_status")


def is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def merge_non_empty(existing: Any, incoming: Any) -> Any:
    if isinstance(existing, dict) and isinstance(incoming, dict):
        merged = dict(existing)
        for key, value in incoming.items():
            if key in merged:
                merged[key] = merge_non_empty(merged[key], value)
            elif not is_empty(value):
                merged[key] = value
        return merged
    return existing if is_empty(incoming) else incoming


def validate_library(library: Any) -> None:
    if not isinstance(library, dict) or not isinstance(library.get("meta"), dict):
        raise ValueError("references.json must contain object field 'meta'")
    if not isinstance(library.get("papers"), list):
        raise ValueError("references.json must contain array field 'papers'")
    if any(not isinstance(paper, dict) or not paper.get("id") for paper in library["papers"]):
        raise ValueError("every existing paper must be an object with a non-empty id")


def validate_incoming(paper: Any) -> None:
    if not isinstance(paper, dict) or not isinstance(paper.get("id"), str) or not paper["id"].strip():
        raise ValueError("incoming paper must be an object with a non-empty string id")
    status = paper.get("access_status")
    if status is not None and status not in ACCESS_RANK:
        raise ValueError(f"unsupported access_status: {status}")


def normalized_identifier(field: str, value: Any) -> str:
    if not isinstance(value, str):
        return ""
    normalized = value.strip().lower()
    if field == "doi":
        for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):]
                break
    return normalized


def find_identifier_conflict(papers: list[dict[str, Any]], incoming: dict[str, Any]) -> str | None:
    for field in ("doi", "arxiv_id"):
        wanted = normalized_identifier(field, incoming.get(field))
        if not wanted:
            continue
        for paper in papers:
            if paper["id"] != incoming["id"] and normalized_identifier(field, paper.get(field)) == wanted:
                return f"{field} {wanted} already belongs to id {paper['id']}"
    return None


def upsert_library(library: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    validate_library(library)
    validate_incoming(incoming)
    conflict = find_identifier_conflict(library["papers"], incoming)
    if conflict:
        raise ValueError(f"identifier conflict: {conflict}")

    result = {**library, "meta": dict(library["meta"]), "papers": [dict(p) for p in library["papers"]]}
    for index, existing in enumerate(result["papers"]):
        if existing["id"] != incoming["id"]:
            continue
        protected = dict(incoming)
        old_status = existing.get("access_status")
        new_status = protected.get("access_status")
        if old_status in ACCESS_RANK and new_status in ACCESS_RANK:
            if ACCESS_RANK[new_status] < ACCESS_RANK[old_status]:
                protected["access_status"] = old_status
        result["papers"][index] = merge_non_empty(existing, protected)
        return result

    missing = [field for field in REQUIRED_NEW_FIELDS if field not in incoming]
    if missing:
        raise ValueError(f"new paper missing required fields: {', '.join(missing)}")
    result["papers"].append(dict(incoming))
    return result


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            delete=False,
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as handle:
            temp_name = handle.name
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
        temp_name = None
    finally:
        if temp_name:
            try:
                Path(temp_name).unlink()
            except FileNotFoundError:
                pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely upsert one paper into references.json")
    parser.add_argument("library", type=Path)
    parser.add_argument("paper", type=Path, help="JSON file containing one paper object")
    args = parser.parse_args()

    try:
        library = load_json(args.library) if args.library.exists() else {"meta": {}, "papers": []}
        incoming = load_json(args.paper)
        merged = upsert_library(library, incoming)
        atomic_write_json(args.library, merged)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Updated {args.library}: {incoming['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
