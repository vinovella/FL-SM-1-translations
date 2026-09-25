## Dutch localization scope

- Phase:
- Batch:
- Files translated:

## Manifest updates

- [ ] Every touched file has the correct manifest status.
- [ ] No unrelated file status was changed.

## Language consistency

- [ ] Glossary/style-guide decisions were followed.
- [ ] New recurring terminology was added to `DUTCH_GLOSSARY.csv` where needed.
- [ ] Identical English/Dutch strings are covered by the approved allowlist.

## Validation

- [ ] `python -m unittest discover -s tests -p 'test_dutch_*.py' -v`
- [ ] `python tools/dutch_phase0_inventory.py --check`
- [ ] `python tools/dutch_source_snapshot.py --check`
- [ ] `python tools/dutch_progress_report.py --check`
- [ ] `python tools/dutch_translation_validate.py`
- [ ] `git diff --check`

## Review and runtime evidence

- [ ] Dutch language review completed.
- [ ] In-game smoke test completed, or the unavailable compatible build is documented below.

### Smoke-test notes

<!-- Record build/version and tested screens/scenes, or explain why an in-game test was not available. -->
