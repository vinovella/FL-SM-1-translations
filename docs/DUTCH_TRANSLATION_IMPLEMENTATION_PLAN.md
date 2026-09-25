# Dutch translation implementation plan for FL-SM-1

**Status:** Proposed implementation plan  
**Baseline date:** 2026-09-08  
**Repository baseline:** `master` at `cbb9016479fa95aca7c6ad58593fdf63093d7659`  
**Upstream baseline:** `vinovella/FL-SM-1-translations` is at the same commit at the time this plan was written.

## 1. Objective

Deliver a complete, maintainable Dutch localization of all user-visible SM-1 game text represented by this translation repository, while preserving Ren'Py syntax, game logic, placeholders, character identity and the tone of the original dialogue.

The implementation must be reviewable in phases. A phase is only complete when its files are fully translated and pass both structural validation and language review.

## 2. Current repository state

At this baseline:

- There is no root `dutch/` translation directory yet.
- Existing language trees show the expected localization shape, including:
  - `common.rpy`
  - `code/classes/`
  - `code/data/`
  - `code/debug/`
  - `code/functions/`
  - `code/hints.rpy`
  - `code/live_chat/`
  - `code/minigames/`
  - `code/renpy/`
  - `code/scenes/`
- `code/scenes/` is split into:
  - `character_scenes/`
  - `cross_characters/`
  - `it_office/`
  - `main_story/`
  - `movies/`
  - `theatre/`
- `code/data/` contains player-facing data such as characters, chat, constants, gallery text, interaction options, quests and quick interactions.
- `code/renpy/` contains configuration, labels and screens.
- Existing language directories contain both `.rpy` and generated `.rpyc` files. Only editable localization source files are translation targets; generated `.rpyc` files must not be hand-edited.
- `.github/copilot-instructions.md` already defines repository-wide translation safety rules and character context.

## 3. Scope

### In scope

- All translatable user-visible strings in Dutch `.rpy` files.
- Dialogue and narration.
- Menu choices and interaction options.
- Main story and optional/branching scenes.
- Character scenes and cross-character scenes.
- Theatre, IT office and movie content.
- Live chat and minigame text.
- Quest, gallery, hint and other gameplay-facing text.
- Ren'Py/common system and accessibility text included by this repository.
- Any other user-visible strings discovered by the inventory process.
- Dutch storefront metadata only if the project confirms that a Dutch equivalent of the existing `storepage_896318_*` JSON files is consumed by the release process.

### Out of scope

- Compiled `.rpyc` files.
- Code logic, variable names, labels, function names or speaker identifiers.
- Source comments and source-reference lines.
- Media assets unless a separate text-in-image localization requirement is confirmed.
- Repository documentation that is not displayed in SM-1.

## 4. Translation rules and guardrails

These rules apply to every phase.

1. **Confirm the Ren'Py locale identifier before creating the Dutch tree.** The human-facing language should be `Nederlands`, but the runtime translation key must be confirmed with the game maintainers instead of assuming that it is `dutch`.
2. **Translate from the embedded English source text, not from another target language.** Existing languages may be used to discover paths and translation block structure, not as linguistic source material.
3. **Never modify translation block identifiers, speaker codes or code structure.**
4. **Never modify placeholders or engine tokens.** Preserve their spelling, count and syntax exactly, including examples such as:
   - `[mcname]`
   - `{i}` and `{/i}`
   - `{b}` and `{/b}`
   - `{w}` and `{w=0.5}`
   - `%(count)d`, `%s`, `%.2f`
   - `%%`
   - `\n`, `\t`, `\r`
5. **Preserve escaped quotes correctly.** A malformed quote can invalidate an entire Ren'Py file.
6. **Do not translate source comments or lines that are explicitly source-side `old` values.** Translate only the corresponding target string.
7. **Preserve character names unless the project explicitly defines a localized role label.** Proper names should remain stable across the game.
8. **Match the source tone and explicitness.** Do not censor, soften or intensify dialogue merely because the target language is Dutch.
9. **Use natural contemporary Netherlands Dutch (`nl-NL`).** Avoid literal English sentence structure and avoid Flemish-specific wording unless character context requires it.
10. **Treat intentional foreign-language dialogue as authored content.** Do not blindly translate Polish, Dutch or other language switches embedded for character flavor. When the intentional foreign language is already Dutch, keep the intended wording/style and record the decision in the glossary rather than replacing it with another language.
11. **Keep formatting tags in the same logical position.** Their exact tokens must remain unchanged even if surrounding Dutch grammar is reordered.
12. **One file is either complete or not complete.** Do not present partially translated files as finished.

## 5. Working model

Each implementation phase should use the same cycle:

