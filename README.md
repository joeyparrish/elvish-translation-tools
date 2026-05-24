# Elvish Translation Tools

A general-purpose framework for translation projects targeting Tolkien's
constructed languages (Sindarin, Quenya, and their precursors).

This repo provides the substrate: lexicon data, grammar references,
mutation tables, and lookup tools. Specific translation projects (for
particular software UIs, documents, etc.) live in their own repos and
use these tools.

## Layout

- `data/` -- compact TSV extracts of the Eldamo lexicon, split by
  language family. Committed so the tools work out of the box.
- `scripts/` -- `extract.py` regenerates the TSVs from upstream Eldamo;
  `lookup.py` provides lookup / search / attestation-check / cognates /
  forms subcommands over the TSVs.
- `references/` -- hand-written grammar and mutation references, plus
  instructions for cloning the upstream Eldamo lexicon when the TSVs
  need to be regenerated.

## Quick start

    python3 scripts/lookup.py check lambë      # attestation check
    python3 scripts/lookup.py search halt      # find by English meaning
    python3 scripts/lookup.py lookup dar-      # exact lemma lookup
    python3 scripts/lookup.py forms daro       # search attested surface forms

See `scripts/README.md` for the full subcommand reference and
`references/README.md` for the grammar / mutation documentation.

## Related

- Eldamo (Paul Strack) -- https://github.com/pfstrack/eldamo
  CC-BY 4.0; the source the TSVs are derived from.
