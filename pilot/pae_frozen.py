# Exact parser copy from the original pilot; original scripts remain unchanged.
import re
STEP = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
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