1. Rebase or synchronize the fork with the latest upstream `master`.
2. Regenerate the translation inventory and detect newly added or changed source blocks.
3. Select a bounded set of files from the phase.
4. Translate complete files.
5. Run automated token/syntax/completeness checks.
6. Perform a Dutch language review.
7. Perform an in-game smoke test where a compatible game build is available.
8. Merge the phase PR into the fork only after all phase acceptance criteria are met.
9. Prepare a clean upstream PR from the completed phase or a reviewable subset of it.

Do not submit a huge English-copy Dutch skeleton upstream. New Dutch `.rpy` files should be submitted when they contain real, complete Dutch translations.

## 6. Phase 0 - Baseline, inventory and language contract

### Goal

Remove ambiguity before translating thousands of strings.

### Tasks

- Confirm the runtime locale key and displayed language name with the SM-1 maintainers.
- Confirm whether Dutch storefront JSON is part of the requested localization deliverable.
- Build a manifest of every translatable `.rpy` path represented by the current repository.
- Record per file:
  - relative path
  - translation block count
  - string/dialogue count
  - source word estimate
  - phase assignment
  - status: `not started`, `in progress`, `review`, `done`
  - source/upstream baseline SHA
- Create a Dutch glossary and style guide covering:
  - character names
  - recurring locations
  - studio/business vocabulary
  - sexual/BDSM terminology
  - UI terminology
  - honorifics and forms of address
  - profanity/register
  - intentional foreign-language expressions
- Define a small allowlist for strings that may legitimately remain identical to English, such as proper names, acronyms, sound effects or technical terms.

### Exit criteria

- Runtime locale identifier confirmed.
- 100% of candidate `.rpy` files are present in the manifest.
- No unassigned file categories remain.
- Initial glossary and exception policy are documented.

## 7. Phase 1 - Translation tooling and Dutch project scaffolding

### Goal

Create a safe translation workflow before large-scale content changes begin.

### Tasks

- Add Dutch translation tracking files without bulk-committing untranslated English copies.
- Add or prepare validation tooling that checks:
  - translation-key consistency
  - placeholder/token parity
  - opening/closing Ren'Py formatting tags
  - escaped quotation marks
  - malformed strings
  - missing target strings
  - accidental modification of speaker codes or block identifiers
  - accidentally committed `.rpyc` files
  - target strings that are still identical to English and are not allowlisted
- Generate a machine-readable or Markdown progress report from the manifest.
- Establish branch/PR naming and review conventions.

### Suggested implementation PR convention

- `nl/phase-02-system-ui-01`
- `nl/phase-03-gameplay-data-01`
- `nl/phase-04-main-story-01`
- `nl/phase-05-character-scenes-01`
- `nl/phase-06-specialized-content-01`
- `nl/phase-07-completion-qa`

### Exit criteria

- Validation can be run repeatably.
- The manifest can identify untranslated or newly introduced source content.
- The first translated file can be added without manually auditing every token by eye.

## 8. Phase 2 - System UI, common text and hints

### Primary scope

- `common.rpy`
- `code/renpy/config/`
- `code/renpy/labels/`
- `code/renpy/screens/`
- `code/hints.rpy`
- Any user-visible strings in `code/classes/`, `code/functions/` and `code/debug/`

### Priority

High. These strings are encountered throughout the game and establish terminology used by later phases.

### Review focus

- Accessibility terminology.
- Save/load/preferences terminology.
- Buttons, labels and status messages.
- Consistent capitalization.
- UI length and clipping.
- Technical terms that should remain English versus terms that should be localized.

### Exit criteria

- All user-visible system/UI strings in scope are Dutch.
- No token-parity errors.
- Main menu/settings/accessibility smoke test passes where runtime testing is possible.

## 9. Phase 3 - Gameplay data, interactions, live chat and minigames

### Primary scope

- `code/data/characters/`
- `code/data/chat/`
- `code/data/constants/`
- `code/data/gallery/`
- `code/data/interaction_options/`
- `code/data/quests/`
- `code/data/quick_interactions/`
- `code/live_chat/`
- `code/minigames/`

### Review focus

- Short strings with limited context.
- Quest terminology and state text.
- Repeated interaction lines.
- Chat tone and internet-style language.
- Consistent character voice in quick interactions.
- Compact phrasing where screen space is limited.

### Exit criteria

- All gameplay-data and interaction strings in scope are Dutch.
- Quick-interaction and chat files contain no unreviewed English duplicates outside the allowlist.
- Cross-file recurring terminology matches the glossary.

## 10. Phase 4 - Main story

### Primary scope

- `code/scenes/main_story/`

### Translation strategy

- Prefer story order for context and continuity.
- Keep each file complete before moving it to review.
- Split implementation into multiple PRs rather than one enormous main-story PR.
- A practical PR should contain one large scene or a coherent group of smaller scenes, not an arbitrary mixture of unrelated files.

### Review focus

- Character voice and relationship continuity.
- Pronouns and forms of address.
- Humor, idiom and emotional tone.
- Choice text matching the consequence/context of the choice.
- Consistency with terms already established in Phases 2 and 3.

### Exit criteria

