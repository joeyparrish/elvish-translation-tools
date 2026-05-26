#!/usr/bin/env python3
# Copyright 2026 Joey Parrish
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Transliterate romanized Elvish into CSUR Tengwar codepoints.

Reads a Tecendil-format mode file from data/modes/ and applies its
rules to produce CSUR Tengwar output (U+E000-U+E07F).

Usage:
    python3 scripts/transliterate.py sjn "northo lim"
    python3 scripts/transliterate.py qya "alcarin"

See references/tengwar-csur.md for the codepoint authority and rule
semantics, references/translation-schema.md for the schema's
expectation on the sjn.tengwar field.
"""

import argparse
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODES_DIR = os.path.join(BASE, "data", "modes")

# Mode short codes -> mode file basenames.
MODE_ALIASES = {
    "sjn": "sindarin",
    "sindarin": "sindarin",
    "qya": "quenya",
    "quenya": "quenya",
    "beleriand": "beleriand",
}

# CSUR Tengwar codepoint table, indexed by Tecendil's symbolic names.
# Extracted from the deployed Tecendil bundle, cross-checked against
# Michael Everson's 2001 CSUR Tengwar proposal (see references/
# tengwar-csur.md). Entries verified empirically appear in tests.md.
#
# Codepoints are written as \uXXXX escapes so this source is reviewable
# in any editor. The actual characters are in the Unicode Private Use
# Area (U+E000-U+E07F) and render as boxes without a CSUR-aware font.
NAME_TO_CSUR = {
    # Tengwar (consonants and carriers) at U+E000-U+E03A
    "tinco":              "\uE000",
    "parma":              "\uE001",
    "calma":              "\uE002",
    "quesse":             "\uE003",
    "ando":               "\uE004",
    "umbar":              "\uE005",
    "anga":               "\uE006",
    "ungwe":              "\uE007",
    "thuule":             "\uE008",
    "formen":             "\uE009",
    "harma":              "\uE00A",
    "hwesta":             "\uE00B",
    "anto":               "\uE00C",
    "ampa":               "\uE00D",
    "anca":               "\uE00E",
    "unque":              "\uE00F",
    "nuumen":             "\uE010",
    "malta":              "\uE011",
    "noldo":              "\uE012",
    "nwalme":             "\uE013",
    "oore":               "\uE014",
    "vala":               "\uE015",
    "anna":               "\uE016",
    "vilya":              "\uE017",
    "roomen":             "\uE020",
    "arda":               "\uE021",
    "lambe":              "\uE022",
    "alda":               "\uE023",
    "silme":              "\uE024",
    "silme-nuquerna":     "\uE025",
    "esse":               "\uE026",
    "esse-nuquerna":      "\uE027",
    "hyarmen":            "\uE028",
    "hwesta-sindarinwa":  "\uE029",
    "yanta":              "\uE02A",
    "uure":               "\uE02B",
    "aara":               "\uE02C",  # LONG CARRIER
    "halla":              "\uE02D",
    "telco":              "\uE02E",  # SHORT CARRIER
    "osse":               "\uE032",  # STEMLESS ANNA per Everson
    "malta-with-curl":    "\uE03A",  # MH per Everson

    # Tehtar (vowel and modifier signs) at U+E040-U+E057
    "triple-dot-above":   "\uE040",
    "double-dot-above":   "\uE042",
    "double-dot-below":   "\uE043",  # also rendered as "double-dot-inside" in Sindarin context
    "double-dot-inside":  "\uE043",
    "dot-above":          "\uE044",
    "dot-below":          "\uE045",
    "dot-below-after":    "\uE045",
    "acute":              "\uE046",
    "right-curl":         "\uE04A",
    "left-curl":          "\uE04C",
    "bar-above":          "\uE050",  # NASALIZER
    "bar-below":          "\uE051",  # DOUBLER
    "bar-inside":         "\uE051",  # same codepoint; font handles positioning
    "tilde-above":        "\uE050",
    "tilde-below":        "\uE051",
    "tilde-high":         "\uE050",
    "over-twist":         "\uE052",  # TILDE; used for labialization
    "breve":              "\uE053",
    "grave":              "\uE054",
    "thinnas":            "\uE057",
    "hook":               "\uE058",
    "dot-inside":         "\uE05A",

    # Punctuation at U+E060-U+E068
    "pusta":              "\uE060",
    "full-stop":          "\uE060",
    "dash":               "",        # empirically swallowed by Tecendil

    # Digits at U+E070-U+E07B
    "zero":               "\uE070",
    "one":                "\uE071",
    "two":                "\uE072",
    "three":              "\uE073",
    "four":               "\uE074",
    "five":               "\uE075",
    "six":                "\uE076",
    "seven":              "\uE077",
    "eight":              "\uE078",
    "nine":               "\uE079",
    "ten":                "\uE07A",
    "eleven":             "\uE07B",
}

# Default short-vowel-to-tehta mapping, used when the mode's `map`
# doesn't override a vowel. Discovered empirically in Tecendil's
# engine: short vowels with no explicit rule fall through to this.
DEFAULT_VOWEL_TEHTAR = {
    "a": "[triple-dot-above]",
    "e": "[acute]",
    "i": "[dot-above]",
    "o": "[right-curl]",
    "u": "[left-curl]",
    "y": "[double-dot-below]",  # Sindarin overrides to double-dot-above
}

# Tehta position classes. Two tehtar in the same class conflict (the
# accumulator must be flushed via telco before adding the second);
# tehtar in different classes coexist on the same tengwa.
#
# Nasal marker (bar-above) and labial marker (over-twist) are
# independent of each other and of vowel tehtar -- they can all stack
# on a single tengwa (e.g. UNGWE for 'angw' carries nasal + labial +
# vowel marks).
TEHTA_POSITION = {
    "triple-dot-above":     "above",
    "double-dot-above":     "above",
    "dot-above":            "above",
    "acute":                "above",
    "right-curl":           "above",
    "left-curl":            "above",
    "triple-dot-below":     "below",
    "double-dot-below":     "below",
    "dot-below":            "below",
    "acute-below":          "below",
    "right-curl-below":     "below",
    "left-curl-below":      "below",
    "bar-above":            "nasal",
    "tilde-above":          "nasal",
    "over-twist":           "labial",
    "bar-below":            "doubler",
    "tilde-below":          "doubler",
    "bar-inside":           "doubler",
    "dot-inside":           "other",
    "double-dot-inside":    "other",
}


def is_word_char(c):
    return c.isalpha() or c in "âêîôûŷœæ"


def strip_jsonc_comments(text):
    """Strip // line comments and /* block */ comments, respecting strings."""
    out = []
    i = 0
    in_str = False
    in_block = False
    while i < len(text):
        c = text[i]
        if in_block:
            if c == "*" and i + 1 < len(text) and text[i+1] == "/":
                in_block = False
                i += 2
                continue
            # Preserve newlines so error messages keep line numbers
            if c == "\n":
                out.append(c)
            i += 1
            continue
        if in_str:
            if c == "\\" and i + 1 < len(text):
                out.append(c)
                out.append(text[i+1])
                i += 2
                continue
            if c == '"':
                in_str = False
            out.append(c)
            i += 1
        else:
            if c == '"':
                in_str = True
                out.append(c)
                i += 1
            elif c == "/" and i + 1 < len(text):
                if text[i+1] == "/":
                    while i < len(text) and text[i] != "\n":
                        i += 1
                elif text[i+1] == "*":
                    in_block = True
                    i += 2
                else:
                    out.append(c)
                    i += 1
            else:
                out.append(c)
                i += 1
    return "".join(out)


