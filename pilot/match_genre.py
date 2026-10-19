# Pilot written on 19 Oct 2026 during Foundation0's scouting. The code below this header is unchanged.
#
# What it does: the same as match.py, then counts the matched anonymous records by genre (the first
# genre term in field 650 of each record). It ran on the export of 1 Oct 2026 and produced the counts
# in results/pilot-2026-10-19.md.
#
# Usage: python3 pilot/match_genre.py data/source-latest.xml.gz > pilot-out.txt
#   Counts go to standard output. The script also writes rism-matched-ids.json, the RISM ID of every
#   matched anonymous record, to the current directory. That is the full match list: it is
#   git-ignored and must not be committed.
#
# Pitches are absolute, so a copy written in another key does not match. Rhythm is ignored.
import gzip, sys, re, json
from collections import defaultdict, Counter
import xml.etree.ElementTree as ET
NS = '{http://www.loc.gov/MARC21/slim}'
STEP = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
L = 12
def pae_pitches(p, keysig):
    ks = {}
    if keysig:
        m = re.match(r'([xb])([A-G]+)', keysig)
        if m:
            for ch in m.group(2): ks[ch] = 1 if m.group(1)=='x' else -1
    octv = 4; acc = None; bar = {}; out = []
    i = 0; s = p
    while i < len(s):
        c = s[i]
        if c == "'":
            n = 0
            while i < len(s) and s[i] == "'": n += 1; i += 1
            octv = 3 + n; continue
        if c == ',':
            n = 0
            while i < len(s) and s[i] == ',': n += 1; i += 1
            octv = 4 - n; continue
        if c in 'xbn':
            if s[i:i+2] in ('xx','bb'): acc = 2 if c=='x' else -2; i += 2; continue
            acc = {'x':1,'b':-1,'n':0}[c]; i += 1; continue
        if c == '/': bar = {}; acc=None; i += 1; continue
        if c in '$%@': # key/clef/time change: skip token
            j = i+1
            while j < len(s) and s[j] not in "'/,ABCDEFG-0123456789=": j += 1
            if c == '$':
                m = re.match(r'([xb])([A-G]+)', s[i+1:j])
                ks = {}
                if m:
                    for ch in m.group(2): ks[ch] = 1 if m.group(1)=='x' else -1
            i = j; continue
        if c in STEP:
            if acc is not None: a = acc; bar[(c,octv)] = acc
            elif (c,octv) in bar: a = bar[(c,octv)]
            else: a = ks.get(c, 0)
            out.append(12*(octv+1) + STEP[c] + a)
            acc = None; i += 1
            if len(out) >= L: break
            continue
        i += 1
    return out
anon_fp = defaultdict(list); attr_fp = defaultdict(set); GEN = {}
n_rec = n_anon = n_anon_inc = 0; n_inc = 0
ctx = ET.iterparse(gzip.open(sys.argv[1]), events=('end',))
for ev, el in ctx:
    if el.tag != NS+'record': continue
    n_rec += 1
    rid = None; comp = None; catref = False; incs = []; genres = []
    for f in el:
        if f.tag == NS+'controlfield' and f.get('tag') == '001': rid = f.text
        elif f.tag == NS+'datafield':
            t = f.get('tag')
            if t == '100':
                for sf in f:
                    if sf.get('code') == 'a': comp = sf.text
            elif t in ('690','691'): catref = True
            elif t == '650':
                for sf in f:
                    if sf.get('code') == 'a': genres.append(sf.text)
            elif t == '031':
                d = {sf.get('code'): sf.text for sf in f}
                if d.get('p'): incs.append(d)
    el.clear()
    if comp is None: continue
    anon = comp.strip().lower().startswith('anonym')
    if anon: n_anon += 1; GEN[rid] = genres
    fps = []
    for d in incs:
        ps = pae_pitches(d['p'], d.get('n'))
        if len(ps) == L and len(set(ps)) >= 5:
            fps.append(tuple(ps))
    n_inc += len(fps)
    if anon:
        if fps and not catref: n_anon_inc += 1
        if not catref:
            for fp in fps: anon_fp[fp].append(rid)
    else:
        for fp in fps: attr_fp[fp].add(comp)
matches = {fp: (ids, attr_fp[fp]) for fp, ids in anon_fp.items() if fp in attr_fp}
single = {fp: v for fp, v in matches.items() if len(v[1]) == 1}
anon_recs_matched = set(r for fp,(ids,c) in single.items() for r in ids)
anon_recs_any = set(r for fp,(ids,c) in matches.items() for r in ids)
print(json.dumps({'records': n_rec, 'records_with_composer_field': None, 'anonymous_records': n_anon,
  'anonymous_with_usable_incipit_no_catref': n_anon_inc, 'usable_incipits_total': n_inc,
  'anon_fingerprints': len(anon_fp), 'fingerprints_matching_attributed': len(matches),
  'fingerprints_matching_one_composer': len(single), 'anon_records_matched_one_composer': len(anon_recs_matched),
  'anon_records_matched_any': len(anon_recs_any),
  'top_composers': Counter(next(iter(c)) for fp,(ids,c) in single.items()).most_common(15)}, indent=1))
ex = list(single.items())[:15]
for fp,(ids,c) in ex: print(ids[:3], list(c), fp)
gc = Counter()
for r in anon_recs_matched:
    g = GEN.get(r) or ['(none)']
    gc[g[0]] += 1
print('GENRES of anon records matched to one composer:')
for g, c in gc.most_common(30): print(c, g)
covered = {'Symphonies','Concertos','Operas','Overtures'}
print('in covered genres', sum(c for g,c in gc.items() if g in covered), 'of', sum(gc.values()))
json.dump(sorted(anon_recs_matched), open('rism-matched-ids.json','w'))
