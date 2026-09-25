# Phase 0 baseline and inventory method

## Baseline

- **Upstream repository:** `vinovella/FL-SM-1-translations`
- **Pinned upstream content SHA:** `cbb9016479fa95aca7c6ad58593fdf63093d7659`
- **Fork Phase 0 base SHA:** `c6c9e8e587619e42190963a2077e9b29ded0d1f2`
- **Target language variant:** Netherlands Dutch (`nl-NL`)
- **Proposed display name:** `Nederlands` (maintainer confirmation pending)
- **Proposed Ren'Py language key:** `dutch` (maintainer confirmation pending)

The fork Phase 0 base is the merge commit for the approved implementation-plan PR. Its first parent is the pinned upstream SHA, while its second parent contains only the approved planning document. Therefore the translation content used for this inventory still corresponds to upstream `cbb9016479fa95aca7c6ad58593fdf63093d7659`.

## Production language roots represented at the baseline

The manifest generator uses the union of editable `.rpy` paths from these production translation roots:

- `chinese/`
- `deutsch/`
- `french/`
- `italian/`
- `magyar/`
- `portuguese/`
- `spanish/`
- `turkish/`
- `ukrainian/`

`WIP/` is not treated as an additional production language root because it contains work-in-progress copies of language trees already represented above. Generated `.rpyc` files are excluded completely.

## Why the manifest uses a union instead of one language

No existing target-language directory is assumed to be a perfect structural authority. A file that is absent from German but present in Italian, for example, is still a candidate Dutch file.

For every normalized path, the generator:

1. Finds the file in every configured production language tree.
2. Parses the embedded English source-side translation comments and `old` strings.
3. Chooses the available file with the greatest source string/dialogue coverage as the count reference.
4. Uses the configured language preference order to break ties.
5. Records all language roots in which the path is present.
6. Flags structural variance when available language copies disagree on translation-block or source-unit counts.

This makes the inventory conservative: it prefers the representation exposing the most source text rather than silently inheriting an incomplete target translation.

## Count definitions

### Translation block count

Number of Ren'Py declarations matching `translate <language> <block>:` including `translate <language> strings:` blocks.

### String/dialogue count

Number of source-visible translation units found inside translation blocks:

- source dialogue/narration/menu lines stored in generated `# ... "English text"` comments; plus
- `old "English text"` entries inside `translate <language> strings:` blocks.

The number is an inventory metric, not a claim about linguistic complexity.

### Source word estimate

An approximate word count derived from the embedded English source strings. Ren'Py formatting tags, interpolation placeholders and percent-format tokens are removed before counting. The estimate is intended for planning and PR sizing, not billing or translation-memory accounting.

## Phase assignment rules

| Path | Phase |
| --- | --- |
| `common.rpy` | Phase 2 |
| `code/hints.rpy` | Phase 2 |
| `code/renpy/**` | Phase 2 |
| `code/classes/**` | Phase 2 |
| `code/functions/**` | Phase 2 |
| `code/debug/**` | Phase 2 |
| `code/data/**` | Phase 3 |
| `code/live_chat/**` | Phase 3 |
| `code/minigames/**` | Phase 3 |
| `code/scenes/main_story/**` | Phase 4 |
| `code/scenes/character_scenes/**` | Phase 5 |
| `code/scenes/cross_characters/**` | Phase 5 |
| `code/scenes/it_office/**` | Phase 6 |
| `code/scenes/theatre/**` | Phase 6 |
| `code/scenes/movies/**` | Phase 6 |

Anything outside these rules is marked `Unassigned` and causes the generator to fail. That is intentional. A new upstream category should be consciously classified rather than quietly dropped into whatever bucket looked lonely.

## Status handling

Every new candidate path starts as `not started`. If the manifest already exists, valid existing status values and manual notes are preserved when the manifest is regenerated. The accepted statuses are:

- `not started`
- `in progress`
- `review`
- `done`

The baseline SHA remains pinned for Phase 0. Later phases should deliberately update the baseline only after upstream reconciliation.
