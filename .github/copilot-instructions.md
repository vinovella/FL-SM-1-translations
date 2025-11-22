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
   CODE: mc        NAME: `[mcname]`     CHINESE_TRANSLATION: `[mcname]`    GENDER: Male               INFO: Main Character          		SPECIALTY: Default Name - Mike Young. Plyers can change the first name
   CODE: mct       NAME: `[mcname]`     CHINESE_TRANSLATION: `[mcname]`    GENDER: Male               INFO: Main Character thinking 	SPECIALTY: Default Name - Stacy Brown. Can be Stacy Young depending on game version
   CODE: mcd       NAME: `[mcname]`     CHINESE_TRANSLATION: `[mcname]`    GENDER: Male               INFO: Main Character          		SPECIALTY: Player can name the character, but gender is fixed
   CODE: mo        NAME: `You`          CHINESE_TRANSLATION: `你`          GENDER: Male               INFO: Main Character          			SPECIALTY: Player can name the character, but gender is fixed
   CODE: arj       NAME: `AmRose`   CHINESE_TRANSLATION: `爱洛丝"`       GENDER: Female             INFO: Amber-Rose Jenkins
   CODE: bg        NAME: `Amore`        CHINESE_TRANSLATION: `阿茉`         GENDER: Female             INFO: BDSM Model Amore
   CODE: dc        NAME: `Debbie`       CHINESE_TRANSLATION: `黛比`         GENDER: Female             INFO: Debbie Callahan         		SPECIALTY: Trans character (has a penis). Identifies as She/Her.
   CODE: kv        NAME: `Kanya`        CHINESE_TRANSLATION: `康雅`         GENDER: Female             INFO: Kanya Vu
   CODE: mes       NAME: `Min`          CHINESE_TRANSLATION: `明`          GENDER: Female             INFO: Min Eun-Soo
   CODE: mh        NAME: `Lyssa`        CHINESE_TRANSLATION: `丽莎`         GENDER: Female             INFO: Melissa Harris (Lyssa)  		SPECIALTY: Trans character (has a penis). Identifies as She/Her.
   CODE: my        NAME: `Melony`       CHINESE_TRANSLATION: `梅洛妮啊`     GENDER: Female             INFO: Melony Young			SPECIALTY: Default Name - Melony Chase. Can be Melony Young depending on game version
   CODE: sy        NAME: `Stacy`        CHINESE_TRANSLATION: `史黛西`       GENDER: Female             INFO: Stacy Young
   CODE: atp       NAME: `Angela`       CHINESE_TRANSLATION: `安琪拉`        GENDER: Female             INFO: Angela Taylor Portillo
   CODE: be        NAME: `Bently`       CHINESE_TRANSLATION: `本特利`        GENDER: Female             INFO: Bently (Taisia's coworker clown)
   CODE: cg        NAME: `Creepy Guy`   CHINESE_TRANSLATION: `怪人`         GENDER: Male               INFO: Creepy Guy (Not named)
   CODE: cs        NAME: `Cecilia`      CHINESE_TRANSLATION: `塞西莉亚`       GENDER: Female             INFO: Cecilia Siegal
   CODE: dw        NAME: `Dog Walker`   CHINESE_TRANSLATION: `遛狗人`        GENDER: Female             INFO: Dog Walker
   CODE: ed        NAME: `Elizabeth`    CHINESE_TRANSLATION: `伊丽莎白`       GENDER: Female             INFO: Elizabeth Davis
   CODE: hr        NAME: `Hana`         CHINESE_TRANSLATION: `哈娜`         GENDER: Female             INFO: Hana Rivera
   CODE: ic        NAME: `Inga`         CHINESE_TRANSLATION: `英格`         GENDER: Female             INFO: Inga Cowen
   CODE: jg        NAME: `Juggsy`       CHINESE_TRANSLATION: `朱西`         GENDER: Male               INFO: Juggsy (Taisia's coworker clown)
   CODE: ka        NAME: `Kennedy`      CHINESE_TRANSLATION: `肯尼迪`        GENDER: Female             INFO: Kennedy Assworth
   CODE: lg        NAME: `Lauren`       CHINESE_TRANSLATION: `劳伦`         GENDER: Female             INFO: Lauren Grindsly
   CODE: nj        NAME: `Jogger`       CHINESE_TRANSLATION: `慢跑人`        GENDER: Female             INFO: Nelly
   CODE: ols       NAME: `Olivia`       CHINESE_TRANSLATION: `奥利维亚`       GENDER: Female             INFO: Olivia Small
   CODE: rd        NAME: `Ridley`       CHINESE_TRANSLATION: `雷德利`        GENDER: Female             INFO: Ridley Driver
   CODE: zh        NAME: `Zuzana`       CHINESE_TRANSLATION: `祖扎娜`        GENDER: Female             INFO: Zuzana Holab
   CODE: ag        NAME: `Anna`         CHINESE_TRANSLATION: `安娜`         GENDER: Female             INFO: Anna Goodwin
   CODE: am        NAME: `April`        CHINESE_TRANSLATION: `艾普尔`        GENDER: Female             INFO: April
   CODE: cw        NAME: `Claire`       CHINESE_TRANSLATION: `克莱尔`        GENDER: Female             INFO: Claire Watts
   CODE: ns        NAME: `Nari`         CHINESE_TRANSLATION: `娜丽`         GENDER: Female             INFO: Nari Song
   CODE: chw       NAME: `Mr. Watts`    CHINESE_TRANSLATION: `沃茨先生`       GENDER: Male               INFO: Charles (Claire's dad)
   CODE: en        NAME: `Eugene`       CHINESE_TRANSLATION: `尤金`         GENDER: Male               INFO: Eugene Nowakowski
   CODE: fw        NAME: `Mrs. Watts`   CHINESE_TRANSLATION: `沃茨夫人`      GENDER: Female             INFO: Farah (Claire's mother)
   CODE: mcon      NAME: `Mitch Conner` CHINESE_TRANSLATION: `米奇·康纳`     GENDER: Male               INFO: Mitch Conor (April's Band Lead Guitar)
   CODE: mj        NAME: `Megan`        CHINESE_TRANSLATION: `梅根`         GENDER: Female             INFO: Megan John
   CODE: ml        NAME: `Mrs. Maureen` CHINESE_TRANSLATION: `莫琳夫人`      GENDER: Female             INFO: Maureen Lindt
   CODE: pm        NAME: `Peter`        CHINESE_TRANSLATION: `皮特`         GENDER: Male               INFO: Peter Maloney
   CODE: ps        NAME: `Pepper Storm` CHINESE_TRANSLATION: `佩珀・斯托姆`   GENDER: Female             INFO: Pepper Storm (April's Band Drummer)
   CODE: sr        NAME: `Sienna`       CHINESE_TRANSLATION: `西耶娜`        GENDER: Female             INFO: Sienna Roberts
   CODE: dvh       NAME: `Denise`       CHINESE_TRANSLATION: `丹尼斯`        GENDER: Female             INFO: Denise Van der Haute
   CODE: km        NAME: `Kellie`       CHINESE_TRANSLATION: `凯莉`         GENDER: Female             INFO: Kellie Moore
   CODE: tl        NAME: `Taisia`       CHINESE_TRANSLATION: `泰西娅`       GENDER: Female             INFO: Taisia Lindqvist
   CODE: vs        NAME: `Veronica`     CHINESE_TRANSLATION: `维罗妮卡`      GENDER: Female             INFO: Veronica Steele
   CODE: ak        NAME: `Amanda`       CHINESE_TRANSLATION: `阿曼达`        GENDER: Female             INFO: Amanda Kline
   CODE: ec        NAME: `Eileen`       CHINESE_TRANSLATION: `艾琳`         GENDER: Female             INFO: Eileen Cavendish
   CODE: jh        NAME: `Jayden`       CHINESE_TRANSLATION: `杰登`         GENDER: Male               INFO: Jayden Hester
   CODE: kw        NAME: `Kai`          CHINESE_TRANSLATION: `凯`           GENDER: Male               INFO: Kai Wyatt
   CODE: lm        NAME: `Libby`        CHINESE_TRANSLATION: `莉比`         GENDER: Female             INFO: Libby Moore
   CODE: sb        NAME: `Bruce`        CHINESE_TRANSLATION: `布鲁斯`        GENDER: Male               INFO: Sam Bruce
   CODE: sj        NAME: `Sue`          CHINESE_TRANSLATION: `苏`           GENDER: Female             INFO: Sue Johnson
   CODE: ms        NAME: `Maya`         CHINESE_TRANSLATION: `玛雅`         GENDER: Female             INFO: Maya Siegel
   CODE: nr        NAME: `Nelson Rohr`  CHINESE_TRANSLATION: `纳尔逊·罗尔`   GENDER: Male               INFO: Nelson Rohr
   CODE: zp        NAME: `Zemfira`      CHINESE_TRANSLATION: `泽菲拉`       GENDER: Female             INFO: Zemfira Power
   CODE: ef        NAME: `Elena`        CHINESE_TRANSLATION: `爱丽娜`       GENDER: Female             INFO: Elena Flanagon
   CODE: dd        NAME: `Daisy`        CHINESE_TRANSLATION: `黛西`         GENDER: Female             INFO: Daisy Diamond
   CODE: dl        NAME: `Doug`         CHINESE_TRANSLATION: `道格`         GENDER: Male               INFO: Doug Dickles
   CODE: et        NAME: `Ethan`        CHINESE_TRANSLATION: `伊桑`         GENDER: Male                INFO: Ethan Foxmorr
   CODE: cb        NAME: `Carmel`       CHINESE_TRANSLATION: `卡梅尔`       GENDER: Female              INFO: Carmel Blaise
   CODE: sbf       NAME: `Samiya`       CHINESE_TRANSLATION: `萨米娅`       GENDER: Female              INFO: Samiya Byers
   CODE: narrator  NAME: `Narrator`     CHINESE_TRANSLATION: None           GENDER: Non-binary         INFO: Used For Narration.     	SPECIALTY: Has no code role. So, all dialogue without speaker attribution is Narrator.
   CODE: mhmes     NAME: `[mhmesname]`  CHINESE_TRANSLATION: `丽莎` or `明`  GENDER: Female             INFO: Lyssa or Min            	SPECIALTY: Used when the speaker could be either Lyssa or Min, depending on player choice.
8. Always use the character's specialty and gender to guide translation choices, ensuring respectful and accurate representation.
9. When translating to Chinese, use the provided Chinese translations for character names.
10. When translating to Italian, don't translate character names.
11. If the speaker is text in quotes, then translate that as well.
12. Do not translate comments that start with # and lines that start with old
13. Escape in line quotes properly using the backslash (`\`) character.
