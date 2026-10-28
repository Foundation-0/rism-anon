# Interval and near-match pilot

Status: implemented on generated controls, awaiting independent review.
The original `match.py` and `match_genre.py` remain unchanged.

```sh
python3 -m unittest discover -s tests -v
python3 pilot/near_match.py --fixture tests/generated-matching.json \
  --trials 20 > /tmp/generated-near-control.json
```

The output reports disjoint record counts by first genre: exact pitch matches,
additional transposed matches, then additional near matches. It also reports
each seeded pitch-order-shuffle control separately, using the same matching
steps. A control preserves each anonymous incipit's pitch multiset. It is not
a calibrated false-discovery rate, particularly for shared tunes and chorales.

Normalised pitches encode the same information as successive intervals.
Deleting the same position from both sequences indexes a possible one-note
change, including a change of the first note. One repeated-note insertion is
handled by removing an adjacent duplicate and comparing the remaining 11 notes
with the other incipit's prefix. The twelfth-note cutoff loses the final note
in that case, so these matches have weaker evidence than full 12-note matches.
Rhythm remains ignored. A candidate is never an attribution.

As in the original pilot, composer uniqueness is checked per fingerprint.
A record with multiple incipits can match different single-composer sets;
counts do not establish one composer for that whole record. Widening a match
can introduce multiple composers and make its uniqueness check fail.

## Full-export acceptance is pending

```sh
python3 pilot/near_match.py --export data/source-latest.xml.gz \
  --expected-sha1 c07ba3fb5cfb535af155956ffe97b51eca2a63e6 \
  --max-records 1700000 --trials 20 > /tmp/full-near-results.json
```

This command has not been run. Index construction stores multiple signatures
per attributed incipit and may require substantial memory. The default record
cap is 25,000 and refuses larger input without publishing partial counts.
Raising the cap is an explicit resource choice, not evidence the run will fit.

Before accepting full results, reproduce the old exact count of 13,696 and its
per-genre counts on the pinned export. Compare a sample of accepted and rejected
fingerprints with the original pilot. Review scale and resource use before
running shuffle replicates on the full export. Report controls by genre and
inspect real pairs before interpreting differences as useful discoveries.
RISM is the source of export data, under CC BY 3.0. No real candidate list is
included in this draft.
