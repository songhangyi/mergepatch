"""Apply an RFC 7396 JSON Merge Patch."""
from __future__ import annotations


def _clone(value: object) -> object:
    if isinstance(value, dict):
        return {key: _clone(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_clone(item) for item in value]
    return value


def apply_merge_patch(document: object, patch: object) -> object:
    if not isinstance(patch, dict):
        return _clone(patch)
    base = document if isinstance(document, dict) else {}
    merged = {key: _clone(value) for key, value in base.items()}
    for key, value in patch.items():
        if value is None:
            merged.pop(key, None)
            continue
        if isinstance(value, dict):
            merged[key] = apply_merge_patch(base.get(key), value)
            continue
        merged[key] = _clone(value)
    return merged
