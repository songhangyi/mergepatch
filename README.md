# mergepatch

Apply a JSON Merge Patch (RFC 7396).

A JSON `null` removes a key. Nested objects merge. Arrays and scalars replace the target. The input document is not mutated.

```python
from mergepatch import apply_merge_patch

apply_merge_patch({"a": "b", "c": {"d": "e"}}, {"a": "z", "c": {"d": None}})
# {"a": "z", "c": {}}
```

```bash
python -m unittest test_mergepatch.py
```

MIT
