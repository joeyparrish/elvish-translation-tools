# Tengwar CSUR codepoint reference

Source: Michael Everson, _Tengwar_ (draft proposal for ISO 10646),
2001-03-07. http://www.evertype.com/standards/iso10646/pdf/tengwar.pdf

Everson's proposal was never adopted into Unicode, but its codepoint
layout became the de facto allocation under the
[ConScript Unicode Registry](https://www.kreativekorp.com/ucsur/) for
Tengwar at **U+E000 – U+E07F** (the Private Use Area). Fonts that
support CSUR Tengwar (Tengwar Telcontar, Free Monospaced, others) use
this layout, and tools that produce CSUR output (Tecendil) target it.

If Tengwar is ever adopted into the official Unicode Standard, the
codepoints will move (Everson's proposal placed them in Plane 1); the
PUA layout below is the stable interim allocation. Anything we encode
in CSUR today should be straightforward to migrate when an official
codepoint is assigned.

## Codepoint table

### Tengwar (consonants and carriers) — U+E000 to U+E03A

| Codepoint | Name | Notes |
|---|---|---|
| U+E000 | TINCO | t |
| U+E001 | PARMA | p |
| U+E002 | CALMA | c, ch (English) |
| U+E003 | QUESSE | q, c (Quenya), k |
| U+E004 | ANDO | d |
| U+E005 | UMBAR | b |
| U+E006 | ANGA | j (English) |
| U+E007 | UNGWE | g |
| U+E008 | THUULE | th (also: suule) |
| U+E009 | FORMEN | f, ph |
| U+E00A | HARMA | sh, kh (also: aha) |
| U+E00B | HWESTA | ch (kh in Sindarin) |
| U+E00C | ANTO | dh |
| U+E00D | AMPA | v (also bh) |
| U+E00E | ANCA | j (English alt) |
| U+E00F | UNQUE | gh |
| U+E010 | NUUMEN | n |
| U+E011 | MALTA | m |
| U+E012 | NOLDO | ngold (also: ngoldo) |
| U+E013 | NWALME | ngw, ng (also: ngwalme) |
| U+E014 | OORE | r (weak / final r in Sindarin) |
| U+E015 | VALA | w (also v in some modes) |
| U+E016 | ANNA | y (consonantal) |
| U+E017 | VILYA | (also: wilya) |
| U+E018 – U+E01F | EXTENDED TINCO / PARMA / ... | series of extended-stem variants |
| U+E020 | ROOMEN | r (strong / initial r) |
| U+E021 | ARDA | rh (initial) |
| U+E022 | LAMBE | l |
| U+E023 | ALDA | lh (initial) |
| U+E024 | SILME | s |
| U+E025 | SILME NUQUERNA | s (inverted variant) |
| U+E026 | AARE | z (also: aaze, esse) |
| U+E027 | AARE NUQUERNA | z (inverted variant) |
| U+E028 | HYARMEN | h |
| U+E029 | HWESTA SINDARINWA | hw (Sindarin) |
| U+E02A | YANTA | (vowel carrier, glide) |
| U+E02B | UURE | (vowel carrier) |
| U+E02C | LONG CARRIER | bears long-vowel tehtar |
| U+E02D | (alternate position; see notes) | |
| U+E02E | SHORT CARRIER | bears short-vowel tehtar when no host |
| U+E031 | STEMLESS VALA | English [w] in some modes |
| U+E032 | STEMLESS ANNA | vowel in Beleriand mode |
| U+E034 | LIGATING SHORT CARRIER | |
| U+E035 | ANNA SINDARINWA | |
| U+E036 | OPEN ANNA | |
| U+E037 | REVERSED PARMA | |
| U+E038 | REVERSED FORMEN | |
| U+E039 | TALL STEMLESS VALA | |
| U+E03A | MH | nasalized m |

**Note on carrier positions:** the PDF lists LONG CARRIER at xx2C and
SHORT CARRIER at xx2E. python-tengwar's `unicode_mappings` table
places LongCarrier at U+E02D and ShortCarrier at U+E02E. Test against
the actual font before committing to one or the other for the engine.

### Tehtar (vowel and modifier signs) — U+E040 to U+E057

| Codepoint | Name | Notes |
|---|---|---|
| U+E040 | THREE DOTS ABOVE | a (most common) |
| U+E041 | THREE DOTS BELOW | a (Beleriand variant) |
| U+E042 | TWO DOTS ABOVE | i (or y in Sindarin) |
| U+E043 | TWO DOTS BELOW | |
| U+E044 | AMATICSE (dot above) | i |
| U+E045 | NUNTICSE (dot below) | |
| U+E046 | ACUTE (andaith, long mark) | e; or marks long vowels |
| U+E048 | DOUBLE ACUTE | |
| U+E049 | DOUBLE ACUTE BELOW | |
| U+E04A | RIGHT CURL | o |
| U+E04B | RIGHT CURL BELOW | |
| U+E04C | LEFT CURL | u |
| U+E04D | LEFT CURL BELOW | |
| U+E04E | DOUBLE RIGHT CURL | |
| U+E04F | DOUBLE LEFT CURL | |
| U+E050 | NASALIZER | bar-above; marks preceding nasal |
| U+E051 | DOUBLER | bar-below; doubles the consonant |
| U+E052 | TILDE | over-twist; labialization (gw, etc.) |
| U+E053 | BREVE | |
| U+E054 | GRAVE | |
| U+E055 | YANTA ABOVE | |
| U+E056 | THREE INVERTED DOTS ABOVE | |
| U+E057 | LONG CARRIER BELOW | |

### Punctuation — U+E060 to U+E068

| Codepoint | Name |
|---|---|
| U+E060 | PUSTA (full stop) |
| U+E061 | DOUBLE PUSTA |
| U+E062 | TRIPLE PUSTA |
| U+E063 | QUADRUPLE PUSTA |
| U+E064 | QUINTUPLE PUSTA |
| U+E065 | EXCLAMATION MARK |
| U+E066 | QUESTION MARK |
| U+E067 | PARENTHESIS MARK |
| U+E068 | SECTION MARK |

### Digits — U+E070 to U+E07D

| Codepoint | Name |
|---|---|
| U+E070 – U+E079 | DIGIT ZERO through DIGIT NINE |
| U+E07A | DUODECIMAL DIGIT TEN |
| U+E07B | DUODECIMAL DIGIT ELEVEN |
| U+E07C | DUODECIMAL DIGIT TWELVE |
| U+E07D | DUODECIMAL LEAST SIGNIFICANT DIGIT MARK |

Tengwar digits are written right-to-left (least-significant first),
unlike normal Tengwar text.

## Encoding conventions

### Combining order

Each tengwa is followed in the byte stream by its associated tehtar.
The font renders the tehtar as combining diacritics on the preceding
tengwa. So `{ando}[acute]` (d + e-tehta) outputs `U+E004 U+E046`,
which the font renders as a single composed glyph: d with the e-mark.

### Carriers

When a tehta has no consonant to attach to (initial vowel before
another vowel, final vowel after no consonant, isolated vowel), it
attaches to a carrier:

- SHORT CARRIER bears a short-vowel tehta.
- LONG CARRIER bears a long-vowel tehta (or use SHORT CARRIER plus the
  long-acute mark, depending on mode).

### Modes

The same Tengwar character stream can be rendered three different ways
depending on font mode:

- **Quenya mode**: tehtar attach to the _preceding_ tengwa (CV
  syllable bias).
- **Sindarin mode**: tehtar attach to the _following_ tengwa (CVC
  syllable bias). This is the mode our translations target.
- **Beleriand mode**: vowels written as full tengwar in their own
  right, not as tehtar.

The mode is a font-level property. The underlying character stream is
the same; the mode determines glyph selection and tehta placement.

## Cross-reference: Tecendil mode-file names

Tecendil's mode files (`sindarin.jsonc`, etc.) use symbolic names like
`{nuumen}` and `[acute]` that map to CSUR codepoints. The mapping is
mostly transparent (`nuumen` → NUUMEN at U+E010), with a handful of
divergences:

| Tecendil name | CSUR codepoint | Everson name |
|---|---|---|
| `aara` | U+E02C or U+E02D | LONG CARRIER (used as long-vowel host) |
| `telco` | U+E02E | SHORT CARRIER |
| `esse-nuquerna` | U+E027 | AARE NUQUERNA |
| `malta-with-curl` | U+E03A | MH |
| `bar-above` | U+E050 | NASALIZER |
| `bar-below` | U+E051 | DOUBLER |
| `over-twist` | U+E052 (likely) | TILDE — needs verification |
| `bar-inside` | U+E051 + lambe (likely, OpenType variant) | DOUBLER applied to LAMBE — needs verification |
| `dash` | (likely literal `-`, U+002D) | needs verification |

The three "needs verification" entries are open questions to resolve
by running known input through Tecendil and inspecting the output.

## What this reference is for

This is the codepoint-level authority for any CSUR Tengwar work in
this repo: the `sjn.tengwar` field convention in
[`translation-schema.md`][schema], the in-progress transliteration
engine, and any future Quenya / Beleriand / other-mode work. The
table above is faithful to the Everson PDF and should not need
updates unless either:

1. CSUR formally extends the Tengwar block, or
2. Tengwar is adopted into official Unicode (at which point this doc
   describes the legacy PUA encoding for migration).

[schema]: ./translation-schema.md
