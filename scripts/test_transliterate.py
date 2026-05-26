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

"""Regression test for scripts/transliterate.py.

Fixtures live in data/modes/<mode>-tests.yaml as a list of {input, output}
pairs. Each `output` is the empirical Tecendil result for that input in
the given mode -- captured by pasting the input into the Tecendil web UI
and grabbing the output codepoints.

This script runs each input through our engine and compares against the
recorded output, with a normalization pass that strips U+2009 (THIN
SPACE) from the expected output: Tecendil emits that for display, but
our engine deliberately doesn't (the existing Shaka translations don't
contain it).

Usage:
    python3 scripts/test_transliterate.py

Exits non-zero if any case fails.
"""

import os
import subprocess
import sys

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE_PATH = os.path.join(BASE, "scripts", "transliterate.py")
MODES_DIR = os.path.join(BASE, "data", "modes")

# (mode-name-for-engine, fixture-file)
FIXTURES = [
    ("sjn", os.path.join(MODES_DIR, "sindarin-tests.yaml")),
    ("qya", os.path.join(MODES_DIR, "quenya-tests.yaml")),
]


def has_output(case):
    """A case is testable iff its output field is non-empty."""
    return bool(case.get("output"))


def fmt_codepoints(s):
    parts = []
    for c in s:
        o = ord(c)
        if o == 0x20:
            parts.append("SPACE")
        elif 0xE000 <= o <= 0xE07F:
            parts.append(f"U+{o:04X}")
        else:
            parts.append(f"U+{o:04X}({c!r})")
    return " ".join(parts)


def normalize(s):
    """Strip thin-space (U+2009); Tecendil emits it for display only."""
    return s.replace(" ", "")


def main():
    total = 0
    failures = 0
    for mode_name, fixture_path in FIXTURES:
        if not os.path.exists(fixture_path):
            print(f"[SKIP] {fixture_path} not found", file=sys.stderr)
            continue
        with open(fixture_path, encoding="utf-8") as f:
            cases = yaml.safe_load(f)
        if not cases:
            print(f"No test cases in {fixture_path}", file=sys.stderr)
            continue
        print(f"--- {os.path.basename(fixture_path)} (mode: {mode_name}) ---")
        skipped = 0
        for case in cases:
            if not has_output(case):
                skipped += 1
                continue
            inp = case["input"]
            expected = case["output"]
            total += 1
            result = subprocess.run(
                ["python3", ENGINE_PATH, mode_name, inp],
                capture_output=True,
                text=True,
            )
            got = result.stdout.rstrip("\n")
            expected_norm = normalize(expected)
            ok = got == expected_norm
            status = "PASS" if ok else "FAIL"
            print(f"  [{status}] input: {inp!r}")
            if not ok:
                print(f"           expected: {fmt_codepoints(expected_norm)}")
                print(f"           got:      {fmt_codepoints(got)}")
                failures += 1
            if result.stderr:
                print(f"           stderr: {result.stderr.strip()}")
        if skipped:
            print(f"  ({skipped} case(s) skipped: empty output -- awaiting Tecendil capture)")
        print()

    print(f"{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
