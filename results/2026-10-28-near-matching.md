# Generated-control results, 28 October 2026

Status: software checks on synthetic data, awaiting independent review.
These are not counts from RISM's export and contain no real candidate matches.

The committed `generated-near-control.json` comes from:

```sh
python3 pilot/near_match.py --fixture tests/generated-matching.json --trials 20
```

Five fictional records comprise one attributed reference, one exact copy,
one transposed copy, one changed-note copy and one repeated-note copy.
All use the genre label `Generated fixture`. The disjoint counts are 1 exact,
1 additional transposed and 2 additional near matches. Twenty seeded shuffled
controls produce zero matches in this tiny constructed example. That result
does not estimate the false-match rate in real musical data.

Four automated tests cover transposition, a changed first note, rejection of
two changed notes, repeated-note handling, composer ambiguity, disjoint counts,
reproducible shuffles and AST equality of the parser copy with the old pilot.
The full-export exact-count comparison and real-data genre/control counts
remain pending. No attribution or contact is authorised by these results.
