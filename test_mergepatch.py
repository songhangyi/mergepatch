import unittest

from mergepatch import added_keys, apply_merge_patch, apply_merge_patches, patch_size, removed_keys


class MergePatchTest(unittest.TestCase):
    def test_rfc_shape(self) -> None:
        doc = {"a": "b", "c": {"d": "e", "f": "g"}}
        patch = {"a": "z", "c": {"f": None}}
        self.assertEqual(apply_merge_patch(doc, patch), {"a": "z", "c": {"d": "e"}})

    def test_empty_patch_does_not_mutate(self) -> None:
        doc = {"a": {"b": 1}, "c": [1]}
        out = apply_merge_patch(doc, {})
        out["a"]["b"] = 9
        out["c"].append(2)
        self.assertEqual(doc, {"a": {"b": 1}, "c": [1]})

    def test_apply_several(self) -> None:
        got = apply_merge_patches({"a": 1, "b": 2}, {"a": 3}, {"b": None})
        self.assertEqual(got, {"a": 3})
        self.assertEqual(removed_keys({"a": 3, "b": None}), ["b"])
        self.assertEqual(added_keys({"a": 1}, {"b": 2, "a": 3, "c": None}), ["b"])
        self.assertEqual(patch_size({"b": 2, "c": None}), 2)
        self.assertEqual(patch_size(["x"]), 0)

    def test_replace_non_object(self) -> None:
        self.assertEqual(apply_merge_patch({"a": 1}, ["x"]), ["x"])
        self.assertEqual(apply_merge_patch(["x"], {"a": 1}), {"a": 1})


if __name__ == "__main__":
    unittest.main()
