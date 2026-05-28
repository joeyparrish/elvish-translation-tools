# Elvish Translation Tools

A [Claude Code][] skill for translating, reviewing, and maintaining
translations into Tolkien's Elvish languages (Sindarin and Quenya).
Every choice is grounded in the [Eldamo][] lexicon (Paul Strack); the
skill won't propose vocabulary it can't cite.

This repo is the skill itself plus the data and tools it relies on.
The skill is reusable across any translation project; project-specific
workspaces (translation files, project glossaries) live in their own
repos and reference this one.

## Install

Clone into your Claude Code skills directory:

    git clone https://github.com/joeyparrish/elvish-translation-tools \
      ~/.claude/skills/elvish-translation-tools

Claude Code discovers the skill via the [SKILL.md][] at the repo root.
The skill auto-loads when you work on Elvish translations; you can also
invoke it explicitly. No further configuration is required.

To update, `git pull` in `~/.claude/skills/elvish-translation-tools/`.

## What the skill does

- **Translate**: takes an English string and proposes Sindarin (or
  Quenya) candidates, ranked by attestation, with per-element
  provenance and rationale.
- **Review**: reads an existing translation, checks every word against
  the lexicon, and surfaces false friends (Quenya-as-Sindarin),
  deprecated coinages, wrong-meaning attested forms, and missing
  mutations.

The skill stays honest about confidence. Anything coined is flagged as
coinage; anything reconstructed is flagged as Neo-Sindarin with the
original creator cited.

## Worked example

For a complete example of a translation project built with this skill, see my
[full translation of Shaka Player's UI into Sindarin](https://github.com/joeyparrish/shaka-sjn-translation).

## Standalone use of the tools

All scripts work without invoking the skill, useful for ad hoc queries
or batch processing of translation files:

    # Attestation lookup over the Eldamo lexicon
    python3 scripts/lookup.py check lambë
    python3 scripts/lookup.py search halt
    python3 scripts/lookup.py forms daro

    # Romanized -> CSUR Tengwar (default: \uXXXX escapes)
    python3 scripts/transliterate.py sjn "daro dîn"
    python3 scripts/transliterate.py qya "namárië"

    # Bulk-regen tengwar fields in a schema-following YAML
    python3 scripts/regen_tengwar.py path/to/translations.yaml

    # Render escape-encoded Tengwar to literal PUA for a font-aware terminal
    echo '' | python3 scripts/preview.py -

See [`scripts/README.md`][scripts-readme] for the full subcommand
reference and [`references/README.md`][references-readme] for the
grammar / mutation / schema / codepoint documentation.

## Layout

- [`SKILL.md`][SKILL.md] -- the skill itself; loaded by Claude Code.
- `data/` -- compact TSV extracts of the [Eldamo][] lexicon (committed,
  so the tools work out of the box) and Tecendil-format mode files
  for Sindarin / Quenya / Beleriand transliteration.
- `scripts/` -- `extract.py` (regenerate TSVs from upstream Eldamo),
  `lookup.py` (attestation), `transliterate.py` (romanized -> CSUR),
  `regen_tengwar.py` (bulk-regen YAML tengwar fields), `preview.py`
  (escape -> literal for font-aware display), `test_transliterate.py`
  (regression suite against empirical Tecendil output).
- `references/` -- hand-written grammar, mutation, CSUR codepoint, and
  translation source-file schema references, plus instructions for
  cloning upstream [Eldamo][] when the TSVs need to be regenerated.

## Requirements

- Python 3 (standard library only for lookup scripts; others use PyYAML).
- [Claude Code][] for the skill itself; the scripts work standalone.

## Related

- [Eldamo][] (Paul Strack), CC-BY 4.0; the source the TSVs are derived
  from. Eldamo covers Quenya, Sindarin, Noldorin, Gnomish, and earlier
  conceptual stages with reliability markers.
- [Tecendil][] (Arno Gourdol); the transliterator whose deployed
  rule semantics this skill's `transliterate.py` reproduces. Mode
  files vendored from arnog/tecendil-js (MIT).


[Claude Code]: https://claude.com/claude-code
[Eldamo]: https://github.com/pfstrack/eldamo
[Tecendil]: https://www.tecendil.com
[SKILL.md]: ./SKILL.md
[scripts-readme]: ./scripts/README.md
[references-readme]: ./references/README.md
