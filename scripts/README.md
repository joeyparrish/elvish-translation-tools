# Scripts

## `extract.py`

Reads `references/eldamo/src/data/eldamo-data.xml` and writes compact TSV
files under `data/`:

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

## Token cost

Loading the full Sindarin family TSV into a conversation costs ~85k
tokens. Using `lookup.py` instead keeps cost near zero per query.
A skill should invoke `lookup.py` on demand rather than vendoring
the data into context.