def load_mode(mode_name):
    """Load a JSONC mode file."""
    basename = MODE_ALIASES.get(mode_name, mode_name)
    path = os.path.join(MODES_DIR, f"{basename}.jsonc")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return json.loads(strip_jsonc_comments(text))


def compile_rule_key(key):
    """Parse a rule key into (kind, payload).

    Kinds:
      ("regex", compiled_pattern)
      ("literal", text, anchor_start_bool, anchor_end_bool)
    """
    if key.startswith("/"):
        last = key.rindex("/")
        pattern = key[1:last]
        return ("regex", re.compile(pattern))
    anchor_start = key.startswith("^")
    anchor_end = key.endswith("$")
    literal = key
    if anchor_start:
        literal = literal[1:]
    if anchor_end:
        literal = literal[:-1]
    return ("literal", literal, anchor_start, anchor_end)


def compile_rules(rules_dict):
    """Compile all rules into a list preserving file order."""
    out = []
    for key, value in rules_dict.items():
        out.append((compile_rule_key(key), value))
    return out


def apply_preprocess(text, preprocess):
    """Run all preprocess rules over the input text.

    We skip the literal `"-": " "` rule because empirically Tecendil
    preserves trailing dashes for the `ia-$` rule. The other preprocess
    rules (ligature expansion, qu->q, etc.) are still applied.
    """
    for key, value in preprocess.items():
        if key == "-":
            continue  # see docstring
        if key.startswith("/"):
            last = key.rindex("/")
            pat = re.compile(key[1:last])
            text = pat.sub(value, text)
        else:
            text = text.replace(key, value)
    return text


