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

"""Lookup tool for the extracted Eldamo data.

Subcommands:
  lookup <lemma>           Exact lemma match across all language families.
  search <gloss-substring> Find words whose English gloss contains a string.
  check <form>             Verify a form's attestation status. Returns:
                           where it appears, in which language, and any
                           warnings (deprecated, wrong language, etc).
  cognates <lemma>         Show related forms across S / N / NS / Q / G.
  forms <pattern>          Search the attested surface forms (refs.tsv) for
                           inflected / compound forms matching pattern.

Default behavior limits to Sindarin family. Use --any-lang to search
Quenya and Gnomish too. Use --langs s,n,ns,q,etc to filter explicitly.
"""

import argparse
import csv
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")

FAMILY_LANGS = {
    "sjn": ["s", "n", "ns"],
    "qya": ["q", "nq", "mq", "eq"],
    "gno": ["g", "en"],
}
LANG_NAMES = {
    "s": "Sindarin", "n": "Noldorin", "ns": "Neo-Sindarin",
    "q": "Quenya", "nq": "Neo-Quenya", "mq": "Middle Quenya",
    "eq": "Early Quenya", "g": "Gnomish", "en": "Early Noldorin",
}


def load(family):
    """Load a TSV file as a list of dicts."""
    path = os.path.join(DATA_DIR, f"{family}.tsv")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def load_refs():
    path = os.path.join(DATA_DIR, "refs.tsv")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def select_langs(args):
    if args.langs:
        return set(args.langs.split(","))
    if args.any_lang:
        return set(sum(FAMILY_LANGS.values(), []))
    return set(FAMILY_LANGS["sjn"])


def all_records():
    """Iterate all word records across families."""
    for family in FAMILY_LANGS:
        for row in load(family):
            yield row


def format_row(row, indent=""):
    parts = [f"{indent}[{LANG_NAMES.get(row['lang'], row['lang'])}]",
             row["lemma"]]
    if row.get("speech"):
        parts.append(f"({row['speech']})")
    if row.get("gloss"):
        parts.append(f'"{row["gloss"]}"')
    line = " ".join(parts)
    flags = []
    if row.get("marker"):
        flags.append(f"mark={row['marker']}")
    if row.get("deprecated"):
        flags.append("DEPRECATED")
    if row.get("created_by"):
        flags.append(f"by {row['created_by']}")
    if row.get("source"):
        flags.append(row["source"])
    if flags:
        line += f"  [{', '.join(flags)}]"
    return line


def cmd_lookup(args):
    langs = select_langs(args)
    found = False
    for row in all_records():
        if row["lang"] in langs and row["lemma"] == args.term:
            print(format_row(row))
            found = True
    if not found:
        print(f"(no exact lemma match for '{args.term}' in {sorted(langs)})",
              file=sys.stderr)
        return 1
    return 0


def cmd_search(args):
    langs = select_langs(args)
    needle = args.term.lower()
    results = []
    for row in all_records():
        if row["lang"] not in langs:
            continue
        gloss = (row.get("gloss") or "").lower()
        if needle in gloss:
            results.append(row)
    if not results:
        print(f"(no gloss matches '{args.term}' in {sorted(langs)})",
              file=sys.stderr)
        return 1
    # Sort: exact word match in gloss first, then by language order.
    lang_order = {l: i for i, l in enumerate(["s", "n", "ns", "q", "nq",
                                              "mq", "eq", "g", "en"])}
    def sort_key(r):
        gloss_words = (r.get("gloss") or "").lower().split()
        exact = 0 if args.term.lower() in gloss_words else 1
        return (exact, lang_order.get(r["lang"], 99), r["lemma"])
    results.sort(key=sort_key)
    for r in results[:args.limit]:
        print(format_row(r))
    if len(results) > args.limit:
        print(f"... and {len(results) - args.limit} more (use --limit)",
              file=sys.stderr)
    return 0


