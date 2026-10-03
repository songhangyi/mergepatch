import unittest

from mergepatch import apply_merge_patch, apply_merge_patches, removed_keys


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

    def test_replace_non_object(self) -> None:
        self.assertEqual(apply_merge_patch({"a": 1}, ["x"]), ["x"])
        self.assertEqual(apply_merge_patch(["x"], {"a": 1}), {"a": 1})


if __name__ == "__main__":
    unittest.main()