# Default vowel normalization. Per the Tecendil bundle, when a mode
# has normalizeVowels:true the engine collapses long-vowel notations
# into the circumflex forms, plus strips the diaeresis from short
# vowels (which Quenya uses to mark word-final pronunciation).
NORMALIZE_VOWELS = [
    (re.compile(r"ā|á|aa"), "â"),
    (re.compile(r"ē|é|ee"), "ê"),
    (re.compile(r"ī|í|ii"), "î"),
    (re.compile(r"ō|ó|oo"), "ô"),
    (re.compile(r"ū|ú|uu"), "û"),
    (re.compile(r"ȳ|ý|yy"), "ŷ"),
    # Strip diaeresis (Quenya pronunciation marker; not phonetic)
    (re.compile(r"ë"), "e"),
    (re.compile(r"ï"), "i"),
    (re.compile(r"ä"), "a"),
    (re.compile(r"ö"), "o"),
    (re.compile(r"ü"), "u"),
]


def normalize_vowels(text):
    for pat, rep in NORMALIZE_VOWELS:
        text = pat.sub(rep, text)
    return text


# Sentinel that marks "the next tengwa emitted should use the uppercase
# (capital) CSUR variant at +0x80 from its lowercase codepoint".
# Used by handle_capitals.
UPPER_MARK = "\x01"


def handle_capitals(text):
    """Lowercase all letters; insert UPPER_MARK before word-initial capitals.

    Tecendil renders a word with an uppercase first letter using its
    extended CSUR range (U+E080-U+E0AE): each uppercase tengwa lives at
    its lowercase codepoint + 0x80. So `Rohan` -> uppercase ROOMEN
    (U+E0A0) + lowercase rest; `Eldamar` -> uppercase TELCO carrier
    (U+E0AE) + lowercase rest.

    We implement this by lowercasing the input (so all the regular
    rules fire normally) and inserting an UPPER_MARK sentinel
    immediately before each word-initial uppercase letter. The
    sentinel passes through the rule application and tehta positioning
    unchanged; to_csur converts the next tengwa to its uppercase
    variant when it sees the mark.

    Mid-word uppercase letters are lowercased silently with no mark
    (rare in Elvish romanization, mostly an input quirk).
    """
    out = []
    at_word_start = True
    for c in text:
        is_letter = c.isalpha() or c in WORD_CHARS_NON_ASCII
        if c.isupper() and at_word_start:
            out.append(UPPER_MARK)
        out.append(c.lower() if c.isupper() else c)
        at_word_start = not is_letter
    return "".join(out)


