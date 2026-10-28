import importlib.util
from pathlib import Path
import tempfile
import re
import unittest

spec = importlib.util.spec_from_file_location('render_pair', Path(__file__).parents[1]/'pilot/render_pair.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RecordTests(unittest.TestCase):
    def test_marc_fields_and_missing_record(self):
        text = '<collection xmlns="http://www.loc.gov/MARC21/slim"><record><controlfield tag="001">7</controlfield><datafield tag="100"><subfield code="a">Named fixture</subfield></datafield><datafield tag="031"><subfield code="g">G-2</subfield><subfield code="n">xF</subfield><subfield code="o">3/4</subfield><subfield code="p">4CDE</subfield></datafield></record></collection>'
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)/'records.xml'
            p.write_text(text)
            record = module.records(p, ['7'])[0]
            self.assertEqual(record['incipits'][0], {'clef':'G-2','keysig':'xF','timesig':'3/4','data':'4CDE'})
            with self.assertRaises(ValueError): module.records(p, ['8'])

    def test_empty_pair_fails(self):
        with self.assertRaises(ValueError): module.page([], lambda: None)

    def test_real_renderer_and_escaped_labels(self):
        import verovio
        record = {'id':'<script>bad</script>', 'composer':'A & B', 'incipits':[{'clef':'G-2','keysig':'','timesig':'4/4','data':"'4CDEF/"}]}
        result = module.page([record, record], verovio.toolkit)
        self.assertNotIn('<script>', result)
        self.assertIn('&lt;script&gt;', result)
        self.assertIn('A &amp; B', result)
        self.assertEqual(result.count('<section>'), 2)
        ids = re.findall(r' id="([^"]+)"', result)
        self.assertEqual(len(ids), len(set(ids)))
