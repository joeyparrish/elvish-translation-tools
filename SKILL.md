---
name: elvish-translation-tools
description: Use when translating, reviewing, or maintaining UI / document translations into Sindarin or Quenya (Tolkien's Elvish languages). Triggers include: working with a Sindarin / sjn / Quenya / qya locale file; asked to translate an English string into Elvish; reviewing existing Elvish translations for correctness; adding new strings to an existing Elvish translation. Uses the bundled Eldamo lexicon and grammar references to ground every choice in attested or documented forms.
allowed-tools: Bash(python3 */elvish-translation-tools/scripts/lookup.py *), Bash(python3 */elvish-translation-tools/scripts/transliterate.py *), Bash(python3 */elvish-translation-tools/scripts/regen_tengwar.py *), Bash(python3 */elvish-translation-tools/scripts/preview.py *)
---

# Elvish Translation Tools

## Core principle

**Every word in an Elvish translation must be traceable to a source: Tolkien's writings, a Neo-Sindarin reconstruction in Eldamo, or a deliberate coinage that you explicitly flag.** Hallucinated vocabulary is the failure mode this skill exists to prevent.

Sindarin and Quenya have small attested corpora and large reconstructed vocabularies. Models often "know" plausible-looking words that don't actually exist, or mix Quenya words into Sindarin text. Always check.

## When to use

- A translation source file uses Sindarin (`sjn`) or Quenya (`qya`).
- The user asks to translate an English string into Elvish.
- The user asks to review or critique an Elvish translation.
- The user asks to add or revise entries in an Elvish translation file.
- You encounter a Tolkien / Middle-earth language question in code context.

## When NOT to use

- Translation to natural languages (use a normal translation skill).
- Lore / worldbuilding questions unrelated to language work.
- Tolkien-flavoured naming that explicitly wants made-up words and doesn't need linguistic grounding.

## Modes

### Mode 1: Review

Use when an entry (or a whole file) already exists and you're checking it.

1. For each Elvish word in the entry, run:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py check <word>
   ```
   This reports: where the word is attested, in what language, and any warnings (Quenya-as-Sindarin, deprecated, Gnomish revival, etc.).
2. Apply the review checklist below.
3. If the entry uses the project's translation schema (see Schema section), verify the `elements[]` provenance matches what `lookup.py check` reports.
4. Surface findings: keep / revise / replace, with reasoning. Don't silently rewrite.

### Mode 2: Translate

Use when adding new entries (drift from upstream source) or producing a translation from scratch.

1. Search the lexicon for relevant words:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py search <english-substring>
   ```
   For false-friend awareness across languages, add `--any-lang`.
2. Check existing project vocabulary for recurring lexemes (e.g. if the project consistently uses `northo` for "play", reuse it; don't invent a new word).
3. Propose candidates ranked: attested > Neo-Sindarin > defensible reconstruction > coinage. Present alternatives, not single answers, when more than one is plausible.
4. Verify each component:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py check <proposed-word>
   ```
5. Apply mutation rules at element boundaries (see Mutations section).
6. Fill out the project's schema fields if the file uses one. At minimum: `sjn.roman`, `sjn.literal`, and `elements[]` with `attestation` and `source` per element.
7. Defer to the user on any coinage. Never invent vocabulary and present it as established.

## The lookup tool (essential)

Path: `${CLAUDE_SKILL_DIR}/scripts/lookup.py`. Reads compact TSVs extracted from Paul Strack's Eldamo lexicon. Default scope: Sindarin family (s, n, ns). Add `--any-lang` to include Quenya / Gnomish.

| Subcommand | Use for |
|------------|---------|
| `lookup <lemma>` | Exact dictionary lookup. Returns the headword entry. |
| `search <gloss>` | Find Sindarin words whose English gloss contains a substring. |
| `check <form>` | **Workhorse.** Reports attestation status + warnings for any form. Use before accepting or proposing any word. |
| `cognates <lemma>` | Show related forms across Sindarin / Noldorin / Quenya. False-friend detection. |
| `forms <pattern>` | Search attested inflected / compound surface forms. |

Run `python3 ${CLAUDE_SKILL_DIR}/scripts/lookup.py --help` for full options.

## Languages and how the tool labels them

| Code | Language | Use for |
|------|----------|---------|
| `s` | Sindarin (post-LotR conception) | Primary target language. |
| `n` | Noldorin (1930s precursor to Sindarin) | Fallback when Sindarin lacks a word; flag explicitly. |
| `ns` | Neo-Sindarin | Modern reconstructions in Eldamo; flag with creator. |
| `q` | Quenya (post-LotR conception) | False-friend check only. **Do not mix into Sindarin text.** |
| `nq` | Neo-Quenya | Same caution as Quenya. |
| `g` | Gnomish (1910s, ancestor of Sindarin) | Rare revival material; flag explicitly. |
| `en` | Early Noldorin (1920s) | Rare revival material; flag explicitly. |

## False friends and common mistakes

The most frequent error is reaching for a Quenya word that looks like the right meaning. Some recurring traps:

| Wrong | Correct Sindarin | Note |
|-------|------------------|------|
| `lambë` "language" | `lam` (sg.) / `laim`, `lammath` (pl. / coll.) | `lambë` is Quenya. |
| `la` "not" | `ú-` (prefix, with mutation) or `law` / `baw` | `la` is Quenya. |
| `panta` "open" | `pant` | `panta` is Quenya. |
| `lintië` "speed" | `lint` "swift" (adj.; no direct attested noun) | `lintië` is Quenya. |
| `enquet-` "repeat" | No attested Sindarin verb; use `ad-` prefix on a verb of doing/saying | `enquet-` is Quenya AND deprecated in Eldamo. |
| `hasto` for "pause" | `daro` (attested imperative of `dar-` "halt") | `hasto` is attested but means "hack through". |
| `neth` for "number" | `gonod` (count) / `nediad` (counting) | `neth` means "girl, youth" in Sindarin. |
| `abont` "backwards" | `adel` "behind" | `abont` is Gnomish, not Sindarin. |

When in doubt, `check` the candidate.

## Mutations (essential reference)

Sindarin requires consonant mutations at certain word boundaries. Get these wrong and the text looks foreign even when the vocabulary is right.

### Soft mutation (lenition)
Triggered by: prepositions `ab, adel, am, be, di, na, nu, trî, u-`; adjectives after their noun; direct objects of verbs; compound second elements.

| Basic | Mutated |
|-------|---------|
| b → v | c → g | d → dh |
| g → (silent) | gw → w | h → ch |
| hw → chw | m → v | p → b |
| s → h | t → d | th → th (no change) |

### Nasal mutation
Triggered by: plural article `in`; preposition / prefix `an` "for, to"; preposition `dan` "against".

| Basic | Mutated |
|-------|---------|
| b → m | d → n | g → ng |
| p → ph | t → th | c → ch |

### Hard mutation
Triggered by: prepositions `ed` "out of", `ned` "in", `o` / `od` "from".

| Basic | Mutated |
|-------|---------|
| p → ph | t → th | c → ch |
| b → p | d → t | g → c |

For the full table including speculative mixed / liquid mutations, see `${CLAUDE_SKILL_DIR}/references/mutations.md`.

## Grammar quick reference

- **Imperative**: ending `-o` for all persons. `dar-` "halt" → `daro!`.
- **Gerund / infinitive**: `-ed` or `-ad`. `teitha-` "write" → `teithad` "writing / to write".
- **Past participle**: `-en` (sg) / `-in` (pl). `teitha-` → `teithen` / `teithin`.
- **Causative**: Quenya `-ta-` extended into Neo-Sindarin (`nor-` "run" → `northa-` "make run"). Defensible but flag as reconstructed.
- **Article**: `i` (sg, lenites) / `in` (pl, nasal-mutates).
- **Adjective**: follows its noun, undergoes lenition. `aran` "king" + `pant` "open" → `aran bant`.
- **"in"**: `mi` (no mutation) or lenited `vi`. Not `bir` (unattested).

For verb paradigms, pluralization rules, pronouns, and prepositions, see `${CLAUDE_SKILL_DIR}/references/grammar.md`.

## Translation source-file schema

Many translation projects benefit from a structured YAML that records per-word provenance. The recommended v1 schema lives at `${CLAUDE_SKILL_DIR}/references/translation-schema.md`. Read it when:

- The project's translation file already uses `elements[]` or similar.
- You're proposing to introduce structure to an unstructured file.
- The user asks "how should we document this choice?"

Key enums to know:

- **Attestation**: `attested` / `noldorin` / `gnomish` / `neo-sindarin` / `quenya` / `coined` / `deprecated`.
- **Status**: `attested` / `attested-components` / `defensible-neo-sindarin` / `coinage` / `needs-revision` / `placeholder`.

When filling out `elements[]`, the source citation should be whatever `lookup.py check` reports (e.g. `Ety/NOR`, `PE17/174`, `LotR/0339`).

## Script encoding (Tengwar)

The `sjn.tengwar` field uses CSUR (ConScript Unicode Registry) Tengwar at U+E000–U+E07F, the encoding supported by the Tengwar Telcontar font and the Tecendil transliterator. Do not hand-edit these characters; they render as boxes without a CSUR-aware font. See `${CLAUDE_SKILL_DIR}/references/tengwar-csur.md` for the codepoint table and `${CLAUDE_SKILL_DIR}/references/translation-schema.md` for alternative encodings.

## Producing Tengwar from romanized Sindarin / Quenya

Use the bundled transliteration engine instead of hand-typing Tengwar:

    python3 ${CLAUDE_SKILL_DIR}/scripts/transliterate.py sjn "<romanized>"
    python3 ${CLAUDE_SKILL_DIR}/scripts/transliterate.py qya "<romanized>"
    python3 ${CLAUDE_SKILL_DIR}/scripts/transliterate.py sjn "<romanized>" --show-codepoints

The engine implements Tecendil's Sindarin / Quenya / Beleriand modes (mode files vendored under `${CLAUDE_SKILL_DIR}/data/modes/`). Its output is CSUR Tengwar codepoints.

**Default output format is `\uXXXX` escape sequences**, not literal PUA characters. This is so the result can be reviewed in any editor and pasted directly into a YAML `sjn.tengwar` double-quoted string or a JSON value. Use `--literal` only to pipe into a font-aware preview, never to store in source files.

When to use:

- **Filling in `sjn.tengwar` for a new entry**: produce the romanized form first (so it's reviewable), then transliterate. Never invent the Tengwar field; always derive it.
- **Verifying an existing `sjn.tengwar`**: transliterate the entry's `sjn.roman` and compare. A mismatch flags either an old hand-typed entry to update or a roman/Tengwar disagreement worth investigating.

Output matches Tecendil's deployed engine for the 24 regression cases in `${CLAUDE_SKILL_DIR}/data/modes/sindarin-tests.yaml` and `quenya-tests.yaml`. Known divergences: no thin-space (U+2009) word separator (Tecendil emits it for display only).

## Previewing escape-encoded Tengwar

To render escape-encoded Tengwar as literal glyphs (requires Tengwar Telcontar or another CSUR font installed):

    echo '' | python3 ${CLAUDE_SKILL_DIR}/scripts/preview.py -
    python3 ${CLAUDE_SKILL_DIR}/scripts/preview.py --yaml path/to/sjn-translations.yaml

## Bulk-regenerating tengwar fields

After revising one or more `sjn.roman` fields in a translation YAML, sync the corresponding `sjn.tengwar` fields:

    python3 ${CLAUDE_SKILL_DIR}/scripts/regen_tengwar.py path/to/sjn-translations.yaml
    python3 ${CLAUDE_SKILL_DIR}/scripts/regen_tengwar.py path/to/qya-translations.yaml --mode qya
    python3 ${CLAUDE_SKILL_DIR}/scripts/regen_tengwar.py path/to/sjn-translations.yaml --dry-run

For every entry with a non-empty `sjn.roman`, runs the romanized form through `transliterate.py` and replaces the value inside `tengwar: "..."` with the escape-encoded result. Uses targeted text editing -- comments, indentation, blank lines, and surrounding content are preserved exactly.

Use this any time you change a `roman` field; never hand-update a `tengwar` field.

## Editing translation YAML files safely

When generating or modifying entries in a translation YAML file (typically `sjn-translations.yaml`), the agent is responsible for emitting valid YAML. Common ways to break it:

**Never embed unescaped double quotes inside a double-quoted YAML string.** This is the most common failure. When citing source material, never write:

    source: "LotR/0307 (in lammen, "lasto beth lammen")"
    note: "Originally "hasto" (intended pause)."

The second `"` closes the string and YAML rejects the rest of the line. Use one of these instead:

- Single quotes around the inner phrase: `source: "LotR/0307 (in lammen, 'lasto beth lammen')"`
- Backslash-escape the inner quotes: `source: "LotR/0307 (in lammen, \"lasto beth lammen\")"`
- Restructure to avoid embedded quotes entirely: `source: "LotR/0307 (in the lammen phrase)"`

The single-quote-inside-double-quote form is usually the most readable and is the preferred style for this project.

**Other YAML safety rules when generating entries:**

- Don't put a colon followed by a space inside an unquoted scalar — YAML will read it as a mapping. Always quote strings that contain `: ` or any other YAML special characters (`#`, `&`, `*`, `!`, `|`, `>`, `'`, `"`, `%`, `@`, leading `-`/`?`/`,`).
- Preserve indentation exactly. The schema uses 1-space for list-item dashes and 5-space indent for nested-map keys.
- After generating any entry, run `python3 -c "import yaml; yaml.safe_load(open('path.yaml'))"` to verify the file parses.
- When modifying an existing entry that contains Tengwar PUA characters, read the file first with the Read tool (which preserves the chars) before using Edit. Don't try to type the PUA chars from memory.

**For values containing Tengwar codepoints**: store as `\uXXXX` escape sequences (see "Producing Tengwar" above), never as literal PUA characters. This avoids invisible-character bugs and makes the YAML reviewable.

## Review checklist

For each entry being reviewed or proposed:

1. **Attestation**: every element checked with `lookup.py check`. Status recorded.
2. **Language purity**: no Quenya headwords used as Sindarin (unless explicitly intentional). Run `cognates` if in doubt.
3. **Deprecation**: nothing flagged DEPRECATED in Eldamo (e.g. `meiras`, `enquet-`).
4. **Wrong-meaning attested forms**: the form exists but means something else? (`hasto`, `neth`.) `check` will surface this via the surface-form listings.
5. **Mutations applied** at element boundaries per the mutation tables.
6. **Word order**: adjective follows noun; preposition precedes; verb position natural.
7. **Project vocabulary consistency**: recurring lexemes match what the project has already used (e.g. always `northo` for "play").
8. **Coinages flagged** as such, not presented as established vocabulary.

## Common rationalizations to resist

| Excuse | Reality |
|--------|---------|
| "I know this Sindarin word" | Training data is unreliable for low-resource constructed languages. Always `check`. |
| "Quenya is close enough" | It isn't. Quenya inside Sindarin reads as broken to anyone who recognizes the difference. |
| "I'll just coin a plausible word" | Coinage is OK, but must be flagged; never present as established. |
| "Mutations are too complex, skip them" | Wrong mutation = visibly broken Sindarin. Apply per the tables. |
| "The user will fix it later" | Make the right call now or defer explicitly. Don't ship guesses. |
| "It's just a UI string, low stakes" | Low stakes means more reason to be honest about confidence, not less. |
| "I'll add a citation with the phrase quoted" | Watch the YAML quoting. Embedded double quotes inside a double-quoted string break the file. Use single quotes for the inner phrase, or paraphrase. See 'Editing translation YAML files safely'. |

## Real-world failure modes (from prior review)

These came up reviewing an existing UI translation. Patterns to recognize:

- **Quenya intrusion via familiarity**: `lambë` for "language" (Sindarin: `lam`). `panta` for "open" (Sindarin: `pant`). The Quenya forms are more famous from fan material; the Sindarin equivalents are less seen but correct.
- **Sindarin morphology on Quenya stem**: `enqueto` from Quenya `enquet-` + Sindarin imperative `-o`. The grammar is Sindarinized but the lexeme is Quenya. Always start from a Sindarin headword.
- **Attested form, wrong meaning**: `hasto` is real Sindarin but means "hack through" (root SYAD), not "pause". `neth` is real Sindarin but means "girl / youth", not "number". The lookup tool catches these via the surface-form listing.
- **Gnomish-as-Sindarin**: `abont` "backwards" and `unt` "nothing" are Gnomish (1910s), not Sindarin. May be deliberate revivals; flag them.
- **Deprecated Neo-Sindarin**: `meiras` for "value" was coined by Paul Strack but flagged deprecated in Eldamo. The tool surfaces this.

## Project-specific application

Translation projects layer their own conventions on this framework. Look for:

- A README or `applying-schema.md` in the project root.
- The existing translation file's vocabulary (recurring lexemes = project conventions).
- A `glossary.md` or similar from prior review work.

Don't override project-specific conventions; reuse them. If the project consistently uses `fanwos` for "picture / screen", new entries that touch that concept should use `fanwos` too.

## Hand-off rules

- **Coinages**: never invent without surfacing to the user. Present coinage candidates explicitly, with the alternatives considered.
- **Existing-text revisions**: don't silently rewrite an existing translation. Report findings, propose revisions, await direction.
- **Schema migrations**: if introducing the schema to an unstructured file, do it in two phases (mechanical lift, then incremental backfill), not all at once.
- **Mutation uncertainty**: if a mutation rule is contested between Sindarin grammarians (e.g. mixed mutation), pick the more conservative reading and note the choice.
