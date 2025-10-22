## Copilot translation instructions

## Key Guidelines

1. NEVER change or translate placeholders, variables, engine tags, escape sequences, or hotkey markers. Treat them as code tokens, not words. Examples of tokens you must preserve exactly: anything that looks like a placeholder or engine tag.
    - Curly-brace placeholders: `{player_name}`, `{score}`, `{w=0.5}`, `{i}`, `{b}` (engine text tags)
    - Square-bracket substitutions: `[player_name]`, which may be used for python/engine interpolation
    - Percent-based formatting: `%(count)d`, `%.2f`, `%s`
    - Line/escape sequences: `\n`, `\t`, `\r`
    - Any text that is outside quotation marks in code files like - `nointeract`, `who_style`, etc.

2. Preserve punctuation and whitespace that are part of tokens.
    - If a placeholder appears adjacent to punctuation or parentheses, keep the punctuation in the translated string as it appears in the source, unless grammar of the target language strictly requires reordering — in that case, keep the token exactly but move its surrounding punctuation/words.

3. Maintain the order and count of placeholders. If the target grammar requires reordering, use numbered placeholders when available (e.g., `%1$s` or similar) — but only if the original uses them. Do not invent a new placeholder format.

4. Preserve comments and code structure. Only edit the visible strings for translation. Do not modify code logic, variable names, or function calls.

5. Keep tone and register appropriate for the character/context provided. When context indicates a character's gender, age, or specialty, use natural language choices consistent with that context (see Character & Context section below).

