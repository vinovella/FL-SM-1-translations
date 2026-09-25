# Phase 0 external confirmations

Two project decisions cannot be proven from the translation repository alone. They require explicit confirmation from an SM-1 maintainer before Phase 0 can be marked complete.

## Decision 1 - Dutch Ren'Py language identifier and display name

**Status:** Pending maintainer confirmation  
**Proposed runtime key:** `dutch`  
**Proposed displayed name:** `Nederlands`  
**Language variant:** `nl-NL`

### Repository evidence

Existing translations use a language-specific root directory and the same language identifier in Ren'Py translation declarations, for example the German tree uses `deutsch/` and `translate deutsch ...` declarations. There is currently no Dutch root and no repository-owned language registration file that proves the identifier expected by the game runtime.

### Confirmation required

A maintainer should explicitly confirm:

> For the SM-1 Dutch localization, should the Ren'Py translation identifier/root directory be `dutch`, and should the language be displayed to players as `Nederlands`?

If the runtime key differs, update `phase0-config.json` before Phase 1 creates any Dutch `.rpy` files.

## Decision 2 - Dutch store-page metadata

**Status:** Pending maintainer confirmation  
**Proposed scope:** Include Dutch storefront metadata  
**Proposed filename if confirmed:** `storepage_896318_dutch.json`

### Repository evidence

Production language trees such as German and Italian contain language-specific `storepage_896318_<language>.json` files alongside `common.rpy` and the `code/` tree. This strongly suggests storefront metadata is maintained through the translation repository, but it does not prove that a Dutch store page is enabled or consumed by the release process.

### Confirmation required

A maintainer should explicitly confirm:

> Should the Dutch localization include Steam/storefront metadata in this repository, using a Dutch equivalent of the existing `storepage_896318_<language>.json` files? If yes, please confirm the expected filename/language identifier.

## Ready-to-post maintainer request

```text
We are preparing the Netherlands-Dutch (nl-NL) localization for SM-1 and need two Phase 0 confirmations before creating the translation tree:

1. Should the Ren'Py language identifier/root directory be `dutch`, with the player-facing language name `Nederlands`?
2. Should Dutch also include the repository's store-page metadata (`storepage_896318_<language>.json`)? If yes, is `storepage_896318_dutch.json` the expected filename?

No Dutch runtime files will be created until these identifiers are confirmed.
```

## Completion rule

Do not change either status to `confirmed` merely because the proposed values look conventional. Record the maintainer response or link in this document and in the Phase 0 PR before declaring Phase 0 complete.
