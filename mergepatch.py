"""Apply an RFC 7396 JSON Merge Patch."""
from __future__ import annotations


def _clone(value: object) -> object:
    if isinstance(value, dict):
        return {key: _clone(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_clone(item) for item in value]
    return value


def added_keys(document: object, patch: object) -> list[str]:
    if not isinstance(patch, dict):
        return []
    base = document if isinstance(document, dict) else {}
    return [key for key, value in patch.items() if value is not None and key not in base]


def patch_size(patch: object) -> int:
    if not isinstance(patch, dict):
        return 0
    return len(patch)


def is_empty(patch: object) -> bool:
    return patch_size(patch) == 0


def kept_keys(patch: object) -> list[str]:
    if not isinstance(patch, dict):
        return []
    return [key for key, value in patch.items() if value is not None]


def removed_keys(patch: object) -> list[str]:
    if not isinstance(patch, dict):
        return []
    return [key for key, value in patch.items() if value is None]


def removed_count(patch: object) -> int:
    return len(removed_keys(patch))


def kept_count(patch: object) -> int:
    return len(kept_keys(patch))


def added_count(document: object, patch: object) -> int:
    return len(added_keys(document, patch))


def replaced_count(document: object, patch: object) -> int:
    if not isinstance(patch, dict):
        return 0
    base = document if isinstance(document, dict) else {}
    return sum(1 for key, value in patch.items() if value is not None and key in base)


def apply_merge_patches(document: object, *patches: object) -> object:
    current = document
    for patch in patches:
        current = apply_merge_patch(current, patch)
    return current


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

def removes_any(patch: object) -> bool:
    return removed_count(patch) > 0

def touches(document: object, patch: object) -> bool:
    return added_count(document, patch) + replaced_count(document, patch) > 0
