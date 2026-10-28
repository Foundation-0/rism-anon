import ast
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/'pilot'))
from near_match import Index, analyse
import pae_frozen

P=[60,62,64,65,67,69,71,72,74,76,77,79]

def row(p,anonymous=False,composer='Fixture composer'):
    return {'pitches':[p], 'anonymous':anonymous, 'composer':composer, 'genre':'Generated fixture'}


class MatchTests(unittest.TestCase):
    def test_stages_changed_first_note_and_transposition(self):
        index=Index([row(P)])
        self.assertEqual(index.candidates(P)[0], {'Fixture composer'})
        self.assertFalse(index.candidates([x+5 for x in P])[0])
        self.assertTrue(index.candidates([x+5 for x in P])[1])
        changed=[61]+P[1:]
        self.assertFalse(index.candidates(changed)[1])
        self.assertTrue(index.candidates(changed)[2])
        changed_twice=[61,63]+P[2:]
        self.assertFalse(index.candidates(changed_twice)[2])

    def test_repeated_note_and_ambiguity(self):
        repeated=P[:5]+[P[4]]+P[5:-1]
        self.assertTrue(Index([row(P)]).candidates(repeated)[2])
        result=analyse([row(P),row(P,composer='Other fixture'),row(P,True)],trials=1)
        self.assertEqual(sum(sum(x.values()) for x in result['counts_by_genre'].values()),0)

    def test_disjoint_counts_and_reproducible_controls(self):
        shifted=[x+4 for x in P]
        near=P[:];near[7]+=1
        rows=[row(P),row(P,True),row(shifted,True),row(near,True)]
        result=analyse(rows,trials=5)
        self.assertEqual([sum(x.values()) for x in result['counts_by_genre'].values()],[1,1,1])
        self.assertEqual(result,analyse(rows,trials=5))
        self.assertEqual(len(result['shuffled_controls_by_genre']),5)

    def test_parser_copy_ast_matches_original(self):
        def function(path):
            return ast.dump(next(x for x in ast.parse(path.read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='pae_pitches'),include_attributes=False)
        self.assertEqual(function(ROOT/'pilot/match_genre.py'),function(ROOT/'pilot/pae_frozen.py'))
        self.assertEqual(pae_frozen.pae_pitches("'4CDEFGAB''CDEFG",''), P[:8]+[74,76,77,79])