def uppercase_tengwa(cp):
    """Return the uppercase-variant codepoint for a lowercase tengwa.

    Tengwar at U+E000-U+E03F have uppercase variants at +0x80
    (Tecendil's extension to CSUR). Tehtar and other codepoints have
    no uppercase variant; they are returned unchanged.
    """
    o = ord(cp)
    if 0xE000 <= o <= 0xE03F:
        return chr(o + 0x80)
    return cp


def apply_word_overrides(text, words):
    """Whole-word substitutions from the mode's `words` dict.

    Matches Tecendil's behavior: the lookup is case-insensitive against
    the LOWERCASED key. Override keys that contain uppercase letters
    are effectively dead in Tecendil (it does
    `words[input.toLowerCase()]`, which never matches a capitalized
    key); we honor that behavior.

    If a replacement value contains symbolic-stream markers ({...} or
    [...]), it is treated as a literal symbolic stream and protected
    from further rule application by wrapping in a sentinel.
    """
    for word, replacement in words.items():
        if word != word.lower():
            continue  # dead override per Tecendil's case-sensitive lookup miss
        # Case-insensitive whole-word match. \b doesn't handle non-ASCII
        # word chars (â, î, ŷ...) well, so use lookarounds.
        pattern = r"(?<![\w" + WORD_CHARS_NON_ASCII + r"])" + \
                  re.escape(word) + \
                  r"(?![\w" + WORD_CHARS_NON_ASCII + r"])"
        if any(c in "{[" for c in replacement):
            # Symbolic stream: protect from rule application with a
            # sentinel that apply_rules passes through unchanged.
            text = re.sub(pattern, SENTINEL_OPEN + replacement + SENTINEL_CLOSE,
                          text, flags=re.IGNORECASE)
        else:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


# Non-ASCII word characters used in Elvish romanization (long vowels,
# y-with-macron, ligatures).
WORD_CHARS_NON_ASCII = "âêîôûŷœæáéíóúýÁÉÍÓÚÝÂÊÎÔÛŸ"

# Sentinels for protecting symbolic-stream word overrides from the rule
# applier. apply_rules emits these spans verbatim; the final tokenizer
# unwraps them and the contents are read as symbolic tokens.
SENTINEL_OPEN = "\x00<"
SENTINEL_CLOSE = ">\x00"


def apply_rules(text, compiled_rules):
    """Walk text left to right. At each position pick the best matching rule.

    Selection order (higher beats lower):
      1. anchored rules (^/$) beat unanchored
      2. longer match beats shorter
      3. earlier-in-file beats later (tiebreaker)

    This matches Tecendil's behavior: '^ang' (anchored) wins over the
    later, unanchored 'angw' rule even though it's shorter; but 'gw'
    (unanchored, length 2) beats 'g' (unanchored, length 1).

    Symbolic-stream sentinels (from word overrides whose value is a
    symbolic stream) are passed through verbatim.
    """
    output = []
    i = 0
    n = len(text)
    while i < n:
        # Pass-through for symbolic-stream sentinels. Preserve the
        # sentinel markers so downstream passes (position_tehtar) know
        # not to process the contents.
        if text.startswith(SENTINEL_OPEN, i):
            end = text.index(SENTINEL_CLOSE, i)
            output.append(text[i:end + len(SENTINEL_CLOSE)])
            i = end + len(SENTINEL_CLOSE)
            continue
        # Find best matching rule at position i.
        best = None  # (score, length, replacement)
        for idx, (key, value) in enumerate(compiled_rules):
            if key[0] == "regex":
                _, pat = key
                m = pat.match(text, i)
                if not m:
                    continue
                length = m.end() - i
                replacement = pat.sub(value, m.group(0))
                anchored = 0
            else:
                _, lit, anchor_start, anchor_end = key
                if anchor_start and i > 0 and is_word_char(text[i-1]):
                    continue
                end = i + len(lit)
                if end > n or text[i:end] != lit:
                    continue
                if anchor_end and end < n and is_word_char(text[end]):
                    continue
                length = len(lit)
                replacement = value
                anchored = 1 if (anchor_start or anchor_end) else 0
            score = (anchored, length, -idx)
            if best is None or score > best[0]:
                best = (score, length, replacement)
        if best is not None:
            _, length, replacement = best
            output.append(replacement)
            i += length
        else:
            c = text[i]
            lc = c.lower()
            if lc in DEFAULT_VOWEL_TEHTAR:
                output.append(DEFAULT_VOWEL_TEHTAR[lc])
            else:
                output.append(c)
            i += 1
    return "".join(output)


