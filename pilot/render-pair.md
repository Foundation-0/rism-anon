# Local incipit comparison

Status: implemented and checked on generated fixtures, awaiting independent
review. No RISM candidate or attribution is published by this tool.

Create an isolated environment and install the pinned renderer there:

```sh
python3 -m venv /tmp/rism-render-env
/tmp/rism-render-env/bin/pip install -r pilot/requirements-render.txt
/tmp/rism-render-env/bin/python pilot/render_pair.py \
  --fixtures examples/generated-pair.json --output /tmp/generated-pair.html
/tmp/rism-render-env/bin/python -m unittest discover -s tests -v
```

The committed `examples/generated-pair.html` contains real Verovio SVG output
for two invented scale fixtures. Their labels identify them as generated,
not RISM records or candidate matches. The page has no network dependencies.
It was visually inspected in Chromium, with both scores visible side by side.

To render two real records from a locally downloaded export:

```sh
/tmp/rism-render-env/bin/python pilot/render_pair.py \
  --export data/source-latest.xml.gz --ids RECORD_A RECORD_B \
  --output /tmp/pair.html
```

The script streams MARCXML and maps 031 g/n/o/p to clef/key signature/time
signature/notes. It renders the first incipit of each record, on every page
Verovio produces. Missing records or incipits fail instead of producing an
empty comparison. Labels and source text are HTML-escaped.

Verovio's [input-format documentation](https://book.verovio.org/toolkit-reference/input-formats.html)
defines the PAE JSON keys. Its [toolkit documentation](https://book.verovio.org/toolkit-reference/toolkit-methods.html)
defines `loadData`, `getPageCount` and `renderToSVG`. Version 6.3.0 was used.
The example demonstrates rendering, not full support for every RISM encoding.

## Acceptance still pending

Five pairs of actual named-composer records must be checked by a reviewer
against RISM Online. Record both IDs, export hash, incipit number, URL, date,
reviewer and discrepancies for each. None of those comparisons has been done.
Choose named-composer records for public examples. Keep anonymous candidate
pages local until the project has an appropriate review and publication path.
RISM data requires CC BY 3.0 attribution. Rendering agreement is not authorship.
