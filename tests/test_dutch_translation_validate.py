import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "dutch_translation_validate.py"
SPEC = importlib.util.spec_from_file_location("dutch_translation_validate", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


REFERENCE = '''\
translate deutsch block_a:
    # mc "Hello, [mcname]! {i}Welcome{/i}"
    mc "Hallo, [mcname]! {i}Willkommen{/i}"

translate deutsch strings:
    old "Save %s"
    new "Speichern %s"
'''

TARGET_GOOD = '''\
translate dutch block_a:
    # mc "Hello, [mcname]! {i}Welcome{/i}"
    mc "Hallo, [mcname]! {i}Welkom{/i}"

translate dutch strings:
    old "Save %s"
    new "Opslaan %s"
'''


class TranslationValidatorTests(unittest.TestCase):
    def make_files(self, target=TARGET_GOOD, reference=REFERENCE):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        target_path = root / "dutch" / "sample.rpy"
        reference_path = root / "deutsch" / "sample.rpy"
        target_path.parent.mkdir(parents=True)
        reference_path.parent.mkdir(parents=True)
        target_path.write_text(target, encoding="utf-8")
        reference_path.write_text(reference, encoding="utf-8")
        return temp, target_path, reference_path

    def test_valid_complete_file_passes(self):
        temp, target, reference = self.make_files()
        try:
            problems = MODULE.validate_target_file(target, reference, "dutch", (set(), [], set()))
        finally:
            temp.cleanup()
        self.assertEqual(problems, [])

    def test_translation_key_mismatch_is_detected(self):
        temp, target, reference = self.make_files(target=TARGET_GOOD.replace("translate dutch", "translate nl", 1))
        try:
            problems = MODULE.validate_target_file(target, reference, "dutch", (set(), [], set()))
        finally:
            temp.cleanup()
        self.assertIn("translation-key-mismatch", {item.code for item in problems})

    def test_token_loss_is_detected(self):
        changed = TARGET_GOOD.replace("Hallo, [mcname]!", "Hallo!")
        temp, target, reference = self.make_files(target=changed)
        try:
            problems = MODULE.validate_target_file(target, reference, "dutch", (set(), [], set()))
        finally:
            temp.cleanup()
        self.assertIn("token-parity", {item.code for item in problems})

    def test_speaker_change_is_detected(self):
        changed = TARGET_GOOD.replace('mc "Hallo', 'sy "Hallo')
        temp, target, reference = self.make_files(target=changed)
        try:
            problems = MODULE.validate_target_file(target, reference, "dutch", (set(), [], set()))
        finally:
            temp.cleanup()
        self.assertIn("speaker-or-code-modified", {item.code for item in problems})

    def test_identical_english_requires_allowlist(self):
        changed = TARGET_GOOD.replace("Opslaan %s", "Save %s")
        temp, target, reference = self.make_files(target=changed)
        try:
            problems = MODULE.validate_target_file(target, reference, "dutch", (set(), [], set()))
            allowed = MODULE.validate_target_file(target, reference, "dutch", ({"Save %s"}, [], set()))
        finally:
            temp.cleanup()
        self.assertIn("untranslated-identical", {item.code for item in problems})
        self.assertNotIn("untranslated-identical", {item.code for item in allowed})

    def test_missing_target_string_is_detected(self):
        blocks, problems = MODULE.parse_translation_text('translate dutch strings:\n    old "Save"\n', "sample.rpy")
        self.assertEqual(len(blocks), 1)
        self.assertIn("missing-target-string", {item.code for item in problems})

    def test_lenient_reference_mode_ignores_orphan_translator_comment(self):
        text = '''\
translate french a:
    # mc "Actual source"
    mc "Vraie traduction"

# mc "Translator note that resembles dialogue"
# Additional explanation.

translate french b:
    # mc "Next source"
    mc "Source suivante"
'''
        strict_blocks, strict_problems = MODULE.parse_translation_text(text, "sample.rpy")
        lenient_blocks, lenient_problems = MODULE.parse_translation_text(
            text, "sample.rpy", strict_missing_targets=False
        )
        self.assertIn("missing-target-string", {item.code for item in strict_problems})
        self.assertEqual(lenient_problems, [])
        self.assertEqual(sum(len(block.units) for block in lenient_blocks), 2)
        self.assertEqual(len(strict_blocks), len(lenient_blocks))

    def test_strings_target_may_have_trailing_comment(self):
        text = '''\
translate french strings:
    old "HIST"
    new "HIST"  # Historique
'''
        blocks, problems = MODULE.parse_translation_text(text, "sample.rpy")
        self.assertEqual(problems, [])
        self.assertEqual(blocks[0].units[0].source, ("HIST",))
        self.assertEqual(blocks[0].units[0].target, ("HIST",))

    def test_multiple_visible_string_literals_are_supported(self):
        reference_text = 'translate deutsch a:\n    # "BDSM Model" "Hey!"\n    "BDSM Model" "Hey!"\n'
        target_text = 'translate dutch a:\n    # "BDSM Model" "Hey!"\n    "BDSM-model" "Hé!"\n'
        temp, target, reference = self.make_files(target=target_text, reference=reference_text)
        try:
            problems = MODULE.validate_target_file(target, reference, "dutch", (set(), [], set()))
        finally:
            temp.cleanup()
        self.assertEqual(problems, [])

    def test_unescaped_extra_quote_is_detected(self):
        with self.assertRaises(ValueError):
            MODULE.extract_statement('mc "Dit is "fout""')

    def test_quoted_speaker_statement_uses_dialogue_text(self):
        source = MODULE.extract_statement('"BDSM Model" "Hey!"')
        target = MODULE.extract_statement('"BDSM-Modell" "Hallo!"')
        self.assertEqual(source, (("BDSM Model", "Hey!"), '"" ""'))
        self.assertEqual(target, (("BDSM-Modell", "Hallo!"), '"" ""'))

    def test_strings_allow_trailing_comments(self):
        blocks, problems = MODULE.parse_translation_text(
            'translate deutsch strings:\n'
            '    old "AUTO"\n'
            '    new "AUTO" # keep the standard label\n',
            "sample.rpy",
        )
        self.assertEqual(problems, [])
        self.assertEqual(blocks[0].units[0].target, ("AUTO",))

    def test_unpaired_annotated_dialogue_comment_is_ignored(self):
        blocks, problems = MODULE.parse_translation_text(
            'translate deutsch block:\n'
            '    # mc "Alternative translated line"\n'
            '    # alternate route note\n',
            "sample.rpy",
            strict_missing_targets=False,
        )
        self.assertEqual(problems, [])
        self.assertEqual(blocks[0].units, [])

    def test_format_tag_order_is_detected(self):
        changed = TARGET_GOOD.replace("{i}Welkom{/i}", "{/i}Welkom{i}")
        temp, target, reference = self.make_files(target=changed)
        try:
            problems = MODULE.validate_target_file(target, reference, "dutch", (set(), [], set()))
        finally:
            temp.cleanup()
        codes = {item.code for item in problems}
        self.assertIn("format-tag-order", codes)
        self.assertIn("format-tag-balance", codes)


if __name__ == "__main__":
    unittest.main()
