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

"""Regenerate sjn.tengwar fields in a schema-following YAML file.

For each entry in `translations[]` whose `sjn.roman` is non-empty, runs the
romanized form through `scripts/transliterate.py` and replaces the
`sjn.tengwar` field with the escape-encoded (\\uXXXX) result.

Uses targeted text editing rather than YAML round-trip parsing, so comments,
whitespace, blank lines, indentation, and quote styles are preserved exactly.
Only the value inside `tengwar: "..."` is touched.

Usage:
    python3 scripts/regen_tengwar.py path/to/translations.yaml
    python3 scripts/regen_tengwar.py path/to/translations.yaml --mode qya
    python3 scripts/regen_tengwar.py path/to/translations.yaml --dry-run

Exits non-zero if any entry's romanized form fails to transliterate.
"""

import argparse
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSLITERATE = os.path.join(BASE, "scripts", "transliterate.py")

# Matches the line ' - key: KEYNAME' or ' - key: "KEYNAME"' at any
# indent depth (the schema uses 1-space indent for list-item dashes).
KEY_RE = re.compile(r'^\s*- key: "?([\w]+)"?\s*$')

# Matches a `roman: "VALUE"` line.
ROMAN_RE = re.compile(r'^\s+roman:\s*"([^"]*)"\s*$')

# Matches a `tengwar: "..."` line. Captures the prefix (indent + key)
# so we can preserve it exactly when rewriting.
TENGWAR_RE = re.compile(r'^(\s+tengwar:\s*)"[^"]*"\s*$')


def transliterate(roman, mode):
    """Invoke scripts/transliterate.py; return escape-encoded output."""
    result = subprocess.run(
        ["python3", TRANSLITERATE, mode, roman],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"transliterate.py failed for {roman!r}: "
            f"{result.stderr.strip()}"
        )
    return result.stdout.rstrip("\n")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("yaml_path", help="Path to the translation YAML.")
    parser.add_argument(
        "--mode",
        default="sjn",
        help="Transliteration mode for transliterate.py (default: sjn).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without modifying the file.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-entry output; only print summary.",
    )
    args = parser.parse_args()

    with open(args.yaml_path, encoding="utf-8") as f:
        lines = f.readlines()

    # Find every entry's starting line.
    entry_starts = [
        (m.group(1), i)
        for i, line in enumerate(lines)
        for m in [KEY_RE.match(line)]
        if m
    ]
    if not entry_starts:
        print(f"No entries found in {args.yaml_path}", file=sys.stderr)
        return 1

    updated = 0
    unchanged = 0
    skipped = 0
    failed = 0

    for j, (key, start) in enumerate(entry_starts):
        end = entry_starts[j + 1][1] if j + 1 < len(entry_starts) else len(lines)
        entry = lines[start:end]

        # Extract the roman form from this entry's lines.
        roman = None
        for line in entry:
            rm = ROMAN_RE.match(line)
            if rm:
                roman = rm.group(1)

        if not roman or not roman.strip():
            if not args.quiet:
                print(f"  [SKIP] {key}: empty romanized form")
            skipped += 1
            continue

        try:
            new_tengwar = transliterate(roman, args.mode)
        except RuntimeError as e:
            print(f"  [FAIL] {key}: {e}", file=sys.stderr)
            failed += 1
            continue

        # Find the tengwar line and update it in place.
        replaced = False
        for k, line in enumerate(entry):
            tm = TENGWAR_RE.match(line)
            if not tm:
                continue
            new_line = f'{tm.group(1)}"{new_tengwar}"\n'
            if new_line == line:
                unchanged += 1
            else:
                if not args.quiet:
                    print(f"  [UPDATE] {key}: {roman!r}")
                entry[k] = new_line
                updated += 1
            replaced = True
            break

        if not replaced:
            print(
                f"  [WARN] {key}: no `tengwar: \"...\"` line found in entry; "
                f"schema may be malformed",
                file=sys.stderr,
            )
            skipped += 1
            continue

        lines[start:end] = entry

    if not args.dry_run and updated > 0:
        with open(args.yaml_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    summary = (
        f"\n{updated} updated, {unchanged} already correct, "
        f"{skipped} skipped, {failed} failed"
    )
    if args.dry_run and updated > 0:
        summary += " (dry-run: no changes written)"
    print(summary)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