- Every main-story file in the manifest is `done`.
- Native-language review has covered the complete main-story path.
- No known untranslated English dialogue remains outside the allowlist.

## 11. Phase 5 - Character and cross-character scenes

### Primary scope

- `code/scenes/character_scenes/`
- `code/scenes/cross_characters/`

### Translation strategy

Group work by character where possible. This makes it easier to keep one character's vocabulary, speech patterns, profanity and recurring jokes consistent.

### Review focus

- Per-character voice.
- Gender/pronoun accuracy based on repository character context.
- Character-specific terminology and nicknames.
- Continuity between a character's main-story and optional scenes.
- Intentional foreign phrases and recurring verbal habits.

### Exit criteria

- Every character/cross-character file in the manifest is `done`.
- Character glossary has been updated with decisions discovered during translation.
- Reviewer spot checks confirm that recurring characters sound consistent across files.

## 12. Phase 6 - Specialized scene content

### Primary scope

- `code/scenes/it_office/`
- `code/scenes/theatre/`
- `code/scenes/movies/`

### Review focus

- Workplace/technical vocabulary in IT-office scenes.
- Theatre terminology and character-specific stage language.
- Movie-production vocabulary.
- Scene-specific explicit terminology.
- Menu choices and route-dependent dialogue.

### Exit criteria

- All specialized-scene files are `done`.
- No phase-specific vocabulary conflicts with the glossary.
- Route/scene smoke tests pass where available.

## 13. Phase 7 - Completion sweep, QA and release readiness

### Goal

Prove that "all text" really means all text, rather than "all files somebody remembered to open".

### Automated checks

- Compare the Dutch file manifest with the current upstream translation-file manifest.
- Verify every expected Dutch `.rpy` file exists.
- Verify every expected translation block/string exists.
- Verify placeholder/token multisets match source strings.
- Verify formatting tags are balanced.
- Verify there are no accidental references to another target language key.
- Verify no `.rpyc` files were edited as translation source.
- Report target text identical to English, excluding the explicit allowlist.
- Report files added or changed upstream since the phase baseline.

### Human checks

- Native Dutch proofreading.
- Main menu, preferences, accessibility and save/load screens.
- New game opening sequence.
- Representative main-story scenes.
- Representative scenes for every major character.
- Theatre, IT office and movie routes.
- Live chat, quests, quick interactions and minigames.
- Text overflow/clipping and punctuation.
- Consistency of explicit vocabulary and character voice.

### Storefront metadata

If Dutch store-page metadata is confirmed as part of the release process, create and review the Dutch equivalent only after in-game terminology is stable so product descriptions use the same naming conventions.

### Exit criteria

- 100% manifest coverage.
- 0 unresolved token/syntax errors.
- 0 unexplained untranslated English strings.
- 0 unreviewed files.
- Upstream delta is reconciled against the latest `master`.
- Final Dutch smoke test passes on a compatible SM-1 build.

## 14. Pull-request strategy

### This PR

Documentation only. It establishes the implementation plan and does not claim that Dutch translation work is complete.

### Translation PRs

Each subsequent PR should include:

- exact phase and file scope
- files completed
- files intentionally deferred
- validation summary
- glossary decisions introduced by the PR
- any intentionally untranslated strings and why
- upstream baseline SHA used for the work

Avoid giant cross-repository translation dumps. Smaller coherent PRs are easier to review, easier to correct and less likely to rot while upstream keeps changing.

## 15. Definition of done for a translated file

A Dutch translation file is `done` only when all of the following are true:

- Every user-visible target string in the file has been translated or explicitly allowlisted.
- No translation block is partially completed.
- Placeholders and Ren'Py tags match the source.
- Escaped quotes and syntax are valid.
- Speaker codes and block identifiers are unchanged.
- Character names and terminology follow the glossary.
- The file has received Dutch-language review.
- The file passes automated validation.

## 16. Definition of done for the complete Dutch localization

The Dutch localization is complete when:

1. Every translatable SM-1 file in the current upstream manifest has a completed Dutch equivalent.
2. All translatable user-visible strings are Dutch or have an explicit, documented reason to remain unchanged.
3. Automated structural/token validation is clean.
4. Native-language review is complete.
5. Runtime smoke testing is complete on representative routes and UI surfaces.
6. The translation is rebased/reconciled against the latest upstream translation baseline.
7. Any confirmed Dutch storefront metadata is complete and terminology-aligned.

## 17. Upstream maintenance after initial completion

Dutch should not become a one-time translation snapshot.

After the initial release:

- Check upstream regularly for new or changed `.rpy` translation blocks.
- Regenerate the manifest after every upstream update.
- Treat newly introduced strings as a small maintenance phase.
- Keep glossary decisions under version control.
- Submit maintenance PRs in small batches so Dutch does not drift behind SM-1 releases.

This turns Dutch localization from a heroic one-off effort into a boring repeatable process, which is exactly what localization maintenance should be.
