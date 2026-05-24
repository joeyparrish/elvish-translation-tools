# Sindarin / Quenya Translation Reference Materials

Reference data for translation projects targeting Tolkien's Elvish
languages. Used as the substrate for any specific translation effort.

## In this folder

- `mutations.md` -- Summary of Sindarin consonant mutations (soft / nasal
  / hard / mixed / liquid) and what triggers each.
- `grammar.md` -- Sindarin morphology / syntax reference: verb forms,
  pluralization, word order, pronouns, common prepositions, derivational
  affixes, and translation pitfalls.

## Upstream lexicon (not in repo)

The compact TSVs under `../data/` are extracted from Paul Strack's
**Eldamo** lexicon, which is too large (~30 MB XML, 35k+ entries) to
vendor here. The extracted TSVs are committed; the source XML is not.

To regenerate the TSVs (e.g. after Eldamo updates upstream), clone it
into this folder and run the extractor:

    git clone https://github.com/pfstrack/eldamo.git
    python3 ../scripts/extract.py

The clone path `references/eldamo/` is gitignored.

Eldamo covers Quenya, Sindarin, Noldorin, Gnomish, and earlier
conceptual stages, with reliability markers (attested, neologism,
reconstructed, deprecated, etc.).

## How to query

For everyday use, prefer `../scripts/lookup.py` (subcommands: lookup,
search, check, cognates, forms) which reads the extracted TSVs.

For ad hoc XML inspection after cloning Eldamo:

    grep -m 5 'l="s" v="WORD"' eldamo/src/data/eldamo-data.xml
    grep 'l="s"' eldamo/src/data/eldamo-data.xml | grep -i 'gloss="[^"]*MEANING'

## Licensing

Eldamo is CC-BY 4.0 (Paul Strack), based on the works of J.R.R. Tolkien
(his intellectual property).
