# Netherlands-Dutch localization style guide

## 1. Language target

- Translate to natural contemporary Netherlands Dutch (`nl-NL`).
- Prefer idiomatic spoken Dutch over English sentence structure copied word-for-word.
- Do not introduce Flemish-specific vocabulary unless the source context intentionally calls for it.
- Preserve the source meaning, humor, awkwardness, intimacy and explicitness. Localization is not a surprise morality committee.

## 2. Source authority

Translate from the embedded English source text in each Ren'Py translation block.

Existing German, Italian, French or other target translations may be consulted for file structure or context, but they are not linguistic source material. If another language conflicts with the English source, follow the English source.

## 3. Ren'Py safety rules

The following are code tokens, not translatable prose. Preserve them exactly:

- square-bracket substitutions such as `[mcname]`
- formatting/action tags such as `{i}`, `{/i}`, `{b}`, `{/b}`, `{w}` and `{w=0.5}`
- percent formatting such as `%s`, `%(count)d`, `%.2f` and literal `%%`
- escape sequences such as `\n`, `\t` and `\r`
- speaker codes, translation block identifiers, labels, variable names and function names

Keep the same number of placeholders and tags as the source. Tags may move only when Dutch grammar requires a different logical position.

Use escaped straight quotation marks inside Ren'Py string literals where required. Do not replace source-code delimiters with typographic smart quotes.

Do not translate source comments or source-side `old` entries. Only target-visible strings are translation content.

## 4. Character names and role labels

Proper names remain unchanged unless the maintainers explicitly establish another policy. This includes names such as Stacy, Kanya, Lyssa, Taisia and Denise.

Player-selected names remain placeholders, for example `[mcname]`.

Generic role labels are translated when visible to the player. Examples from the repository character context include:

- `Narrator` -> `Verteller` when a visible label actually exists
- `Creepy Guy` -> `Enge man`
- `Dog Walker` -> `Hondenuitlater`
- `Jogger` -> `Hardloper`
- `Carnival Worker` -> `Kermismedewerker`
- `Waiter` -> `Ober`
- `BDSM Model` -> `BDSM-model`

Honorifics are localized when they are part of the visible name: `Mr.` -> `meneer`, `Mrs.` -> `mevrouw`. Do not alter the surname.

## 5. Forms of address

Default to natural informal Dutch (`je/jij/jouw`) in ordinary peer conversation.

Use `u/uw` only when source context clearly communicates formality, professional distance, age/status deference or a deliberately formal character voice. Keep the choice consistent within a scene unless the relationship itself changes.

Do not mechanically translate English `you` as one fixed Dutch form. Dutch forces a social choice that English often leaves pleasantly ambiguous.

## 6. Character voice

Character-specific tone takes priority over literal wording.

- Keep confident characters confident.
- Keep awkward characters awkward without making the Dutch grammatically broken unless the source is intentionally broken.
- Preserve sarcasm, teasing and recurring jokes.
- Preserve gender/pronoun context from `.github/copilot-instructions.md`.
- Preserve nicknames and recurring forms of address consistently across main-story and optional scenes.

When a line has insufficient context for a gendered or relationship-sensitive Dutch choice, flag it for review instead of inventing certainty.

## 7. Profanity and explicit content

Preserve the source register and intensity. Do not sanitize sexual, BDSM or profane dialogue and do not make a neutral source line more explicit.

There is no universal one-word mapping for English profanity. Translate by function:

- exclamation/intensifier
- insult
- sexual verb
- anatomical slang
- affectionate/teasing profanity

Terms such as `fuck`, `dick`, `pussy`, `bitch` and similar words are therefore context-sensitive. Choose Dutch wording that matches the speaker and scene, then record recurring character-specific decisions in the glossary.

For neutral terminology, prefer established Dutch forms such as `seks`, `porno`, `orgasme`, `toestemming` and `stopwoord`. For deliberately crude dialogue, use equally direct Dutch rather than clinical wording.

