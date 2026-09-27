"""Apply an RFC 7396 JSON Merge Patch."""
from __future__ import annotations


def apply_merge_patch(document: object, patch: object) -> object:
    if not isinstance(patch, dict):
        return patch
    base = document if isinstance(document, dict) else {}
    merged = dict(base)
    for key, value in patch.items():
        if value is None:
            merged.pop(key, None)
            continue
        if isinstance(value, dict):
            merged[key] = apply_merge_patch(merged.get(key), value)
            continue
        merged[key] = value
    return merged
