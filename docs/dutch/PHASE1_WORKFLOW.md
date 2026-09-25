# Phase 1 translation workflow

Phase 1 establishes repeatable Dutch translation validation and tracking without bulk-committing untranslated English copies.

## Current language-contract gate

The merged Phase 0 repository still records the Ren'Py key/display-name and storefront decisions as pending maintainer confirmation. Phase 1 therefore adds tooling and review scaffolding, but it does not create Dutch runtime `.rpy` files. If a Dutch `.rpy` file is added before the language key is marked `confirmed` in `phase0-config.json`, repository validation fails deliberately.

## Local quality command sequence

Run these commands from the repository root before pushing a Dutch implementation branch:

```bash
python -m unittest discover -s tests -p 'test_dutch_*.py' -v
python tools/dutch_phase0_inventory.py --check
python tools/dutch_source_snapshot.py --check
python tools/dutch_progress_report.py --check
python tools/dutch_translation_validate.py
git diff --check
```

When source tracking files need regeneration:

```bash
python tools/dutch_phase0_inventory.py --write
python tools/dutch_source_snapshot.py --write
python tools/dutch_progress_report.py --write
```

## Validator coverage

`tools/dutch_translation_validate.py` checks every committed Dutch `.rpy` file against the manifest-selected reference language file. It rejects:

- a Ren'Py translation key different from the configured Dutch key;
- missing, reordered or modified translation block identifiers;
- missing target strings;
- changed speaker codes or other non-translatable statement syntax;
- placeholder, interpolation, printf-token or escape-sequence mismatches;
- changed Ren'Py formatting-tag sequences or malformed paired tags;
- malformed or improperly escaped quoted strings;
- source-side English comments/`old` strings that no longer match the reference file;
- target strings that remain identical to English unless covered by the approved allowlist/glossary policy;
- Dutch `.rpy` files that are not represented in the manifest;
- compiled `.rpyc` files in the Dutch tree.

Validation is file-complete by design. A partially translated `.rpy` file does not pass merely because the edited lines are valid.

## Source change detection

`tools/dutch_source_snapshot.py` generates `SOURCE_CONTENT_SNAPSHOT.csv`. Each manifest path receives a SHA-256 fingerprint derived from its translation block identifiers, source statement shape and embedded English source text.

The combination of:

```bash
python tools/dutch_phase0_inventory.py --check
python tools/dutch_source_snapshot.py --check
```

therefore detects both newly introduced/removed candidate paths and source-content changes that keep the same number of strings or words.

## Progress tracking

`tools/dutch_progress_report.py` generates `TRANSLATION_PROGRESS.md` from the Phase 0 manifest. The manifest remains the authoritative place for per-file workflow status:

```text
not started
in progress
review
done
```

A file should only be marked `done` after translation validation, Dutch language review and the applicable smoke test have passed.

## CI behavior

`.github/workflows/dutch-translation-quality.yml` runs on `nl/**` pushes and relevant pull requests. On implementation-branch pushes it refreshes the generated source snapshot and progress report. On pull requests it runs them in check-only mode, so stale generated tracking files fail CI rather than being silently changed during review.