def tokenize_symbolic(s):
    """Yield (kind, value) tokens from a symbolic stream.

    Empty tengwa `{}` is yielded with an empty value so callers can
    decide what to do (to_csur treats it as a no-op placeholder).
    Empty tehta `[]` is silently dropped (it's how Tecendil represents
    'no tehta here').
    """
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == "{":
            end = s.index("}", i)
            yield ("tengwa", s[i+1:end])
            i = end + 1
        elif c == "[":
            end = s.index("]", i)
            name = s[i+1:end]
            if name:
                yield ("tehta", name)
            i = end + 1
        else:
            yield ("text", c)
            i += 1


def tehtar_conflict(a, b):
    return TEHTA_POSITION.get(a, "above") == TEHTA_POSITION.get(b, "above")


def context_substitute(tengwa_name, tehta_name):
    """Tecendil's context substitutions: certain tehtar change name when applied to lambe."""
    if tengwa_name == "lambe":
        if tehta_name == "bar-below":
            return "bar-inside"
        if tehta_name == "dot-below":
            return "dot-inside"
    return tehta_name


# Order of tehtar within one tengwa's output. Tecendil emits in this
# order: nasal marker, labial marker, below tehtar, above tehtar,
# doubler/other. The visual stacking is handled by the font.
TEHTA_EMIT_ORDER = {
    "nasal":   0,  # bar-above
    "labial":  1,  # over-twist
    "below":   2,
    "above":   3,  # vowel tehtar
    "doubler": 4,  # bar-below, bar-inside
    "other":   5,
}


def sort_tehtar(tehtar):
    """Sort tehtar by Tecendil's canonical emission order; stable on ties."""
    return sorted(
        enumerate(tehtar),
        key=lambda x: (TEHTA_EMIT_ORDER.get(
            TEHTA_POSITION.get(x[1], "above"), 99), x[0]),
    )


def maybe_promote_silme_nuquerna(tengwa_name, tehtar):
    """If silme would carry an 'above'-class tehta, switch to silme-nuquerna.

    The inverted form leaves clean space below for the tehta. This is a
    Tecendil convention also seen in mode rules like 'ans' -> ...
    {silme-nuquerna}.
    """
    if tengwa_name != "silme":
        return tengwa_name
    has_above_tehta = any(
        TEHTA_POSITION.get(t, "above") == "above" for t in tehtar)
    return "silme-nuquerna" if has_above_tehta else tengwa_name


def position_tehtar(symbolic, tehtar_follow):
    """Apply tehtarFollow placement, producing a refined symbolic stream
    where each tehta is bound to its host tengwa (with a telco as fallback).

    Sentinel-wrapped regions (from symbolic-stream word overrides) are
    passed through verbatim -- the override author is trusted to have
    placed the tehtar correctly; reapplying tehtarFollow would shift
    them incorrectly.
    """
    # Split on sentinels so we can pass-through override regions.
    # Each segment is either a sentinel block (str starting with SENTINEL_OPEN)
    # or a normal symbolic substring to process.
    out_parts = []
    i = 0
    while i < len(symbolic):
        si = symbolic.find(SENTINEL_OPEN, i)
        if si < 0:
            out_parts.append(_position_segment(symbolic[i:], tehtar_follow))
            break
        # Process the leading normal segment
        if si > i:
            out_parts.append(_position_segment(symbolic[i:si], tehtar_follow))
        # Then pass through the override region verbatim (sans markers).
        sj = symbolic.index(SENTINEL_CLOSE, si)
        out_parts.append(symbolic[si + len(SENTINEL_OPEN):sj])
        i = sj + len(SENTINEL_CLOSE)
    return "".join(out_parts)