6. Context for characters and their gender and speciality is provided here:
    CODE: mc        NAME: `[mcname]`     GENDER: Male               INFO: Main Character          SPECIALTY: Player can name the character, but gender is fixed
    CODE: mct       NAME: `[mcname]`     GENDER: Male               INFO: Main Character thinking SPECIALTY: Player can name the character, but gender is fixed
    CODE: mcd       NAME: `[mcname]`     GENDER: Male               INFO: Main Character          SPECIALTY: Player can name the character, but gender is fixed
    CODE: mo        NAME: `You`          GENDER: Male               INFO: Main Character          SPECIALTY: Player can name the character, but gender is fixed
    CODE: arj       NAME: `Amber-Rose`   GENDER: Female             INFO: Amber-Rose Jenkins
    CODE: bg        NAME: `Amore`        GENDER: Female             INFO: BDSM Model Amore
    CODE: dc        NAME: `Debbie`       GENDER: Female             INFO: Debbie Callahan         SPECIALTY: Trans character (has a penis). Identifies as She/Her.
    CODE: kv        NAME: `Kanya`        GENDER: Female             INFO: Kanya Vu
    CODE: mes       NAME: `Min`          GENDER: Female             INFO: Min Eun-Soo
    CODE: mh        NAME: `Lyssa`        GENDER: Female             INFO: Melissa Harris (Lyssa)  SPECIALTY: Trans character (has a penis). Identifies as She/Her.
    CODE: my        NAME: `Melony`       GENDER: Female             INFO: Melony Young
    CODE: sy        NAME: `Stacy`        GENDER: Female             INFO: Stacy Young
    CODE: atp       NAME: `Angela`       GENDER: Female             INFO: Angela Taylor Portillo
    CODE: be        NAME: `Bently`       GENDER: Female             INFO: Bently (Taisia's coworker clown)
    CODE: cg        NAME: `Creepy Guy`   GENDER: Male               INFO: Creepy Guy (Not named)
    CODE: cs        NAME: `Cecilia`      GENDER: Female             INFO: Cecilia Siegal
    CODE: dw        NAME: `Dog Walker`   GENDER: Female             INFO: Dog Walker
    CODE: ed        NAME: `Elizabeth`    GENDER: Female             INFO: Elizabeth Davis
    CODE: hr        NAME: `Hana`         GENDER: Female             INFO: Hana Rivera
    CODE: ic        NAME: `Inga`         GENDER: Female             INFO: Inga Cowen
    CODE: jg        NAME: `Juggsy`       GENDER: Male               INFO: Juggsy (Taisia's coworker clown)
    CODE: ka        NAME: `Kennedy`      GENDER: Female             INFO: Kennedy Assworth
    CODE: lg        NAME: `Lauren`       GENDER: Female             INFO: Lauren Grindsly
    CODE: nj        NAME: `Jogger`       GENDER: Female             INFO: Nelly
    CODE: ols       NAME: `Olivia`       GENDER: Female             INFO: Olivia Small
    CODE: rd        NAME: `Ridley`       GENDER: Female             INFO: Ridley Driver
    CODE: zh        NAME: `Zuzana`       GENDER: Female             INFO: Zuzana Holab
    CODE: ag        NAME: `Anna`         GENDER: Female             INFO: Anna Goodwin
    CODE: am        NAME: `April`        GENDER: Female             INFO: April
    CODE: cw        NAME: `Claire`       GENDER: Female             INFO: Claire Watts
    CODE: ns        NAME: `Nari`         GENDER: Female             INFO: Nari Song
    CODE: chw       NAME: `Mr. Watts`    GENDER: Male               INFO: Charles (Claire's dad)
    CODE: en        NAME: `Eugene`       GENDER: Male               INFO: Eugene Nowakowski
    CODE: fw        NAME: `Mrs. Watts`   GENDER: Female             INFO: Farah (Claire's mother)
    CODE: mcon      NAME: `Mitch Conner` GENDER: Male               INFO: Mitch Conor (April's Band Lead Guitar)
    CODE: mj        NAME: `Megan`        GENDER: Female             INFO: Megan John
    CODE: ml        NAME: `Mrs. Maureen` GENDER: Female             INFO: Maureen Lindt
    CODE: pm        NAME: `Peter`        GENDER: Male               INFO: Peter Maloney
    CODE: ps        NAME: `Pepper Storm` GENDER: Female             INFO: Pepper Storm (April's Band Drummer)
    CODE: sr        NAME: `Sienna`       GENDER: Female             INFO: Sienna Roberts
    CODE: dvh       NAME: `Denise`       GENDER: Female             INFO: Denise Van der Haute
    CODE: km        NAME: `Kellie`       GENDER: Female             INFO: Kellie Moore
    CODE: tl        NAME: `Taisia`       GENDER: Female             INFO: Taisia Lindqvist
    CODE: vs        NAME: `Veronica`     GENDER: Female             INFO: Veronica Steele
    CODE: ak        NAME: `Amanda`       GENDER: Female             INFO: Amanda Kline
    CODE: ec        NAME: `Eileen`       GENDER: Female             INFO: Eileen Cavendish
    CODE: jh        NAME: `Jayden`       GENDER: Male               INFO: Jayden Hester
    CODE: kw        NAME: `Kai`          GENDER: Male               INFO: Kai Wyatt
    CODE: lm        NAME: `Libby`        GENDER: Female             INFO: Libby Moore
    CODE: sb        NAME: `Bruce`        GENDER: Male               INFO: Sam Bruce
    CODE: sj        NAME: `Sue`          GENDER: Female             INFO: Sue Johnson
    CODE: ms        NAME: `Maya`         GENDER: Female             INFO: Maya Siegel
    CODE: nr        NAME: `Nelson Rohr`  GENDER: Male               INFO: Nelson Rohr
    CODE: narrator  NAME: `Narrator`     GENDER: Non-binary         INFO: Used For Narration.     SPECIALTY: Has no code role. So, all dialogue without speaker attribution is Narrator.
    CODE: mhmes     NAME: `[mhmesname]`  GENDER: Female             INFO: Lyssa or Min            SPECIALTY: Used when the speaker could be either Lyssa or Min depending on player choice.

7. Always use the character's specialty and gender to guide translation choices, ensuring respectful and accurate representation.
