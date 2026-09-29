---
name: add-fixture-sample
description: Bring a real instrument sample folder (e.g. 260918_E4 with four CSVs) into tests/fixtures/ as immutable reference input, and record what it reveals about the CSV format.
---
# Add a fixture sample

Fixtures are raw instrument exports and are **append-only** (invariant 1, hook-enforced).

1. **Locate** the folder the human provided (repo root, `data/`, or a path they gave you). Don't
   edit anything in it.
2. **Inspect before copying.** List the files. Show `head -5` and `tail -3` of each CSV, plus a
   byte-level check of the ending (`tail -c 64 file | od -c`) to catch trailing newlines, CRLF,
   BOM, `;` delimiters and decimal commas.
3. **Copy without overwriting:**
   `mkdir -p tests/fixtures/<sample> && cp -n <src>/* tests/fixtures/<sample>/`
   If the target folder already exists with different content, stop and ask. Never replace a fixture.
4. **Sanitize?** If the files contain anything that must not be committed (personal names, paths,
   proprietary headers), ask the human. Never alter fixture content yourself.
5. **Record the format** in `docs/domain/input-format.md`: tick the checklist, write down the exact
   variable names and units from the second-to-last line, and add a new
   "Observed in `<sample>`" section. Put anything surprising in MEMORY.md › Known pitfalls.
6. **Commit** the fixture on its own: `test(fixtures): add <sample> instrument export`.

**Done when:** the fixture is committed unmodified and input-format.md reflects it.
