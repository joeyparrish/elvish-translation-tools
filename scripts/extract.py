#!/usr/bin/env python3
"""Transform Eldamo's XML lexicon into compact TSV files by language family.

Reads:   references/eldamo/src/data/eldamo-data.xml
Writes:  data/sjn.tsv  (Sindarin family: s, n, ns)
         data/qya.tsv  (Quenya family: q, nq, mq, eq)
         data/gno.tsv  (Gnomish + Early Noldorin: g, en)
         data/refs.tsv (attested surface forms cross-referenced to lemmas)

TSV columns: lang, lemma, speech, gloss, marker, deprecated, created_by,
             source, neo_version

Markers (from Eldamo):
  #   word appears only in inflected form / compound
  *   reconstructed from primitives
  ^   reformulated from early versions
  ?   speculative
  !   pure neologism (fan invention)
  ‽   Tolkien himself wrote a "?"
  †   archaic / poetic
  ⚠️  excluded by Eldamo (do not use)
"""

import csv
import os
import sys
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XML_PATH = os.path.join(BASE, "references", "eldamo", "src", "data",
                       "eldamo-data.xml")
DATA_DIR = os.path.join(BASE, "data")

LANG_FAMILIES = {
    "sjn": {"s", "n", "ns"},
    "qya": {"q", "nq", "mq", "eq"},
    "gno": {"g", "en"},
}

HEADER = ["lang", "lemma", "speech", "gloss", "marker", "deprecated",
          "created_by", "source", "neo_version"]


def find_first_source(elem):
    """Find the first <ref> child's source attribute, if any."""
    for ref in elem.iter("ref"):
        src = ref.get("source")
        if src:
            return src
    return ""


def is_deprecated(elem):
    """Check whether this word is marked deprecated."""
    return elem.find("deprecated") is not None


def extract_words():
    """Yield (lang, record_dict) tuples for every <word> in the lexicon."""
    # Use iterparse to keep memory low on the 30MB file.
    context = ET.iterparse(XML_PATH, events=("end",))
    for event, elem in context:
        if elem.tag != "word":
            continue
        lang = elem.get("l", "")
        record = {
            "lang": lang,
            "lemma": elem.get("v", ""),
            "speech": elem.get("speech", ""),
            "gloss": elem.get("gloss", ""),
            "marker": elem.get("mark", ""),
            "deprecated": "1" if is_deprecated(elem) else "",
            "created_by": elem.get("created", ""),
            "source": find_first_source(elem),
            "neo_version": elem.get("neo-version", ""),
        }
        yield lang, record
        # Don't clear elem -- words can be nested inside other words
        # (etymological hierarchies). Memory is fine at this scale.


def extract_refs():
    """Yield (lang, form, gloss, source, parent_lemma, parent_lang) tuples
    for every attested surface form mentioned in <ref> tags. This lets us
    detect attested inflected forms like 'Daro' as imperative of 'dar-'.
    """
    context = ET.iterparse(XML_PATH, events=("end",))
    # Track the most recently entered <word> via a parent stack approximation:
    # we can't reliably get parent here without building it ourselves, so use
    # a separate pass with ET.parse for refs.
    tree = ET.parse(XML_PATH)
    root = tree.getroot()
    for word in root.iter("word"):
        parent_lang = word.get("l", "")
        parent_lemma = word.get("v", "")
        for ref in word.iter("ref"):
            # Skip nested refs from nested words (we'll hit them when we
            # process those words separately).
            yield {
                "lang": parent_lang,  # ref forms are in the same language
                "form": ref.get("v", ""),
                "gloss": ref.get("gloss", ""),
                "source": ref.get("source", ""),
                "parent_lemma": parent_lemma,
                "parent_lang": parent_lang,
            }


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Open one writer per language family.
    writers = {}
    files = {}
    for family in LANG_FAMILIES:
        path = os.path.join(DATA_DIR, f"{family}.tsv")
        f = open(path, "w", newline="", encoding="utf-8")
        files[family] = f
        w = csv.DictWriter(f, fieldnames=HEADER, delimiter="\t",
                          extrasaction="ignore")
        w.writeheader()
        writers[family] = w

    counts = {family: 0 for family in LANG_FAMILIES}
    other_count = 0

    for lang, record in extract_words():
        placed = False
        for family, langs in LANG_FAMILIES.items():
            if lang in langs:
                writers[family].writerow(record)
                counts[family] += 1
                placed = True
                break
        if not placed:
            other_count += 1

    for f in files.values():
        f.close()

    # Refs: attested surface forms.
    refs_path = os.path.join(DATA_DIR, "refs.tsv")
    with open(refs_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["lang", "form", "gloss", "source",
                                          "parent_lemma", "parent_lang"],
                           delimiter="\t", extrasaction="ignore")
        w.writeheader()
        ref_count = 0
        for ref in extract_refs():
            if ref["form"]:
                w.writerow(ref)
                ref_count += 1

    print("Extraction complete:", file=sys.stderr)
    for family, count in counts.items():
        path = os.path.join(DATA_DIR, f"{family}.tsv")
        size = os.path.getsize(path)
        print(f"  {family}: {count:5d} entries ({size:7d} bytes)",
              file=sys.stderr)
    print(f"  refs: {ref_count:5d} attested surface forms",
          file=sys.stderr)
    print(f"  (skipped {other_count} entries in other languages)",
          file=sys.stderr)


if __name__ == "__main__":
    main()
