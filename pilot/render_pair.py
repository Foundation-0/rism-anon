#!/usr/bin/env python3
"""Render two locally supplied RISM MARCXML records as a static HTML pair."""
import argparse
import gzip
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET

NS = '{http://www.loc.gov/MARC21/slim}'


def records(path, wanted):
    found = {}
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rb') as source:
        for _, element in ET.iterparse(source, events=('end',)):
            if element.tag != NS+'record':
                continue
            rid = next((x.text for x in element if x.tag == NS+'controlfield' and x.get('tag') == '001'), None)
            if rid in wanted:
                composer, incipits = None, []
                for field in element:
                    if field.tag != NS+'datafield':
                        continue
                    values = {x.get('code'): x.text or '' for x in field}
                    if field.get('tag') == '100':
                        composer = values.get('a')
                    if field.get('tag') == '031' and values.get('p'):
                        incipits.append({'clef': values.get('g', ''), 'keysig': values.get('n', ''),
                                         'timesig': values.get('o', ''), 'data': values['p']})
                found[rid] = {'id': rid, 'composer': composer, 'incipits': incipits}
            element.clear()
    missing = set(wanted) - found.keys()
    if missing:
        raise ValueError('records missing from input: '+', '.join(sorted(missing)))
    return [found[rid] for rid in wanted]


def page(pair, toolkit_factory):
    if len(pair) != 2:
        raise ValueError('exactly two records are required')
    panels = []
    for index, record in enumerate(pair):
        incipits = record.get('incipits') or []
        if not incipits:
            raise ValueError('record has no incipit')
        tk = toolkit_factory()
        # Separate toolkit instances prevent SVG identifiers colliding between panels.
        tk.resetXmlIdSeed(index+1)
        if not tk.setOptions({'inputFrom': 'pae', 'pageWidth': 1200, 'adjustPageHeight': True}):
            raise ValueError('renderer options rejected')
        if not tk.loadData(json.dumps(incipits[0])):
            raise ValueError('renderer rejected incipit')
        svgs = [tk.renderToSVG(n) for n in range(1, tk.getPageCount()+1)]
        if not svgs or any('<svg' not in svg for svg in svgs):
            raise ValueError('renderer produced no SVG')
        label = html.escape(str(record.get('id', 'unknown')))
        composer = html.escape(record.get('composer') or 'No composer field')
        panels.append(f'<section><h2>{label}</h2><p>{composer}</p>'+''.join(svgs)+
                      '<details><summary>Source incipit</summary><pre>'+html.escape(json.dumps(incipits[0], indent=2))+'</pre></details></section>')
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Incipit comparison</title><style>body{font:18px system-ui;margin:2rem}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem}svg{max-width:100%;height:auto}pre{white-space:pre-wrap}</style><h1>Incipit comparison</h1><p>Notation comparison only. A shared melody does not establish authorship. First incipit of each record; all rendered pages.</p><main>'+''.join(panels)+'</main><p>Local rendering with Verovio. For RISM exports: source RISM, CC BY 3.0. Generated fixtures are labelled separately.</p></html>'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--export', type=Path)
    source.add_argument('--fixtures', type=Path, help='JSON record pair, explicitly synthetic or locally extracted')
    parser.add_argument('--ids', nargs=2)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.export and not args.ids:
        parser.error('--export requires two --ids')
    import verovio
    try:
        pair = records(args.export, args.ids) if args.export else json.loads(args.fixtures.read_text())
        result = page(pair, verovio.toolkit)
        args.output.write_text(result)
        print(json.dumps({'output': str(args.output), 'renderer': verovio.toolkit().getVersion(), 'records': len(pair)}))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
