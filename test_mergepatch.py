import unittest

from mergepatch import apply_merge_patch


class MergePatchTest(unittest.TestCase):
    def test_rfc_shape(self) -> None:
        doc = {"a": "b", "c": {"d": "e", "f": "g"}}
        patch = {"a": "z", "c": {"f": None}}
        self.assertEqual(apply_merge_patch(doc, patch), {"a": "z", "c": {"d": "e"}})

    def test_replace_non_object(self) -> None:
        self.assertEqual(apply_merge_patch({"a": 1}, ["x"]), ["x"])
        self.assertEqual(apply_merge_patch(["x"], {"a": 1}), {"a": 1})


if __name__ == "__main__":
    unittest.main()
