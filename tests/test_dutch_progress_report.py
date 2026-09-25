import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "dutch_progress_report.py"
SPEC = importlib.util.spec_from_file_location("dutch_progress_report", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ProgressReportTests(unittest.TestCase):
    def test_report_counts_status_and_target_files(self):
        rows = [
            {"relative_path": "common.rpy", "phase": "Phase 2", "status": "done", "string_dialogue_count": "10", "source_word_estimate": "50"},
            {"relative_path": "code/hints.rpy", "phase": "Phase 2", "status": "not started", "string_dialogue_count": "5", "source_word_estimate": "20"},
        ]
        config = {
            "target_language": {"renpy_language_key": {"proposed": "dutch"}},
            "source": {"upstream_baseline_sha": "abc123"},
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "dutch").mkdir()
            (root / "dutch" / "common.rpy").write_text("", encoding="utf-8")
            report = MODULE.build_report(rows, config, root)

        self.assertIn("**Done:** 1 (50.0%)", report)
        self.assertIn("**Tracked Dutch `.rpy` files present:** 1", report)
        self.assertIn("| Phase 2 | 2 | 1 | 0 | 0 | 1 | 15 | 70 |", report)


if __name__ == "__main__":
    unittest.main()
