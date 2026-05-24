# Sindarin Translation Reference Materials

Reference data for maintaining the Sindarin translation of Shaka Player
(`ui/locales/sjn-translations.yaml` in the shaka-player repo).

## Contents

- `eldamo/` -- Paul Strack's Eldamo lexicon (git clone of
  https://github.com/pfstrack/eldamo). The data file is at
  `eldamo/src/data/eldamo-data.xml` (~30 MB, 35k+ entries spanning Quenya,
  Sindarin, and earlier conceptual stages). Each entry has reliability
  markers (attested, neologism, reconstructed, deprecated). Query Sindarin
  entries by `l="s"`, Quenya by `l="q"` or `l="nq"` (Neo-Quenya).
- `mutations.md` -- Summary of Sindarin consonant mutations (soft / nasal
  / hard / mixed / liquid) and what triggers each.
- `grammar.md` -- Sindarin morphology / syntax reference: verb forms,
  pluralization, word order, pronouns, common prepositions, derivational
  affixes, and translation pitfalls.

## How to query

Quick word lookups in Eldamo:

    grep -m 5 'l="s" v="WORD"' eldamo/src/data/eldamo-data.xml

For English-to-Sindarin search, grep on `gloss=`:

    grep 'l="s"' eldamo/src/data/eldamo-data.xml | grep -i 'gloss="[^"]*MEANING'

Higher-level access via `scripts/lookup.py` (which reads the extracted
TSVs in `data/`, not the XML directly).

## Licensing

Eldamo is CC-BY 4.0 (Paul Strack), based on the works of J.R.R. Tolkien
(his intellectual property).
