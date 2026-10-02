# mergepatch

Apply a JSON Merge Patch (RFC 7396).

A JSON `null` removes a key. Nested objects merge. Arrays and scalars replace the target. Untouched nested values are copied, so later edits to the result do not change the input.

```python
from mergepatch import apply_merge_patch, apply_merge_patches

apply_merge_patch({"a": "b", "c": {"d": "e"}}, {"a": "z", "c": {"d": None}})
# {"a": "z", "c": {}}
apply_merge_patches({"a": 1, "b": 2}, {"a": 3}, {"b": None})
# {"a": 3}
```

```bash
python -m unittest test_mergepatch.py
```

MIT
