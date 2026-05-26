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

"""Render escape-encoded Tengwar strings as literal Unicode for display.

The translation source files (sjn-translations.yaml, sjn.json) store
Tengwar codepoints as \\uXXXX escapes so they're reviewable in any
editor. To actually SEE the Tengwar (in a terminal with the Tengwar
Telcontar font installed, or to copy into a font-aware editor), pipe
the escaped text through this tool.

Usage:
    # Inline string
    python3 scripts/preview.py '\\uE004\\uE020\\uE040'

    # From a file (Tengwar fields in a YAML get extracted and previewed)
    python3 scripts/preview.py --yaml path/to/sjn-translations.yaml

    # From stdin
    echo '\\uE004\\uE020' | python3 scripts/preview.py -

Output is raw Unicode -- the PUA characters render as boxes without a
CSUR-aware font. With Tengwar Telcontar (or another CSUR font) loaded
in your terminal, they render as Tengwar glyphs.
"""

import argparse
import codecs
import os
import sys


def unescape(s):
    """Decode \\uXXXX sequences (and the usual escapes) to literal chars."""
    return codecs.decode(s, "unicode_escape")


def preview_string(s):
    sys.stdout.write(unescape(s))
    sys.stdout.write("\n")


def preview_yaml(path):
    """Walk a translation YAML; print key + roman + literal Tengwar per entry."""
    import yaml

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    entries = data.get("translations", data) if isinstance(data, dict) else data
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        key = entry.get("key", "?")
        sjn = entry.get("sjn", {})
        roman = sjn.get("roman", "") if isinstance(sjn, dict) else ""
        tengwar = sjn.get("tengwar", "") if isinstance(sjn, dict) else ""
        # PyYAML already decoded escapes, so tengwar is literal PUA chars.
        print(f"{key:30}  {roman:30}  {tengwar}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("text", nargs="?",
                   help="Escape-encoded string to preview. Use '-' for stdin.")
    g.add_argument("--yaml", metavar="PATH",
                   help="Preview the Tengwar field of every entry in a "
                        "translation YAML file.")
    args = parser.parse_args()

    if args.yaml:
        preview_yaml(args.yaml)
        return 0

    if args.text == "-":
        text = sys.stdin.read()
    else:
        text = args.text
    preview_string(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
