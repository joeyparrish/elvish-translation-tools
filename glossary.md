# Sindarin Translation Glossary

Extracted from `ui/locales/sjn-translations.yaml` in shaka-player as of
2026-05-22. This is a snapshot of vocabulary choices made by the original
translator, not an endorsement of any of them. Each entry shows attestation
status against Eldamo (Paul Strack's lexicon, included under
`references/eldamo/`).

## Attestation legend

- `[ATT]`    -- attested in Tolkien's own writings (Sindarin or Noldorin).
- `[NS]`     -- Neo-Sindarin: post-Tolkien reconstruction or invention,
  recorded in Eldamo with a creator attribution.
- `[DEP]`    -- present in Eldamo but explicitly deprecated.
- `[COIN]`   -- coined for this translation, not in Eldamo.
- `[Q]`      -- Quenya word used as if Sindarin (mistake or stylistic choice).
- `[G]`      -- Gnomish (Tolkien's earliest language for the same world);
  not Sindarin.
- `[WRONG]`  -- attested in Sindarin but with a different meaning than used.

## Recurring lexemes

These appear in two or more entries and should be considered the
"established vocabulary" of the translation. New strings that touch the
same concepts should reuse these forms (or replace them everywhere if we
decide they are wrong).

### Verbs of motion / action

| Form | English used for | Status | Used in |
|------|------------------|--------|---------|
| `northo` | "play, make-run" (causative imperative of nor- "to run") | `[COIN]` form, root nor- is `[ATT]` | PLAY, FAST_FORWARD ("northo lim"), REWIND ("northo abont") |
| `adnortho` | "replay, make-run again" (ad- + northo) | `[COIN]` form, prefix ad- is `[ATT]` | REPLAY |
| `minno` | "enter" (imperative) | `[ATT]` (LotR, PE17, PE23) | ENTER_LOOP_MODE, ENTER_PICTURE_IN_PICTURE |
| `uthro` | "escape, exit" (imperative of uthra-) | `[COIN]` form, root uthra- is `[ATT]` Neo-Sindarin | EXIT_LOOP_MODE, EXIT_PIP, EXIT_FULL_SCREEN |
| `cabo` | "leap, skip" (imperative of cab-) | `[COIN]` form, root cab- is `[ATT]` | SKIP_AD, SKIP_TO_LIVE |
| `garo` | "keep, hold" (imperative of gar-) | `[ATT]` | DOWNLOAD_VIDEO_FRAME |

### Nouns and adjectives

| Form | English used for | Status | Used in |
|------|------------------|--------|---------|
| `fanwos` | "picture, frame, screen" (lit. "mind-picture of apparition in dream") | `[ATT]` (PE17/174) | DOWNLOAD_VIDEO_FRAME, ENTER_PIP, EXIT_PIP, PICTURE_IN_PICTURE, FULL_SCREEN, EXIT_FULL_SCREEN |
| `hastië` | "interruption, break" (used for "ad") | `[COIN]` (root hast "hindrance" attested, but this derivation is not) | AD_DURATION, AD_PROGRESS, AD_STATISTICS, AD_TIME, SKIP_AD |
| `mirian` | "money, coin" (a Númenórean coin) | `[ATT]` | AD_DURATION, AD_PROGRESS, AD_STATISTICS, AD_TIME, SKIP_AD |
| `pith teithiel` | "written words" (used for captions) | components `[ATT]`, agreement may be off (consider `pith teithennin` plural participle) | CAPTIONS, SUBTITLE_FORCED |
| `lambë` | "language" | `[Q]` — Quenya. Sindarin is `lam` / pl. `laim` / collective `lammath` | LANGUAGE, MULTIPLE_LANGUAGES |
| `cîrwain` | "freshest, live" | `[COIN]`; `cîr` and `gwain` ("new") are `[ATT]` but the compound is invented | LIVE, SKIP_TO_LIVE |
| `enquetië` / `enqueto` | "repetition / repeat" (used for loop) | `[Q]` AND `[DEP]` in Eldamo. Quenya `enquet-` is itself a deprecated form. | LOOP, ENTER_LOOP_MODE, EXIT_LOOP_MODE |

### Function words

| Form | English used for | Status | Used in |
|------|------------------|--------|---------|
| `la` | "not" (negation) | `[Q]` — Quenya. Sindarin uses prefix `ú-` (with mutation) or independent `law` / `baw`. | NOT_APPLICABLE, UNDETERMINED_LANGUAGE, UNRECOGNIZED_LANGUAGE |
| `an` | "for, to" (preposition, triggers nasal mutation) | `[ATT]` | AD_* entries, SKIP_AD |
| `bir` | "within, in" | `[COIN]` — no attestation. Standard Sindarin "in" is `mi` (no mutation) or `vi` (lenited). | PICTURE_IN_PICTURE, ENTER_PIP, EXIT_PIP |
| `na` | "to, with" (lenites following word) | `[ATT]` | SKIP_TO_LIVE ("na cîrwain") |
| `thar` | "across, over" | `[ATT]` | SKIP_AD ("cabo thar...") |

## Single-use lexemes

Listed by key. Status and any concerns flagged.

| Key | Sindarin | English gloss given | Status / notes |
|-----|----------|---------------------|----------------|
| BACK | `dan` | "return / back" | `[ATT]` (preposition "against, back"). Good fit. |
| AUTO_QUALITY | `cammo` | "adapt, make fit" | `[COIN]` — not in Eldamo. Consider attested alternatives. |
| CAST | `hanto` | "throw" | `[COIN]` — appears to be intended as imperative of `had-` "hurl" but the form is wrong; attested imperative would be `hado`. |
| CHAPTERS | `tylme` | "events" | `[COIN]` — not in Eldamo. Looks Quenya-influenced. |
| FAST_FORWARD | `northo lim` | "make-run fast" | `lim` "swift" is `[ATT]`. Adverbial use of adjective acceptable. |
| FULL_SCREEN | `fanwos panta` | "mind-picture full/open" | `panta` is `[Q]`. Sindarin is `pant`. |
| LIVE | `cîrwain` | "freshest" | See recurring. |
| MORE_SETTINGS | `galainc` | "more+choices" | `[COIN]` — opaque, can't parse the components. |
| MULTIPLE_LANGUAGES | `lambë arnoediad` | "language without count" | `arnoediad` `[ATT]` (cf. *Nírnaeth Arnoediad*). `lambë` is `[Q]`. |
| MUTE | `dîn` | "silence" | `[ATT]` (cf. *Amon Dîn*). Good fit. |
| NOT_APPLICABLE | `la bâl` | "not important" | `la` `[Q]`. `bâl` not in Eldamo. |
| OFF | `unt` | "nothing" | `[G]` — Gnomish, marked Neo-Sindarin in Eldamo via cognate. Tenuous. |
| ON | `carweg` | "active" | `[ATT]` (PE17/144) "active; busy". Strong choice. |
| PAUSE | `hasto` | "tarry/wait/pause" | `[WRONG]` — `hasto` IS attested but means "hack through" (root `SYAD`), not pause. The attested "halt" imperative is `daro` (LotR, Haldir in Lórien). |
| PICTURE_IN_PICTURE | `fanwos bir fanwos` | "picture within picture" | `bir` `[COIN]`; use `mi`. |
| PLAY | `northo` | "make-run" | See recurring. |
| PLAYBACK_RATE | `lintië` | "speed" | `[Q]`. Sindarin has `lint` "swift" attested; abstract `*lintad` or similar would be conjectural. |
| QUALITY | `aglar` | "brilliance / glory" | `[ATT]`. Semantic stretch (literally "glory, splendor"). |
| RECENTER_VR | `ened` | "center / middle" | `[ATT]`. Good fit. |
| REPLAY | `adnortho` | "make-run again" | See recurring. |
| RESOLUTION | `meiras` | "value, preciousness" | `[NS]` `[DEP]` — Neo-Sindarin and deprecated in Eldamo. Needs replacement. |
| REWIND | `northo abont` | "make-run backwards" | `abont` is `[G]` (Gnomish), not Sindarin. Sindarin "behind/back" is `adel`. |
| SEEK | `lû` | "time, occasion" | `[ATT]` but a stretch for "seek". Also reused as the noun in AD_DURATION, causing semantic overlap. |
| SKIP_AD | `cabo thar hastië an mirian` | "leap across break for money" | Components mostly OK; `hastië` is `[COIN]`. |
| SKIP_TO_LIVE | `cabo na cîrwain` | "leap to freshest" | See recurring. |
| STATISTICS | `cetho neth` | "interrogate numbers" | `ceth-` `[NS]` "examine, search, interrogate" (good). `neth` `[WRONG]` — `neth` in Sindarin means "youth, girl", not "number". Use `gonod` ("count, reckoning") or `nediad`. |
| SUBTITLE_FORCED | `pith teithiel taug` | "words written firm" | `taug` `[ATT]` "firm, abiding". |
| SURROUND | `ostao` | "surround" | `[COIN]` — not in Eldamo. |
| TOGGLE_STEREOSCOPIC | `at-tírad` | "double-seeing" | Components OK (`at(a)-` prefix `[ATT]`, `tîr-` `[ATT]`, `-ad` gerund). Hyphen unusual; with mutation should be `athirad` (`t-` lenites to `th-` after the prefix). |
| UNDETERMINED_LANGUAGE | `la sinnen` | "not known" | `la` `[Q]`. `sinnen` `[NS]` "known" (Fiona Jallings). Replace `la` with `ú-`: `úsinnen`. |
| UNMUTE | `lhôn` | "noise / sound" | `[ATT]` form. Sense is plausible but not strongly attested. Alternatives: `lamath` "echo, sound". |
| UNRECOGNIZED_LANGUAGE | `la sinnen` | (same as UNDETERMINED) | Same as above. The two English strings collapse to the same Sindarin. |
| VOLUME | `brui` | "loud, loudness" | `[ATT]` (cf. river *Brui*). |

## Summary statistics

- Entries: 41
- Recurring lexemes: 16 (used in 2+ entries)
- Attestation breakdown of distinct lexemes used:
  - `[ATT]` attested: ~22 (including roots whose imperatives are derived)
  - `[Q]` Quenya: 5 (`lambë`, `panta`, `enquet-`, `la`, `lintië`)
  - `[G]` Gnomish: 2 (`unt`, `abont`)
  - `[NS]` Neo-Sindarin: 3 (`ceth-`, `sinnen`, `uthra-`)
  - `[DEP]` deprecated in Eldamo: 2 (`enquet-`, `meiras`)
  - `[COIN]` coined / unattested: ~10 (`hastië`, `cîrwain`, `cammo`, `tylme`, `galainc`, `bir`, `ostao`, several imperative forms whose roots are attested but exact forms are not)
  - `[WRONG]` attested but wrong meaning: 2 (`hasto`, `neth`)

## Next questions to decide together

1. **`fanwos`**: keep it (attested) as our word for picture/screen/frame? It's
   actually well-grounded -- correcting my earlier critique.
2. **`hastië an mirian` for "ad"**: keep this distinctive coinage, or replace
   with something more attested?
3. **`lambë` → `lam`**: clear win to switch to attested Sindarin?
4. **`la` → `ú-`**: clear win to switch to Sindarin negation?
5. **`hasto` for pause**: replace with attested `daro` (clear win)?
6. **`neth` for number**: must replace (wrong meaning -- means "girl"). Use
   `gonod` or `nediad`.
7. **`enquet-` for loop**: must replace (Quenya, deprecated). Need a Sindarin
   alternative.
8. **`abont` for backwards**: replace with `adel` "behind" (Sindarin) or use a
   different construction.
9. **`meiras` for resolution**: replace (deprecated).
10. **`bir` → `mi`** for "in/within": clear win.
