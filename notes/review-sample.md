# A reproducible private sample for readers

Status: draft code tested with fictional records. The 50 real pairs have not been
sampled or read. Refs #1. RISM data are credited to RISM under CC BY 3.0; a match
does not establish authorship.

The pilot retained composer names but lost the attributed record IDs. The new
`pilot/review_sample.py` keeps both IDs, source links and MARC 031 fields. It uses
an unchanged copy of the pilot pitch parser and leaves the old scripts intact.
It keeps the same 12-pitch and five-distinct-pitch rules, excludes anonymous
records with catalogue references, and requires exactly one attributed composer.
Parser limitations remain; this is not independent validation of pitch parsing.

For this sample it then selects the `Masses` and `Arias` genre labels, one pair per
anonymous record. When several attributed copies qualify, it chooses one by a
stable lexical ordering before sampling. The seed is explicit and the input's
SHA-256 is stored. Reordering candidate input does not change the sample.

```sh
python3 -m unittest discover -s tests -v
python3 pilot/review_sample.py /private/tmp/source.xml.gz /private/tmp/rism-review.json --size 50 --seed 20261028
```

Python 3.11 or later is required. Use the pinned October export for comparison
with the existing pilot. The output must be outside the checkout and must not
already exist. It is created with owner-only permissions. Standard output has
counts and provenance only. Do not publish the private pair file or candidate
composer associations. The complete export run, memory use and original pilot
count comparison remain unchecked.

Give the two incipits and catalogue context to a reader. Record privately one of
`same piece`, `arrangement`, `shared opening`, or `unclear`, with reasons. Hide the
algorithm's composer suggestion during the initial comparison where practical.
Another reader checks the same 50 cases independently. Preserve disagreements
before discussion; publish only class counts and reader agreement. Do not infer
authorship from exact opening notes. RISM editors decide any attribution.

Before this issue closes, reproduce the pilot on its pinned export, generate the
sample, complete both readings, and have a person review the aggregate report.
