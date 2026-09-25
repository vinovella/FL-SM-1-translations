import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "dutch_phase0_inventory.py"
SPEC = importlib.util.spec_from_file_location("dutch_phase0_inventory", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class InventoryParserTests(unittest.TestCase):
    def test_parse_dialogue_and_strings_blocks(self):
        content = '''\
translate deutsch abc123:
    # mc "Hello, [mcname]!"
    mc "Hallo, [mcname]!"

translate deutsch def456:
    # "Two words"
    "Zwei Wörter"

translate deutsch strings:
    old "Save"
    new "Speichern"
    old "Progress: 100%%"
    new "Fortschritt: 100%%"
'''
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.rpy"
            path.write_text(content, encoding="utf-8")
            metrics = MODULE.parse_translation_file(path, "deutsch")

        self.assertEqual(metrics.translation_blocks, 3)
        self.assertEqual(metrics.source_units, 4)
        # [mcname] and %% are tokens and therefore not counted as source words.
        self.assertEqual(metrics.source_words, 6)

    def test_word_count_ignores_renpy_tokens(self):
        self.assertEqual(MODULE.word_count("Hello {i}beautiful{/i} [mcname] {w=0.5}"), 2)
        self.assertEqual(MODULE.word_count("Progress %(count)d of %s"), 2)

    def test_phase_assignment_covers_approved_categories(self):
        expected = {
            "common.rpy": "Phase 2",
            "code/hints.rpy": "Phase 2",
            "code/renpy/screens/preferences.rpy": "Phase 2",
            "code/classes/player.rpy": "Phase 2",
            "code/functions/example.rpy": "Phase 2",
            "code/debug/example.rpy": "Phase 2",
            "code/data/quests/example.rpy": "Phase 3",
            "code/live_chat/example.rpy": "Phase 3",
            "code/minigames/example.rpy": "Phase 3",
            "code/scenes/main_story/sm1ms001.rpy": "Phase 4",
            "code/scenes/character_scenes/foo.rpy": "Phase 5",
            "code/scenes/cross_characters/foo.rpy": "Phase 5",
            "code/scenes/it_office/foo.rpy": "Phase 6",
            "code/scenes/theatre/foo.rpy": "Phase 6",
            "code/scenes/movies/foo.rpy": "Phase 6",
        }
        for path, phase in expected.items():
            with self.subTest(path=path):
                self.assertEqual(MODULE.phase_for_path(path), phase)

    def test_unknown_category_is_not_silently_assigned(self):
        self.assertEqual(MODULE.phase_for_path("code/scenes/new_category/example.rpy"), "Unassigned")

    def test_discover_candidates_uses_union(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "deutsch" / "code").mkdir(parents=True)
            (root / "italian" / "code").mkdir(parents=True)
            (root / "deutsch" / "code" / "a.rpy").write_text("", encoding="utf-8")
            (root / "italian" / "code" / "b.rpy").write_text("", encoding="utf-8")
            (root / "italian" / "code" / "a.rpy").write_text("", encoding="utf-8")
            result = MODULE.discover_candidates(root, ["deutsch", "italian"])

        self.assertEqual(set(result), {"code/a.rpy", "code/b.rpy"})
        self.assertEqual(sorted(result["code/a.rpy"]), ["deutsch", "italian"])
        self.assertEqual(result["code/b.rpy"], ["italian"])


if __name__ == "__main__":
    unittest.main()
