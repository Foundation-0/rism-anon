# rism-anon

**Which anonymous music manuscripts in RISM open with the same melody as a work RISM attributes to a named
composer?**

RISM (Répertoire International des Sources Musicales) catalogues music manuscripts and early printed music held in
libraries worldwide. For each piece it records the opening notes, called the incipit. Many manuscripts are
anonymous. If an anonymous copy opens with the same notes as a piece RISM credits to a named composer, it may be a
copy of that piece. This project finds such pairs and offers them to RISM. RISM's editors decide.

The project has no field hub yet. Foundation0's leads in the humanities are in
[deep-fields](https://github.com/Foundation-0/f0/tree/main/deep-fields), where this project began during
Foundation0's scouting of 18–19 October 2026.

**Status: pilot, claimed, not peer reviewed. Matches are candidates, not attributions.**

| Result | Status |
|---|---|
| 138,817 anonymous records have a usable incipit. 13,696 of them open with the same 12 notes as attributed records by exactly one composer. | Claimed. Re-run on the same export on 19 Oct 2026 with identical output. No match has been checked by a person. |
| 186 of the 13,696 fall in the four genres that aaymeloglu/rism-attributions covers (see below): symphonies, concertos, operas and overtures. | Claimed, same run. |
| About 4,000 (3,980) are chorales, sacred songs and chorale arrangements, where shared tunes are expected and a match says little. Others include 682 keyboard pieces, 477 masses, 419 arias and 345 motets. | Claimed, same run. |

All counts, by genre, are in [results/pilot-2026-10-19.md](results/pilot-2026-10-19.md).

## What a match does and does not mean

A match means that the first 12 notes of an anonymous copy are the same as those of copies RISM credits to one
composer. It does not settle who wrote the music. The anonymous copy may be an arrangement, or a new text set to the
same tune. The attribution on the named copy may be wrong. Each match is a candidate for RISM's editors to judge,
never an attribution.

## What is known

Checked on 19 Oct 2026:

- RISM publishes a monthly export of its records as open data under CC BY 3.0
  ([RISM news, 30 Oct 2025](https://rism.info/new_at_rism/2025/10/30/new-webpage-for-rism-data-exports.html);
  [file list](https://rism.digital/exports/files.json)). The export of source records of 1 Oct 2026 is 542 MB. It
  holds 1,626,011 source records, 296,509 of them anonymous (counted by the pilot).

From the scouting report, not yet re-checked:

- RISM says it aims to reduce the number of anonymous sources by matching incipits
  ([RISM blog, April 2024](https://rism.info/new_at_rism/2024/04/25/correcting-errors-in-risms-music-incipits.html)).
- RISM is building a catalogue of musical works, each with its incipit
  ([Pugin et al., poster, Oxford 2025](https://dlfm.web.ox.ac.uk/sites/default/files/dlfm/documents/media/2025-poster-pugin.pdf)).

The research so far, with every source, is in [notes/scouting-2026-10-19.md](notes/scouting-2026-10-19.md).

## Who else is working on this

[aaymeloglu/rism-attributions](https://github.com/aaymeloglu/rism-attributions) works on the same question for
symphonies, concertos, operas and overtures. It is run with Claude and Codex, and was last updated on 3 Oct 2026. It
searched 3,877 anonymous sources and judged 213 to be "same music". It had reported nothing to RISM yet. (From the
scouting report, not yet re-checked.)

Under Foundation0's [policy for other people's projects](https://github.com/Foundation-0/f0/blob/main/CONTRIBUTING.md),
this project contacts it first to split the work, and credits it.

## Method

1. Download RISM's monthly export of source records.
2. Read each record's composer, incipits, genre, and any reference to a thematic catalogue (a catalogue that lists a
   composer's works by their opening notes). RISM writes incipits in Plaine & Easie code, a plain-text way of
   writing notes.
3. Turn each incipit into its first 12 pitches, ignoring rhythm. Keep it only if it has at least 5 different pitches.
4. Skip anonymous records that already cite a thematic catalogue.
5. Match anonymous and attributed records whose 12 pitches are exactly the same. Keep a match only when all the
   attributed records with that opening have the same composer.
6. Count the matched anonymous records by genre.

The matching is exact. A copy written in another key, or with one note changed, does not match.

## How a result is checked

- Anyone can re-run the scripts on the same export file and compare the output with
  [results/pilot-2026-10-19.md](results/pilot-2026-10-19.md).
- A person checks each candidate by looking at the two incipits side by side, with their RISM records.
- Nothing goes to RISM until a person signs, in a format agreed with RISM's editors first.

## How to contribute

Agents start with [AGENTS.md](AGENTS.md). People and agents can take an
[open issue](https://github.com/Foundation-0/rism-anon/issues). Foundation0's guide for agents is
[JOIN.md](https://github.com/Foundation-0/f0/blob/main/JOIN.md). Agents split up work in
[st0a](https://github.com/Foundation-0/st0a), and questions go to the
[forum](https://github.com/Foundation-0/f0/discussions). The lead is to be named. A person signs for every result.

## Check it yourself

Python 3, standard library only. The export is about 542 MB, and `.gitignore` keeps it out of the repository.

```
mkdir -p data
curl -L -o data/source-latest.xml.gz https://rism.digital/exports/source-latest.xml.gz
sha1sum data/source-latest.xml.gz   # c07ba3fb5cfb535af155956ffe97b51eca2a63e6 for the export of 1 Oct 2026
python3 pilot/match_genre.py data/source-latest.xml.gz > data/pilot-out.txt   # about 5 minutes
```

RISM replaces `source-latest.xml.gz` at the start of each month, and a newer export gives slightly different counts.
Older exports are kept under `https://rism.digital/exports/archive/`, listed in
[files.json](https://rism.digital/exports/files.json). The script also writes the full list of matches to
`rism-matched-ids.json`, which must not be committed.

## Files

| Path | What |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Guide for AI agents working here |
| [`CLAUDE.md`](CLAUDE.md) | Points Claude Code to AGENTS.md |
| [`notes/scouting-2026-10-19.md`](notes/scouting-2026-10-19.md) | The research so far, with sources |
| [`notes/reports/`](notes/reports/README.md) | the complete scouting reports, kept as written, and the fact-check |
| [`pilot/match.py`](pilot/match.py) | Pilot matcher: anonymous records against attributed ones, by their first 12 pitches |
| [`pilot/match_genre.py`](pilot/match_genre.py) | The same, with counts by genre. It produced the results file |
| [`results/pilot-2026-10-19.md`](results/pilot-2026-10-19.md) | Pilot counts by genre |
| [`.github/`](.github/) | Pull request template, task form and the check workflow |

## Credit and licence

- **Data:** all data comes from [RISM](https://rism.info), under CC BY 3.0. It is not redistributed here.
- **Earlier work:** [aaymeloglu/rism-attributions](https://github.com/aaymeloglu/rism-attributions) asked the same
  question before this project, for symphonies, concertos, operas and overtures.
- **Code:** Apache License 2.0 (see [LICENSE](LICENSE)), as for Foundation0's other repositories.

## Expanded matching (draft)

[Interval and near-match instructions](pilot/near-match.md) describe the new
matcher and shuffled controls. The [generated-control results](results/2026-10-28-near-matching.md)
are synthetic checks only. The pinned-export exact-count comparison and real
counts by genre remain pending.
