# Translator intent: inferred reasoning behind each choice

This file documents what the original translator (Joey) appears to have
been doing when constructing each Sindarin translation, based on a
second-pass analysis against Eldamo. It is preserved as a record even for
entries we plan to update, so the reasoning is not lost.

Format: each entry notes the apparent intent, the grammatical/derivational
move involved, and a "verdict" of whether the entry should stand, stand with
a footnote, or be revised.

## Verb forms built by Neo-Sindarin causative pattern

### PLAY -- `northo`
- Built from attested `nor-` "to run" + Neo-Sindarin causative `-tha-`
  pattern (extended from Quenya `-ta-`) → `northa-` "to make run".
- Imperative ending `-o`: `northo`.
- The metaphor "play a video" = "make it run" is sound and matches English
  idiom.
- **Verdict**: defensible Neo-Sindarin. Keep.

### REPLAY -- `adnortho`
- Same as PLAY with attested `ad-` prefix "again, re-": `ad-` + `northa-`
  → `adnortha-`, imperative `adnortho`.
- **Verdict**: defensible. Keep.

### FAST_FORWARD -- `northo lim`
- Same `northo` verb; `lim` "swift" attested as adjective used adverbially.
- **Verdict**: keep.

### REWIND -- `northo abont`
- `northo` as above. `abont` is Gnomish "back, backwards" (GL/17), not
  Sindarin. The intent was to find a "backwards" adverb to pair with the
  verb.
- **Verdict**: revise. Replace `abont` with Sindarin `adel` "behind" or
  reconstruct `*ad-nor-` (already used for REPLAY though, so a different
  construction is needed -- perhaps `northo adel` "make-run behind").

## Verb forms with imperative `-o` on attested roots

### MUTE-related, ENTER, EXIT, LEAP, KEEP
- `minno` (enter) -- attested as imperative form in LotR. Correct.
- `cabo` (leap) -- imperative of attested `cab-` "leap". Correct paradigm.
- `garo` (keep) -- attested imperative of `gar-` "hold, have".
- `uthro` (escape) -- imperative of Neo-Sindarin `uthra-` "escape".
- `daro` -- not used yet, but is the attested halt-imperative (Haldir).
- **Verdict**: all defensible.

### PAUSE -- `hasto`
- Intent: imperative meaning "tarry/wait/pause".
- Problem: `hasto` IS attested (Etymologies, root SYAD), but means
  "hack through" not "pause". And the intended root for "halt" would yield
  `daro`, not `hasto`.
- **Verdict**: revise to `daro`.

### CAST -- `hanto`
- Intent: imperative of `had-` "to hurl, throw".
- The straight imperative is `hado`; `hanto` looks like an imperative built
  on the past stem `hant-` (nasal infixion past). This is a stretched but
  recognizable Neo-Sindarin move.
- **Verdict**: revise to `hado` for paradigm regularity, OR document
  `hanto` as a deliberate past-stem imperative if that was the intent.

## Compounds with proper lenition

### LIVE / SKIP_TO_LIVE -- `cîrwain`
- `cîr` (attested) + `gwain` "new" (attested).
- In compound, `g-` lenites to silence: `cîr-` + `gwain` → `cîrwain`.
- The lenition is applied correctly.
- **Verdict**: well-formed coinage. Keep, but mark as a deliberate
  neologism.

### ENTER_PIP / EXIT_PIP / PICTURE_IN_PICTURE -- `fanwos bir fanwos`
- `fanwos` IS attested (PE17/174) "mind-picture of apparition in dream".
  Excellent choice for "picture" with documented psychological imagery
  connotation.
- `bir` for "within": not attested, no mutation produces it from any
  attested preposition.
- **Verdict**: keep `fanwos`, revise `bir` to `mi`.

### SUBTITLE_FORCED -- `pith teithiel taug`
- `pith` = plural of `peth` "word" (attested pluralization).
- `teithiel` = attempt at past participle of `teitha-` "to write". The
  paradigmatic Sindarin past participle is `-en` sg / `-in` pl, so the
  plural-agreement form would be `teithennin`. The `-iel` ending is
  Quenya-influenced.
- `taug` "firm, abiding" attested.
- **Verdict**: keep all three lexemes; revise `teithiel` to `teithennin`
  for proper Sindarin participle morphology.

### CAPTIONS -- `pith teithiel`
- Same comments as SUBTITLE_FORCED on `teithiel`.

## Choices built from older Tolkien-stage material (Gnomish, etc.)

### NOT_APPLICABLE -- `la bâl`
- `bâl` is Gnomish "worthy, important; great, mighty" (GL/21, 23). Eldamo
  proposes a Neo-Root `BALAD` "worth, value" precisely for reviving such
  material. So `bâl` is a thought-through revival.
- `la` is Quenya negation; Sindarin uses `ú-` (with mutation) or
  independent `law` / `baw`.
- **Verdict**: keep `bâl` as deliberate Neo-Sindarin revival; revise `la`
  to `ú-` (giving e.g. `úval` after nasal mutation of b → m? Actually `ú-`
  + `bâl` would lenite to `úvâl`).

### OFF -- `unt`
- Gnomish "nothing" (cognate noted in Eldamo). Sindarin equivalent not
  cleanly attested; the user used the Gnomish form directly.
- **Verdict**: defensible as Gnomish revival, but flag.

### REWIND -- `abont`
- See above. Gnomish revival, less defensible because attested Sindarin
  `adel` is available.

## Lexical choices on attested roots