def _position_segment(symbolic, tehtar_follow):
    """Position-tehtar for a single segment (no embedded sentinels)."""
    tokens = list(tokenize_symbolic(symbolic))
    out = []
    acc = []  # pending tehtar

    def emit_carrier():
        if acc:
            ordered = [acc[i] for i, _ in sort_tehtar(acc)]
            out.append("{telco}" + "".join(f"[{t}]" for t in ordered))
            acc.clear()

    def emit_tengwa(name):
        # Tecendil promotes silme -> silme-nuquerna when it carries an
        # above-class tehta.
        name = maybe_promote_silme_nuquerna(name, acc)
        substituted = [context_substitute(name, t) for t in acc]
        ordered = [substituted[i] for i, _ in sort_tehtar(substituted)]
        out.append("{" + name + "}" + "".join(f"[{t}]" for t in ordered))
        acc.clear()

    if tehtar_follow:
        for kind, value in tokens:
            if kind == "tehta":
                if any(tehtar_conflict(t, value) for t in acc):
                    emit_carrier()
                acc.append(value)
            elif kind == "tengwa":
                emit_tengwa(value)
            else:  # text
                emit_carrier()
                out.append(value)
        emit_carrier()
    else:
        # tehtarFollow:false (Quenya): tehta attaches to previous tengwa.
        prev = None
        def emit_prev():
            nonlocal prev
            # Treat empty-string prev (from `{}` placeholder) as no prev:
            # the trailing tehtar fall back to a telco carrier rather
            # than attaching to an invisible "no tengwa".
            if prev:
                p = maybe_promote_silme_nuquerna(prev, acc)
                substituted = [context_substitute(p, t) for t in acc]
                ordered = [substituted[i] for i, _ in sort_tehtar(substituted)]
                out.append("{" + p + "}" + "".join(f"[{t}]" for t in ordered))
                prev = None
                acc.clear()
            elif acc:
                ordered = [acc[i] for i, _ in sort_tehtar(acc)]
                out.append("{telco}" + "".join(f"[{t}]" for t in ordered))
                acc.clear()
            elif prev == "":
                # Empty placeholder with no pending tehtar: just clear.
                prev = None
        for kind, value in tokens:
            if kind == "tehta":
                if any(tehtar_conflict(t, value) for t in acc):
                    emit_prev()
                acc.append(value)
            elif kind == "tengwa":
                emit_prev()
                prev = value
            else:
                emit_prev()
                out.append(value)
        emit_prev()

    return "".join(out)


def to_csur(symbolic):
    """Convert symbolic stream to CSUR codepoints.

    Sentinel-wrapped regions (from symbolic-stream word overrides) are
    unwrapped here -- the markers themselves are skipped, and the
    contents (already symbolic tokens) flow through normally.

    Empty tengwa `{}` and the `dash` token both emit nothing -- they're
    used as no-op placeholders by Tecendil's rules (e.g. the trailing
    `{}` in `"ri" -> "{roomen}[dot-above]{}"`).
    """
    # Strip sentinel markers before tokenizing -- the contents are
    # already pre-positioned symbolic tokens that should pass through.
    symbolic = symbolic.replace(SENTINEL_OPEN, "").replace(SENTINEL_CLOSE, "")
    parts = []
    upper_next = False
    for kind, value in tokenize_symbolic(symbolic):
        if kind == "text" and value == UPPER_MARK:
            upper_next = True
            continue
        if kind == "tengwa":
            if value == "" or value == "dash":
                continue  # no-op placeholder
            cp = NAME_TO_CSUR.get(value)
            if cp is None:
                raise ValueError(f"Unknown tengwa name: {value!r}")
            if upper_next:
                cp = uppercase_tengwa(cp)
                upper_next = False
            parts.append(cp)
        elif kind == "tehta":
            cp = NAME_TO_CSUR.get(value)
            if cp is None:
                raise ValueError(f"Unknown tehta name: {value!r}")
            parts.append(cp)
        else:
            parts.append(value)
    return "".join(parts).rstrip()


