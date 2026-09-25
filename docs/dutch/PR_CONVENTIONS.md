# Dutch translation branch and PR conventions

## Branch names

Use the implementation-plan naming scheme:

```text
nl/phase-02-system-ui-01
nl/phase-03-gameplay-data-01
nl/phase-04-main-story-01
nl/phase-05-character-scenes-01
nl/phase-06-specialized-content-01
nl/phase-07-completion-qa
```

For additional bounded batches, increment the final two-digit sequence rather than creating one enormous phase branch.

Phase 1 itself uses:

```text
nl/phase-01-tooling-scaffolding
```

## Scope rules

- Translate complete `.rpy` files, not scattered lines across many files.
- Do not add English-copy Dutch skeleton files.
- Do not modify source-side comments, `old` strings, speaker identifiers, block identifiers, variables or Ren'Py tokens.
- Never commit Dutch `.rpyc` files.
- Update `DUTCH_GLOSSARY.csv` when a recurring term or character-specific decision is introduced.
- Update the manifest status for every file touched by the PR.
- Keep a PR bounded enough for a reviewer to read the Dutch text and its context rather than merely trusting green automation. Humanity has already invented enough ways to approve 30,000-line diffs without reading them.

## Status transitions

```text
not started -> in progress -> review -> done
```

`done` means the complete file has passed automated validation, language review and the applicable smoke test. Do not use `done` as a synonym for "the translator stopped typing".

## Required PR evidence

Every Dutch translation PR should state:

1. implementation phase and file batch;
2. translated files and manifest status changes;
3. glossary/allowlist changes, if any;
4. automated validation result;
5. Dutch language-review result;
6. in-game smoke-test result, or a clear explanation that no compatible build was available;
7. any intentionally unchanged English strings and the allowlist rule that permits them.

## Review rule

Automation protects syntax and structural parity. It does not approve Dutch prose. A human language review remains required before translated files are marked `done`.