def cmd_check(args):
    """Comprehensive attestation check for a form."""
    form = args.term
    print(f"Checking '{form}':\n")

    # 1. Direct lemma matches in any language.
    lemma_hits = [r for r in all_records() if r["lemma"] == form]
    if lemma_hits:
        print("  As a headword (lemma):")
        for r in lemma_hits:
            print("    " + format_row(r))
        print()
    else:
        print("  Not a headword in any included language.\n")

    # 2. Attested surface forms (inflected, compound).
    ref_hits = [r for r in load_refs() if r["form"] == form]
    if ref_hits:
        print("  As an attested surface form (in <ref> citations):")
        for r in ref_hits[:10]:
            parent = (f"of {LANG_NAMES.get(r['parent_lang'], r['parent_lang'])} "
                     f"{r['parent_lemma']}")
            extra = []
            if r.get("gloss"):
                extra.append(f'"{r["gloss"]}"')
            if r.get("source"):
                extra.append(r["source"])
            extras = f"  [{', '.join(extra)}]" if extra else ""
            print(f"    [{LANG_NAMES.get(r['lang'], r['lang'])}] {r['form']} "
                  f"{parent}{extras}")
        if len(ref_hits) > 10:
            print(f"    ... and {len(ref_hits) - 10} more")
        print()

    # 3. Warnings.
    warnings = []
    sjn_lemma = [r for r in lemma_hits if r["lang"] == "s"]
    qya_lemma = [r for r in lemma_hits if r["lang"] in ("q", "nq")]
    gno_lemma = [r for r in lemma_hits if r["lang"] == "g"]
    nol_lemma = [r for r in lemma_hits if r["lang"] == "n"]
    if not sjn_lemma and (qya_lemma or gno_lemma):
        if qya_lemma:
            warnings.append("This form is QUENYA, not Sindarin. Sindarin would "
                          "likely use a different cognate.")
        if gno_lemma:
            warnings.append("This form is GNOMISH (Tolkien's earliest stage of "
                          "the language that became Sindarin). Consider whether "
                          "a Sindarin form is available.")
    for r in lemma_hits:
        if r.get("deprecated"):
            warnings.append(f"The {LANG_NAMES.get(r['lang'], r['lang'])} "
                          f"entry for '{r['lemma']}' "
                          f'("{r.get("gloss", "")}") is DEPRECATED in Eldamo.')
        if r["lang"] == "ns" and r.get("marker") == "!":
            who = r.get("created_by", "unknown")
            warnings.append(f"The Neo-Sindarin '{r['lemma']}' is a neologism "
                          f"({who}). Document creator and rationale.")
    if not lemma_hits and not ref_hits:
        warnings.append("UNATTESTED in any included language. If used, mark as "
                      "coined.")

    if warnings:
        print("  Warnings:")
        for w in warnings:
            print(f"    - {w}")
    else:
        print("  No warnings.")

    return 0


def cmd_cognates(args):
    """Show all forms that share a lemma or look like cognates."""
    target = args.term
    print(f"Cognates / cross-language forms for '{target}':\n")
    # Direct lemma matches first.
    direct = [r for r in all_records() if r["lemma"] == target]
    if direct:
        print("  Direct lemma matches:")
        for r in direct:
            print("    " + format_row(r))
        print()
    # Loose match: lemma starts with the same first 3 chars, ignoring hyphens.
    key = target.lstrip("*†").rstrip("-").lower()[:3]
    if not key:
        return 0
    loose = []
    for r in all_records():
        lemma = r["lemma"].lstrip("*†").rstrip("-").lower()
        if lemma.startswith(key) and r["lemma"] != target:
            loose.append(r)
    if loose:
        print(f"  Similar-looking lemmas (starting with '{key}'):")
        for r in loose[:20]:
            print("    " + format_row(r))
        if len(loose) > 20:
            print(f"    ... and {len(loose) - 20} more")
    return 0


def cmd_forms(args):
    """Search attested surface forms (inflected, compound)."""
    needle = args.term.lower()
    langs = select_langs(args)
    refs = load_refs()
    hits = [r for r in refs if r["lang"] in langs and needle in r["form"].lower()]
    if not hits:
        print(f"(no surface-form match for '{args.term}')", file=sys.stderr)
        return 1
    for r in hits[:args.limit]:
        parent = (f"of {LANG_NAMES.get(r['parent_lang'], r['parent_lang'])} "
                 f"{r['parent_lemma']}")
        extra = []
        if r.get("gloss"):
            extra.append(f'"{r["gloss"]}"')
        if r.get("source"):
            extra.append(r["source"])
        extras = f"  [{', '.join(extra)}]" if extra else ""
        print(f"[{LANG_NAMES.get(r['lang'], r['lang'])}] {r['form']} "
              f"{parent}{extras}")
    if len(hits) > args.limit:
        print(f"... and {len(hits) - args.limit} more", file=sys.stderr)
    return 0


def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--any-lang", action="store_true",
                       help="Search all language families (default: Sindarin family only)")
    common.add_argument("--langs", metavar="LANGS",
                       help="Comma-separated language codes (s,n,ns,q,nq,mq,eq,g,en)")
    common.add_argument("--limit", type=int, default=30,
                       help="Max results for search commands (default: 30)")

    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common])
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name, helptext in [
        ("lookup", "Exact lemma match"),
        ("search", "Find by English gloss substring"),
        ("check", "Comprehensive attestation check"),
        ("cognates", "Show related cross-language forms"),
        ("forms", "Search attested surface forms (inflected, compound)"),
    ]:
        p = sub.add_parser(name, help=helptext, parents=[common])
        p.add_argument("term")
    args = parser.parse_args()

    handlers = {
        "lookup": cmd_lookup,
        "search": cmd_search,
        "check": cmd_check,
        "cognates": cmd_cognates,
        "forms": cmd_forms,
    }
    sys.exit(handlers[args.cmd](args))


if __name__ == "__main__":
    main()
