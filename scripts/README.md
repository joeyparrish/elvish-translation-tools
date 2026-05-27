# Scripts

## `extract.py`

Reads `references/eldamo/src/data/eldamo-data.xml` and writes compact
TSV files under `data/`:

- `data/sjn.tsv` -- Sindarin family (s, n, ns). ~6700 entries, ~330 KB.
- `data/qya.tsv` -- Quenya family (q, nq, mq, eq). ~15k entries, ~830 KB.
- `data/gno.tsv` -- Gnomish + Early Noldorin (g, en). ~5k entries.
- `data/refs.tsv` -- ~148k attested surface forms (inflected, compound).

Run after pulling new Eldamo data:

    python3 scripts/extract.py

## `lookup.py`

Subcommands (default scope: Sindarin family; add `--any-lang` for full):

    # Exact lemma match
    python3 scripts/lookup.py lookup dar-

    # Find by English gloss substring
    python3 scripts/lookup.py search halt --limit 5
    python3 scripts/lookup.py search count --any-lang

    # Comprehensive attestation check -- the workhorse for review
    python3 scripts/lookup.py check hasto
    python3 scripts/lookup.py check lambë
    python3 scripts/lookup.py check fanwos

    # Cross-language cognates / similar-looking forms
    python3 scripts/lookup.py cognates lambë

    # Search attested inflected / compound forms
    python3 scripts/lookup.py forms daro
    python3 scripts/lookup.py forms -en

The `check` command reports:

1. Whether the form appears as a headword in any included language.
2. Whether it appears as an attested surface form (cited in <ref> tags).
3. Warnings: Quenya-mistaken-for-Sindarin, Gnomish-fallback, deprecated
   in Eldamo, Neo-Sindarin neologism flag.

## `transliterate.py`

Romanized Sindarin / Quenya / Beleriand to CSUR Tengwar codepoints.

    # Default: escape-encoded output (reviewable, diff-friendly)
    python3 scripts/transliterate.py sjn "northo lim"
    python3 scripts/transliterate.py qya "namárië"
    python3 scripts/transliterate.py beleriand "elen sila"

    # Raw PUA codepoints (for piping into a font-aware preview)
    python3 scripts/transliterate.py sjn "daro" --literal

    # Diagnostic: print U+xxxx per codepoint
    python3 scripts/transliterate.py sjn "daro" --show-codepoints

Implements Tecendil's deployed rule semantics: file-order +
longest-match-with-anchored-priority rule application, tehtarFollow
positioning with telco fallback, context substitutions (silme ->
silme-nuquerna; lambe + bar -> bar-inside), capital-letter CSUR
extension (U+E080-U+E0AE), normalizeVowels for Quenya, JSONC block
comments, and UI-placeholder pass-through (`[VARIABLE]`).

Mode files vendored from arnog/tecendil-js (MIT) under `data/modes/`.

## `test_transliterate.py`

Regression suite for `transliterate.py` against the empirical Tecendil
fixtures in `data/modes/sindarin-tests.yaml` and `quenya-tests.yaml`.

    python3 scripts/test_transliterate.py

Normalizes Tecendil's display-only U+2009 thin-space before comparing,
since the engine deliberately doesn't emit it.

## `regen_tengwar.py`

Bulk-regenerate the `sjn.tengwar` field of every entry in a
schema-following translation YAML by running each entry's `sjn.roman`
through `transliterate.py`.

    python3 scripts/regen_tengwar.py path/to/translations.yaml
    python3 scripts/regen_tengwar.py path/to/translations.yaml --mode qya
    python3 scripts/regen_tengwar.py path/to/translations.yaml --dry-run

Uses targeted text editing rather than YAML round-trip parsing, so
comments, indentation, blank lines, quote styles, and any surrounding
content are preserved exactly. Only the substring inside
`tengwar: "..."` on each entry is touched.

## `preview.py`

Decode `\uXXXX` escape-encoded Tengwar to literal PUA characters for
display in a terminal with Tengwar Telcontar (or another CSUR font)
installed.

    # Inline string
    python3 scripts/preview.py ''

    # From stdin (e.g. piping from transliterate.py)
    python3 scripts/transliterate.py sjn daro | python3 scripts/preview.py -

    # Walk a translation YAML and preview each entry
    python3 scripts/preview.py --yaml path/to/translations.yaml

## Token cost

Loading the full Sindarin family TSV into a conversation costs ~85k
tokens. Using `lookup.py` instead keeps cost near zero per query.
A skill should invoke `lookup.py` on demand rather than vendoring
the data into context.
