# Translation source-file schema (v1)

Recommended YAML structure for any Elvish translation project that wants
to record enough provenance to defend or critique each translation
choice. Versioned: this is v1, and may evolve as it gets exercised.

## Why this shape

A translation entry must answer three questions for a future reader:

1. **What does it say?** -- romanized form, script form, literal gloss.
2. **Why these specific words?** -- per-element attestation and
   rationale.
3. **How were they composed?** -- mutations, agreement, word order.

Without (2) and (3), a translator looking at an existing entry has to
re-derive the reasoning from scratch (or, worse, guess from grammar
alone). The fields below make that work persistent.

## Top-level shape (per entry)

```yaml
- key: PLAY
  english: "Play"

  sjn:
    roman: "northo"
    literal: "make-run"
    tengwar: "..."   # script-encoded form; edit with a Tengwar font

  elements:
    - form: "northo"
      headword: "nor-"
      headword-meaning: "to run"
      attestation: attested
      source: "Ety/NOR"
      derivations:
        - "causative -tha-: nor- -> northa- 'to make run' (Neo-Sindarin pattern, extended from Quenya -ta-)"
        - "imperative -o: northa- -> northo"
      rationale: "Metaphor: 'play a video' = 'make it run'. Parallels English idiom."

  composition: ""
  status: defensible-neo-sindarin
  concerns: |
    -tha- causative is reconstructed by extension from Quenya; not
    strictly attested in Sindarin. Common Neo-Sindarin pattern though.
  history:
    - date: 2022-01-15
      note: "Initial translation."
```

## Field reference

### Required

- `key` -- the localization key, matching whatever the consuming
  application expects.
- `english` -- the source string being translated.
- `sjn.roman` -- romanized translation. The form everyone reads.
- `sjn.tengwar` (or other script form) -- the script-encoded form, if
  the build pipeline needs one.

### Strongly recommended

- `sjn.literal` -- literal English back-translation. Lets a reviewer
  judge meaning without knowing Sindarin.

### Optional (the provenance fields)

- `elements[]` -- per-token breakdown, in order.
  - `form` -- the surface form as it appears in `sjn.roman`.
  - `headword` -- the dictionary lemma the token comes from.
  - `headword-meaning` -- gloss of the headword.
  - `attestation` -- one of:
    - `attested` -- in Tolkien's own writings.
    - `noldorin` -- attested in the earlier (1930s) Noldorin stage; may
      need adjustment for later Sindarin sound changes.
    - `gnomish` -- attested in the even earlier (1910s) Gnomish stage;
      use with caution.
    - `neo-sindarin` -- in Eldamo with a creator attribution.
    - `quenya` -- deliberate Quenya borrowing. Flag if accidental.
    - `coined` -- this translation, no external source.
    - `deprecated` -- present in references but flagged against.
  - `source` -- citation. `PE17/174`, `Ety/SYAD`, `LotR/0305`,
    `Eldamo:ns:by-Paul-Strack`, `coined:this-file`.
  - `derivations[]` -- ordered grammatical moves from headword to
    surface form (imperative, lenition, compound, pluralization, etc.).
    One step per line.
  - `rationale` -- why this word for this concept. Free text.

- `composition` -- prose for how the elements fit together: boundary
  mutations, word order rationale, agreement. Empty when trivial.

- `status` -- short tag summarizing the overall verdict:
  - `attested` -- all elements attested, no concerns.
  - `attested-components` -- elements attested, composition is new.
  - `defensible-neo-sindarin` -- uses recognized Neo-Sindarin patterns.
  - `coinage` -- contains a coinage worth flagging.
  - `needs-revision` -- known to have a problem (use with `concerns`).
  - `placeholder` -- not really translated yet; needs work.

- `concerns` -- free text about what is uncertain or contested.

- `history[]` -- append-only log of significant changes. Date plus a
  one-line note. Capture *why* changes were made, not what (git has
  what).

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
    roman: "daro"
    literal: "halt"
    tengwar: ""
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

## Alternatives considered

- **Single string with inline annotations** -- impossible to validate
  or query.
- **Sidecar metadata file** -- breaks the locality between the
  translation and its justification; will drift.
- **Separate file per key** -- too many files for a typical UI locale
  (~50-200 entries).
- **Skip `elements`, just use freeform `notes`** -- works initially
  but loses the structure that lets tools validate each token against
  the lexicon automatically.

The per-element breakdown is the load-bearing addition. Everything
else is documentation that a careful translator was going to write
somewhere anyway; this just puts it next to the translation.

## Versioning

This is v1. Likely evolution points:

- The `attestation` enum may grow (e.g. for languages other than
  Sindarin / Quenya).
- Tooling may want a `confidence` field separate from `status`.
- Multi-script projects (e.g. both Tengwar and Cirth) may want
  `sjn.tengwar` and `sjn.cirth` as a more general script map.

Project files should record which schema version they target, so
tools can adapt.