def transliterate(text, mode):
    # Protect UI placeholders like [VARIABLE] (all-caps + underscores
    # inside square brackets) so they pass through verbatim instead
    # of being parsed as tehta tokens or mangled by handle_capitals.
    placeholders, text = extract_placeholders(text)
    text = handle_capitals(text)
    text = apply_preprocess(text, mode.get("preprocess", {}))
    if mode.get("normalizeVowels"):
        text = normalize_vowels(text)
    text = apply_word_overrides(text, mode.get("words", {}))
    rules = compile_rules(mode.get("map", {}))
    symbolic = apply_rules(text, rules)
    positioned = position_tehtar(symbolic, mode.get("tehtarFollow", False))
    out = to_csur(positioned)
    out = restore_placeholders(out, placeholders)
    return out


PLACEHOLDER_PATTERN = re.compile(r"\[[A-Z][A-Z0-9_]*\]")
PLACEHOLDER_SENTINEL = "\x02"


def extract_placeholders(text):
    """Replace [VAR] placeholders with sentinel markers; return them too."""
    placeholders = []
    def collect(m):
        placeholders.append(m.group(0))
        return PLACEHOLDER_SENTINEL
    new_text = PLACEHOLDER_PATTERN.sub(collect, text)
    return placeholders, new_text


def restore_placeholders(text, placeholders):
    """Restore [VAR] placeholders from sentinel markers in order."""
    parts = text.split(PLACEHOLDER_SENTINEL)
    out = [parts[0]]
    for ph, part in zip(placeholders, parts[1:]):
        out.append(ph)
        out.append(part)
    return "".join(out)


def escape_csur(s):
    r"""Render a CSUR string with PUA characters as \uXXXX escapes.

    Non-PUA characters (ASCII letters, spaces, etc.) pass through
    literally. Tengwar codepoints (U+E000-U+E0FF) become escape
    sequences. The result is a string that's reviewable in any editor
    and is identical to its decoded form when read as Python or YAML
    double-quoted source.
    """
    out = []
    for c in s:
        o = ord(c)
        if 0xE000 <= o <= 0xE0FF:
            out.append(f"\\u{o:04X}")
        else:
            out.append(c)
    return "".join(out)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "mode",
        help="Mode name (sjn, qya, sindarin, quenya, beleriand)",
    )
    parser.add_argument(
        "text",
        nargs="+",
        help="Romanized text to transliterate",
    )
    parser.add_argument(
        "--literal",
        action="store_true",
        help="Emit literal PUA characters instead of \\uXXXX escapes. "
             "Default output is escaped (reviewable in any editor); "
             "use --literal only for piping into something that needs "
             "raw CSUR bytes (e.g. a font-aware preview).",
    )
    parser.add_argument(
        "--show-codepoints",
        action="store_true",
        help="Diagnostic format: print 'U+xxxx' for each codepoint, "
             "space-separated. Useful for inspecting output without a "
             "Tengwar font.",
    )
    args = parser.parse_args()

    try:
        mode = load_mode(args.mode)
    except FileNotFoundError:
        print(f"Unknown mode: {args.mode}", file=sys.stderr)
        sys.exit(2)

    text = " ".join(args.text)
    out = transliterate(text, mode)
    if args.show_codepoints:
        cps = []
        for c in out:
            o = ord(c)
            if o == 0x20:
                cps.append("SPACE")
            elif 0xE000 <= o <= 0xE0FF:
                cps.append(f"U+{o:04X}")
            else:
                cps.append(f"U+{o:04X}({c!r})")
        print(" ".join(cps))
    elif args.literal:
        print(out)
    else:
        print(escape_csur(out))


if __name__ == "__main__":
    main()
