import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"pilot"))
import review_sample as m

def record(rid, composer, genre="Masses", catref=False):
    return {"id":rid, "composer":composer, "catref":catref, "genres":[genre],
            "incipits":[{"p":"CDEFGABCDEFG", "n":""}]}

class SampleTests(unittest.TestCase):
    def test_both_ids_retained_and_unique_anonymous(self):
        pairs=m.candidates([record("101","Anonymous"),record("201","Fictional A"),record("202","Fictional A")])
        self.assertEqual(len(pairs),1)
        self.assertEqual(pairs[0]["anonymous"]["id"],"101")
        self.assertEqual(pairs[0]["attributed"]["id"],"201")
    def test_composer_conflict_catref_and_other_genre_excluded(self):
        attr=[record("201","Fictional A"),record("202","Fictional B")]
        self.assertEqual(m.candidates([record("101","Anonymous")]+attr),[])
        self.assertEqual(m.candidates([record("101","Anonymous",catref=True),attr[0]]),[])
        self.assertEqual(m.candidates([record("101","Anonymous","Chorales"),attr[0]]),[])
    def test_sample_reproducible_under_input_permutation(self):
        pairs=m.candidates([record(str(i),"Anonymous") for i in range(100,110)]+[record("201","Fictional A")])
        self.assertEqual(m.sample(pairs,5,7),m.sample(list(reversed(pairs)),5,7))
        with self.assertRaises(ValueError):m.sample(pairs,50,7)
    def test_private_write_never_overwrites_or_writes_inside_repo(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"sample.json";m.write_private(p,{"pairs":[]})
            self.assertEqual(p.stat().st_mode&0o777,0o600)
            with self.assertRaises(FileExistsError):m.write_private(p,{})
        with self.assertRaises(ValueError):m.write_private(Path(m.__file__).parent/"sample.json",{})

if __name__=="__main__":unittest.main()
