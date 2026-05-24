# Proposed structure for sjn-translations.yaml

Goal: capture enough provenance for each translation that we (or a future
maintainer, or a skill) can defend or critique it without re-deriving the
reasoning. Stay YAML so it remains hand-editable with the Tengwar font
workflow; stay backward-compatible with `sync-sjn.py` so the build pipeline
doesn't break.

## Top-level shape (per entry)

```yaml
- key: PLAY
  english: "Play"

  sjn:
    roman: "northo"
    literal: "make-run"
    tengwar: "    "   # Tengwar Telcontar PUA characters; edited with the font

  # Per-word breakdown. One entry per token in the romanized form,
  # in order. Lets us attach attestation/source to each piece.
  elements:
    - form: "northo"
      headword: "nor-"
      headword-meaning: "to run"
      attestation: attested
      source: "Ety/NOR"
      derivations:
        - "causative -tha-: nor- -> northa- 'to make run' (Neo-Sindarin pattern, extended from Quenya -ta-)"
        - "imperative -o: northa- -> northo"
      rationale: |
        Metaphor: 'play a video' = 'make it run'. Parallels English idiom.

  # Notes that apply to the whole construction (mutations between
  # elements, word order rationale, etc).
  composition: ""

  # Overall assessment.
  status: defensible-neo-sindarin
  concerns: |
    -tha- causative is reconstructed by extension from Quenya; not
    strictly attested in Sindarin. Common Neo-Sindarin pattern though.

  # Append-only log of changes. Captures *why* we changed our mind.
  history:
    - date: 2022-01-15
      note: "Initial translation."
```

## Field reference

### Required (consumed by sync-sjn.py)

- `key` -- localization key, must match `source.json`.
- `english` -- the English source string.
- `sjn.tengwar` -- the Tengwar-encoded form that becomes the value in
  `sjn.json`. (`sync-sjn.py` reads this via `item["sjn"]["tengwar"]`.)

### Required (human-facing)

- `sjn.roman` -- romanized Sindarin. The form everyone reads and reviews.
- `sjn.literal` -- a literal English back-translation, useful when
  proposing changes ("does this convey the right meaning?").

### Optional but recommended (provenance)

- `elements[]` -- per-word breakdown. One entry per token (or per
  compound element, your call).
  - `form` -- the surface form as it appears in `sjn.roman`.
  - `headword` -- the dictionary form (lemma) the token comes from.
  - `headword-meaning` -- gloss of the headword.
  - `attestation` -- one of:
    - `attested` (in Tolkien's own writings)
    - `neo-sindarin` (in Eldamo with a creator attribution)
    - `gnomish` or `noldorin` (revived from earlier Tolkien-stage material)
    - `quenya` (deliberate borrowing -- flag if not intentional)
    - `coined` (this translation, no external source)
    - `deprecated` (in Eldamo but flagged against)
  - `source` -- short citation (`PE17/174`, `Ety/SYAD`, `LotR/0305`,
    `Eldamo:ns`, `coined:this-file`).
  - `derivations[]` -- ordered list of grammatical moves from headword
    to surface form (imperative, lenition, compound, pluralization, etc.).
  - `rationale` -- why this word for this concept. Free text.

- `composition` -- prose explanation of how the elements fit together
  (mutations at boundaries, word order, agreement). Empty when trivial.

- `status` -- short tag summarizing the overall verdict:
  - `attested` -- all elements attested, no concerns.
  - `attested-components` -- elements attested, composition is new.
  - `defensible-neo-sindarin` -- uses recognized Neo-Sindarin patterns.
  - `coinage` -- contains a coinage worth flagging.
  - `needs-revision` -- known to have a problem (use with `concerns`).
  - `placeholder` -- not really translated yet; English passthrough or
    a guess to be revisited.

- `concerns` -- free text about what is uncertain or contested.

- `history[]` -- append-only log of significant changes. Date plus a
  one-line note. Don't restate what git can tell us; do capture *why*.

## Worked examples

### Simple (one element, no composition concerns)

```yaml
- key: BACK
  english: "Back"
  sjn:
    roman: "dan"
    literal: "back, against"
    tengwar: ""
  elements:
    - form: "dan"
      headword: "dan"
      headword-meaning: "back, against"
      attestation: attested
      source: "Ety/NDAN"
      derivations: []
      rationale: "Direct attested preposition; perfect semantic fit for navigation 'back'."
  status: attested
```

### Compound with intentional lenition

```yaml
- key: LIVE
  english: "Live"
  sjn:
    roman: "cîrwain"
    literal: "freshest, ever-new"
    tengwar: ""
  elements:
    - form: "cîr"
      headword: "cîr"
      headword-meaning: "renewed, fresh"
      attestation: attested
      source: "PE17/..."
      derivations: []
      rationale: "Attested word for fresh / renewed -- 'live' content is the freshest available."
    - form: "wain"
      headword: "gwain"
      headword-meaning: "new"
      attestation: attested
      source: "Narwain (LotR appendix D)"
      derivations:
        - "soft mutation in compound: gw- -> w- (g lenites to silence, w remains)"
      rationale: "Reinforces 'fresh / new' connotation in compound."
  composition: |
    Two synonyms compounded for emphasis. The g- of gwain lenites to
    silence inside the compound, leaving cîr-wain.
  status: attested-components
  concerns: ""
```

### Entry with known problem and proposed revision

```yaml
- key: PAUSE
  english: "Pause"
  sjn:
    roman: "daro"   # revised from earlier "hasto"
    literal: "halt"
    tengwar: "  "
  elements:
    - form: "daro"
      headword: "dar-"
      headword-meaning: "to halt, stop"
      attestation: attested
      source: "LotR/0339 (Haldir at Lothlorien border: 'Daro!')"
      derivations:
        - "imperative -o: dar- -> daro"
      rationale: |
        Attested in-canon imperative for 'halt!'. The most evocative
        possible choice given Tolkien used it for exactly this purpose.
  status: attested
  history:
    - date: 2022-01-15
      note: "Originally 'hasto' (intended pause/tarry)."
    - date: 2026-05-22
      note: "Replaced with 'daro' -- 'hasto' is attested but means 'hack through' (root SYAD), not pause."
```

### Placeholder for an untranslated string

```yaml
- key: PROGRESS_BAR_LABEL
  english: "Progress"
  sjn:
    roman: ""
    literal: ""
    tengwar: ""
  status: placeholder
  concerns: "Untranslated. Needs work."
```

## Migration notes

- `sync-sjn.py` currently does `destination[item["key"]] = item["sjn"]`.
  Update to `item["sjn"]["tengwar"]` (one-line change).
- The old `sjn-literal`, `sjn-roman`, `sjn` fields become
  `sjn.literal`, `sjn.roman`, `sjn.tengwar` -- moved under the `sjn` map.
- Migration can be done incrementally: a script can lift existing values
  into the new shape with empty `elements[]`, then we backfill elements
  per entry as we touch them (or as part of the glossary work).

## Why this shape rather than something denser

Considered alternatives:

- **Single string with inline annotations** -- impossible to validate or
  query.
- **Sidecar metadata file** -- breaks the locality between the
  translation and its justification; would drift.
- **Separate file per key** -- too many files for a ~50-entry locale.
- **Skip `elements`, just use freeform `notes`** -- works for now but
  loses the structure that lets a future skill validate each token
  against Eldamo automatically.

The per-element breakdown is the load-bearing addition. Everything else
is documentation that the translator was going to write somewhere anyway;
this just puts it next to the translation.
