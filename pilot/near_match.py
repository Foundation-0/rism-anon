#!/usr/bin/env python3
"""Count pitch-only matches and shuffled controls; never infer attribution."""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import random
import xml.etree.ElementTree as ET
from pae_frozen import pae_pitches

NS = '{http://www.loc.gov/MARC21/slim}'


def norm(pitches):
    return tuple(p-pitches[0] for p in pitches)


def removals(pitches):
    return [(i, norm(pitches[:i]+pitches[i+1:])) for i in range(len(pitches))]


def repeats(pitches):
    return [norm(pitches[:i]+pitches[i+1:]) for i in range(1,len(pitches)) if pitches[i] == pitches[i-1]]


class Index:
    def __init__(self, attributed):
        self.exact, self.transposed, self.changed = defaultdict(set), defaultdict(set), defaultdict(set)
        self.prefix, self.repeated = defaultdict(set), defaultdict(set)
        for record in attributed:
            for raw in record['pitches']:
                p = tuple(raw)
                self.exact[p].add(record['composer'])
                self.transposed[norm(p)].add(record['composer'])
                for key in removals(p): self.changed[key].add(record['composer'])
                self.prefix[norm(p[:11])].add(record['composer'])
                for key in repeats(p): self.repeated[key].add(record['composer'])

    def candidates(self, pitches):
        p = tuple(pitches)
        exact = self.exact.get(p, set())
        transposed = self.transposed.get(norm(p), set())
        near = set(transposed)
        for key in removals(p): near.update(self.changed.get(key, ()))
        # A repeated insertion shifts the 12-note cutoff. Only the shared 11 notes are compared.
        for key in repeats(p): near.update(self.prefix.get(key, ()))
        near.update(self.repeated.get(norm(p[:11]), ()))
        return exact, transposed, near


def read_export(path, max_records):
    rows = []
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rb') as stream:
        count = 0
        for _, el in ET.iterparse(stream, events=('end',)):
            if el.tag != NS+'record': continue
            count += 1
            if count > max_records: raise ValueError('record cap exceeded; no partial counts are reported')
            comp, genre, catref, pitches = None, None, False, []
            for field in el:
                if field.tag != NS+'datafield': continue
                values = {x.get('code'): x.text or '' for x in field}
                tag = field.get('tag')
                if tag == '100' and values.get('a'): comp = values['a']
                if tag == '650' and genre is None: genre = values.get('a')
                if tag in ('690','691'): catref = True
                if tag == '031' and values.get('p'):
                    ps = pae_pitches(values['p'], values.get('n'))
                    if len(ps)==12 and len(set(ps))>=5: pitches.append(ps)
            el.clear()
            if comp is None: continue
            anonymous = comp.strip().lower().startswith('anonym')
            if pitches and not (anonymous and catref):
                rows.append({'composer':comp,'anonymous':anonymous,'genre':genre or '(none)','pitches':pitches})
    return rows


def validate(rows):
    for r in rows:
        if not isinstance(r.get('anonymous'), bool) or not isinstance(r.get('composer'), str):
            raise ValueError('each record needs anonymous boolean and composer text')
        if not r.get('pitches'): raise ValueError('record needs pitches')
        for p in r['pitches']:
            if len(p)!=12 or any(type(x) is not int for x in p) or len(set(p))<5:
                raise ValueError('each incipit needs 12 integer pitches, at least 5 distinct')


def tally(index, anonymous):
    counts = {stage: Counter() for stage in ('exact','transposed_additional','near_additional')}
    for record in anonymous:
        hits = [False, False, False]
        for pitches in record['pitches']:
            for i, names in enumerate(index.candidates(pitches)):
                if len(names)==1: hits[i] = True
        # Per-record counts preserve the pilot's per-incipit composer-uniqueness convention.
        stage = next((i for i, hit in enumerate(hits) if hit), None)
        if stage is not None: counts[list(counts)[stage]][record.get('genre','(none)')] += 1
    return {stage:dict(sorted(values.items())) for stage,values in counts.items()}


def analyse(rows, seed=20261028, trials=20):
    validate(rows)
    if not 1 <= trials <= 1000: raise ValueError('trials must be 1..1000')
    index = Index([r for r in rows if not r['anonymous']])
    anonymous = [r for r in rows if r['anonymous']]
    rng = random.Random(seed)
    controls = []
    for _ in range(trials):
        shuffled = []
        for r in anonymous:
            seqs = [list(p) for p in r['pitches']]
            for p in seqs: rng.shuffle(p)
            shuffled.append(dict(r,pitches=seqs))
        controls.append(tally(index, shuffled))
    return {'status':'counts are candidates, never attributions', 'anonymous_records':len(anonymous),
            'counts_by_genre':tally(index,anonymous), 'shuffle_seed':seed,
            'shuffled_controls_by_genre':controls,
            'control_limit':'pitch-order shuffle preserves pitch multiset; not a calibrated false discovery rate'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--export', type=Path)
    group.add_argument('--fixture', type=Path)
    ap.add_argument('--max-records',type=int,default=25000)
    ap.add_argument('--expected-sha1', help='refuse input with a different SHA-1')
    ap.add_argument('--trials',type=int,default=20)
    ap.add_argument('--seed',type=int,default=20261028)
    a = ap.parse_args()
    try:
        source = a.export or a.fixture
        with source.open('rb') as stream: digest = hashlib.file_digest(stream,'sha1').hexdigest()
        if a.expected_sha1 and digest != a.expected_sha1:
            raise ValueError('input SHA-1 differs from the required export')
        rows = read_export(source,a.max_records) if a.export else json.loads(source.read_text())
        result = analyse(rows,a.seed,a.trials)
        result['input_sha1'] = digest
        result['input_kind'] = 'RISM export; full-pilot equality still requires comparison' if a.export else 'generated fixture'
        print(json.dumps(result,indent=2))
    except (ValueError,OSError) as exc: ap.error(str(exc))


if __name__ == '__main__': main()
