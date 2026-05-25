# Tengwar transliteration mode files

These JSONC files are vendored from
[arnog/tecendil-js](https://github.com/arnog/tecendil-js) (MIT
License, see `LICENSE.tecendil-js`). They describe the rules for
transliterating romanized Sindarin / Quenya / Beleriand into
symbolic Tengwar tokens (e.g. `{nuumen}`, `[acute]`).

The transliteration engine is in `scripts/transliterate.py`. It
reads these mode files, applies the rules per the conventions
documented in `references/tengwar-csur.md`, and emits CSUR Tengwar
codepoints.

To refresh from upstream:

```sh
for m in sindarin quenya beleriand; do
  curl -s "https://raw.githubusercontent.com/arnog/tecendil-js/refs/heads/master/modes/${m}.jsonc" \
    -o "data/modes/${m}.jsonc"
done
```