## 8. BDSM terminology

Use established terminology consistently:

- `BDSM` remains `BDSM`
- `bondage` remains `bondage`
- `dominant` remains `dominant` as a role/noun where natural
- `submissive` may be `sub` as a role/noun and `onderdanig` as an adjective, depending on context
- `safe word` -> `stopwoord`
- `consent` -> `toestemming` / `instemming` according to sentence context

Do not expand abbreviations or add explanations inside dialogue unless the English source does so.

## 9. Studio, business and production terminology

Prefer concise, natural terms used in Dutch work/production contexts:

- `studio` -> `studio`
- `filming` -> `opnames`
- `shoot` (noun) -> `opname` or `draaidag`, depending on context
- `director` -> `regisseur`
- `sound person` -> `geluidsmedewerker`
- `rent` -> `huur`
- `weekly rent` -> `weekhuur`
- `revenue` -> `omzet`
- `profit` -> `winst`
- `expenses` -> `kosten`
- `budget` -> `budget`

`S&M Studio` is a proper project/studio name and remains unchanged.

## 10. IT terminology

Use Dutch where a stable Dutch UI/workplace term exists, but do not translate brands, protocols or acronyms merely to prove enthusiasm.

Preferred baseline terms include:

- `IT Office` -> `IT-kantoor`
- `email` -> `e-mail`
- `password` -> `wachtwoord`
- `server` -> `server`
- `software` -> `software`
- `USB` remains `USB`

## 11. UI terminology

Prefer short, familiar Netherlands-Dutch interface labels. Initial baseline choices:

- `Save` -> `Opslaan`
- `Load` -> `Laden`
- `Back` -> `Terug`
- `Preferences` -> `Voorkeuren`
- `History` -> `Geschiedenis`
- `Enable` -> `Inschakelen`
- `Disable` -> `Uitschakelen`
- `Reset` -> `Resetten`
- `Accessibility Menu` -> `Toegankelijkheidsmenu`

UI strings must also be reviewed in-game for clipping. A linguistically gorgeous label that lives three centimeters outside the button is still a bug.

## 12. Intentional foreign-language dialogue

Foreign-language switches are authored characterization and must not be flattened automatically.

When the English/source scene intentionally contains Dutch already, preserve the exact authored Dutch wording unless a maintainer explicitly asks for correction. Examples known from existing translation work include `Lekker`, `Oprotten`, `Vreselijk`, `pannenkoek`/`pannekoek`, `Kuts` and `helaas, pindakaas`.

If a character intentionally speaks Polish or another non-English language, preserve that language unless the source explicitly provides a translation or the maintainers define another policy.

Record recurring intentional foreign phrases in the unchanged-string allowlist.

## 13. Sound effects and action text

Translate lexical action descriptions when that sounds natural in Dutch, for example `*laughing*` may become `*lacht*` or `*gelach*` depending on the established scene style.

Do not force translation of non-lexical vocalizations such as `Mmm`, `Ahh` or invented noises when there is no meaningful Dutch equivalent. Preserve punctuation and Ren'Py tags around them.

## 14. Punctuation and typography

- Preserve purposeful ellipses, repeated punctuation and pauses when they carry timing or character voice.
- Use Dutch punctuation around translated prose where it does not affect engine syntax.
- Keep code-level quotes and escapes valid.
- Do not normalize unusual capitalization if it represents shouting, a UI convention or a deliberate source effect.

## 15. Review rules

A translated file is ready for Dutch-language review only when every target-visible string in that file is translated or explicitly allowlisted.

Reviewers should check:

1. meaning and scene context
2. character voice and forms of address
3. glossary consistency
4. explicit/profanity register
5. intentional foreign phrases
6. placeholders, tags and escaped quotes
7. UI length where applicable

Any new recurring terminology decision should be added to `DUTCH_GLOSSARY.csv` rather than being rediscovered file by file for the rest of eternity.
