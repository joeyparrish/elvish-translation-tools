# Elvish Translation Tools

A [Claude Code][] skill for translating, reviewing, and maintaining
translations into Tolkien's Elvish languages (Sindarin and Quenya). Every
choice is grounded in the [Eldamo][] lexicon (Paul Strack); the skill
won't propose vocabulary it can't cite.

This repo is the skill itself plus the data and tools it relies on. The
skill is reusable across any translation project; project-specific
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

## Standalone use of the tools

The lookup tool also works without invoking the skill, useful for ad hoc
queries:

    python3 scripts/lookup.py check lambë      # attestation check
    python3 scripts/lookup.py search halt      # find by English meaning
    python3 scripts/lookup.py lookup dar-      # exact lemma lookup
    python3 scripts/lookup.py forms daro       # search attested surface forms

See [`scripts/README.md`][scripts-readme] for the full subcommand
reference and [`references/README.md`][references-readme] for the
grammar / mutation / schema documentation.

## Layout

- [`SKILL.md`][SKILL.md] -- the skill itself; loaded by Claude Code.
- `data/` -- compact TSV extracts of the [Eldamo][] lexicon, split by
  language family. Committed so the tools work out of the box.
- `scripts/` -- `extract.py` regenerates the TSVs from upstream
  [Eldamo][]; `lookup.py` provides lookup / search / attestation-check
  / cognates / forms subcommands over the TSVs.
- `references/` -- hand-written grammar, mutation, and translation
  source-file schema references, plus instructions for cloning upstream
  [Eldamo][] when the TSVs need to be regenerated.

## Requirements

- Python 3 (standard library only).
- [Claude Code][] for the skill itself; the scripts work standalone.

## Related

- [Eldamo][] (Paul Strack), CC-BY 4.0; the source the TSVs are derived
  from. Eldamo covers Quenya, Sindarin, Noldorin, Gnomish, and earlier
  conceptual stages with reliability markers.


[Claude Code]: https://claude.com/claude-code
[Eldamo]: https://github.com/pfstrack/eldamo
[SKILL.md]: ./SKILL.md
[scripts-readme]: ./scripts/README.md
[references-readme]: ./references/README.md