### AUTO_QUALITY -- `cammo`
- Attested verb `cam-` "to fit, suit, be agreeable, adapt" (VT44/14,
  VT47/20-21). Tolkien's primitive `kamta-` "to make fit, accommodate,
  adapt" is also attested.
- `cammo` as imperative is plausible (the doubled `mm` may come from a
  nasal-infixed past stem `camne-`/`camme-`).
- The semantic move "adapt → auto" is sound.
- **Verdict**: defensible Neo-Sindarin. Keep, document derivation.

### SURROUND -- `ostao`
- Attested Sindarin prefix `os-` "about, around" (cf. `osgar-` "amputate"
  = "cut around"). Neo-Sindarin verb `osta-` "to surround with walls,
  fortify" is in Eldamo (revived from Gnomish `osta-`, GL/63).
- `ostao` is the imperative of `osta-`.
- **Verdict**: defensible. Keep.

### ON -- `carweg`
- Attested adjective (PE17/144) "active, busy". Direct match.
- **Verdict**: keep.

### BACK -- `dan`
- Attested preposition "back, against".
- **Verdict**: keep.

### MUTE -- `dîn`
- Attested noun "silence" (cf. *Amon Dîn*).
- **Verdict**: keep.

### RECENTER_VR -- `ened`
- Attested "middle, center".
- **Verdict**: keep.

### QUALITY -- `aglar`
- Attested "glory, brilliance". Semantic stretch for "quality of video"
  but the connotation works.
- **Verdict**: keep, document as deliberate metaphor.

### VOLUME -- `brui`
- Attested "loud" (cf. river *Brui*).
- **Verdict**: keep.

### UNMUTE -- `lhôn`
- Attested form. Sense "sound, noise" plausible but not strongly
  attested.
- **Verdict**: keep tentatively; alternative `lamath` "echo, sound" worth
  considering.

### SEEK -- `lû`
- Attested "time, occasion". Metaphor: "seek" = "find a time/position".
- Collides with use of `lû` for "time" in AD_DURATION.
- **Verdict**: works but flag the collision.

### STATISTICS -- `cetho neth`
- `cetho`: imperative of Neo-Sindarin `ceth-` "examine, search,
  interrogate". Defensible.
- `neth`: intent was "numbers" -- perhaps a clipped form related to
  `nedia-` "to count" or attested `nediad` "counting" -- but `neth` IS a
  Sindarin word meaning "youth, girl". The homophone collision is
  unworkable.
- **Verdict**: keep `cetho`; revise `neth` to `gonod` "count" or
  `nediad` "counting".

### TOGGLE_STEREOSCOPIC -- `at-tírad`
- `at-` (attested prefix "again, double") + `tîr-` "watch" + `-ad`
  (gerund suffix). The hyphen is unusual; the t- following at- should
  lenite to th-, giving `athirad`.
- **Verdict**: revise spelling to `athirad`.

### UNDETERMINED / UNRECOGNIZED -- `la sinnen`
- `sinnen` is Neo-Sindarin "known" (Fiona Jallings).
- `la` is Quenya negation.
- **Verdict**: revise `la` to `ú-` → `úsinnen`. Same fix for both keys
  (they currently collapse to the same Sindarin; the English distinction
  may need a different word for one of them).

## Ad-related entries (recurring pattern)

The translator chose a distinctive coinage `hastië an mirian` for "ad",
literally "interruption for money". The components:

- `hast` attested noun "obstacle, hindrance"; `-ie` is a Quenya-style
  abstract noun ending (Sindarin would use `-as` or `-ath`). So `hastië`
  is a half-Sindarinized abstract from `hast`.
- `an` (attested preposition "for, to", triggers nasal mutation).
- `mirian` (attested Númenórean coin).

The phrase reads coherently as "interruption-thing for money", which is
a vivid (perhaps satirical) translation of "ad". Worth keeping as a
deliberate stylistic choice, even though `hastië` is a partial
Sindarinization.

- **Verdict**: keep as a signature coinage of this translation; document
  that `hastië` is a Sindarinized abstract on attested `hast`.

## Loop-related entries (Quenya intrusion)

LOOP / ENTER_LOOP_MODE / EXIT_LOOP_MODE all use forms of `enquet-`
("repeat") which is Quenya, AND deprecated within Eldamo's Quenya entries.
The intent was clearly "repeat / loop". Sindarin doesn't have an attested
verb meaning "repeat" directly; candidates:

- `ad-` + verb of speaking/doing: e.g., `adbeth-` "re-say" (unattested
  but transparent), `adgar-` "re-do".
- Use a circumlocution like "northo ad" "play again" (already used for
  REPLAY though).
- Coin a new verb: `*peliad` or similar.

- **Verdict**: needs a deliberate Sindarin alternative. Decision required.

## Items I genuinely could not parse

### MORE_SETTINGS -- `galainc`
- Cannot identify components. If `gal-` (light/grow) + something, the
  rest is opaque. Need the translator's original notes.

### CHAPTERS -- `tylme`
- Could maybe be read as i-affected plural of `*talm` (attested `talm`
  "foundation") with Quenya-ish `-e` ending, but uncertain. Original
  intent needed.

### RESOLUTION -- `meiras`
- Neo-Sindarin "value, preciousness" but flagged deprecated in Eldamo.
  Semantic match for "resolution" (display quality) is also a stretch.
- Needs replacement; suggest considering `lîn` (clear) family or `tîr`
  (vision-related).
