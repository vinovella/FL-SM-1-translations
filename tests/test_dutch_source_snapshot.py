import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "dutch_source_snapshot.py"
SPEC = importlib.util.spec_from_file_location("dutch_source_snapshot", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SourceSnapshotTests(unittest.TestCase):
    def test_fingerprint_changes_when_embedded_english_changes(self):
        first, problems = MODULE.VALIDATOR.parse_translation_text(
            'translate deutsch a:\n    # mc "Hello"\n    mc "Hallo"\n', "a.rpy"
        )
        second, problems2 = MODULE.VALIDATOR.parse_translation_text(
            'translate deutsch a:\n    # mc "Goodbye"\n    mc "Tschüss"\n', "a.rpy"
        )
        self.assertEqual(problems, [])
        self.assertEqual(problems2, [])
        self.assertNotEqual(MODULE.fingerprint_blocks(first), MODULE.fingerprint_blocks(second))

    def test_build_rows_uses_manifest_reference_language(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "deutsch").mkdir()
            (root / "deutsch" / "a.rpy").write_text(
                'translate deutsch a:\n    # mc "Hello"\n    mc "Hallo"\n', encoding="utf-8"
            )
            rows = MODULE.build_rows(root, [{"relative_path": "a.rpy", "count_reference_language": "deutsch"}])
        self.assertEqual(rows[0]["string_dialogue_count"], "1")
        self.assertEqual(len(rows[0]["source_fingerprint_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
