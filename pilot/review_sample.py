"""Retain both sides of exact pilot matches in a private seeded review sample."""
import argparse
from collections import defaultdict
import gzip
import hashlib
import json
import os
from pathlib import Path
import random
import xml.etree.ElementTree as ET
from pilot_pitch_parser import pae_pitches, L

NS = "{http://www.loc.gov/MARC21/slim}"

def records(path):
    with gzip.open(path, "rb") as stream:
        context = ET.iterparse(stream, events=("start", "end"))
        _, root = next(context)
        for event, element in context:
            if event != "end" or element.tag != NS + "record":
                continue
            record = {"id": None, "composer": None, "catref": False, "genres": [], "incipits": []}
            for field in element:
                tag = field.get("tag")
                if field.tag == NS + "controlfield" and tag == "001":
                    record["id"] = field.text
                elif field.tag == NS + "datafield":
                    values = {node.get("code"): node.text for node in field}
                    if tag == "100": record["composer"] = values.get("a")
                    elif tag in ("690", "691"): record["catref"] = True
                    elif tag == "650" and values.get("a"): record["genres"].append(values["a"])
                    elif tag == "031" and values.get("p"): record["incipits"].append(values)
            element.clear()
            root.clear()
            yield record

def candidates(rows):
    anonymous, attributed = defaultdict(list), defaultdict(list)
    for record in rows:
        composer, rid = record["composer"], record["id"]
        if not composer or not rid or not rid.isdigit():
            continue
        anon = composer.strip().lower().startswith("anonym")
        if anon and record["catref"]:
            continue
        for incipit in record["incipits"]:
            pitches = pae_pitches(incipit["p"], incipit.get("n"))
            if len(pitches) != L or len(set(pitches)) < 5:
                continue
            item = {"id": rid, "composer": composer, "genres": record["genres"],
                    "incipit": incipit, "url": "https://rism.online/sources/" + rid}
            (anonymous if anon else attributed)[tuple(pitches)].append(item)
    # Choose one deterministic counterpart per anonymous record after preserving all
    # attributed record identities through the composer-uniqueness filter.
    pairs = defaultdict(list)
    for fingerprint in sorted(anonymous):
        matches = attributed.get(fingerprint, [])
        if len({item["composer"] for item in matches}) != 1:
            continue
        for anon in anonymous[fingerprint]:
            if not {g.casefold() for g in anon["genres"]} & {"masses", "arias"}:
                continue
            for attr in matches:
                pairs[anon["id"]].append({"anonymous": anon, "attributed": attr})
    return [min(pairs[rid], key=lambda pair: json.dumps(pair, sort_keys=True)) for rid in sorted(pairs)]

def sample(pairs, size, seed):
    if size < 1 or len(pairs) < size:
        raise ValueError("sample size must be positive and no larger than eligible candidates")
    ordered = sorted(pairs, key=lambda pair: json.dumps(pair, sort_keys=True))
    return random.Random(seed).sample(ordered, size)

def write_private(path, payload):
    path = Path(path).resolve()
    root = Path(__file__).resolve().parents[1]
    if path == root or root in path.parents:
        raise ValueError("sample must be outside the repository")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        json.dump(payload, stream, indent=2)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export"); parser.add_argument("output")
    parser.add_argument("--size", type=int, default=50)
    parser.add_argument("--seed", type=int, default=20261028)
    args = parser.parse_args()
    source = Path(args.export)
    with source.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    pairs = candidates(records(source))
    selection = sample(pairs, args.size, args.seed)
    write_private(args.output, {"source_sha256": digest, "seed": args.seed,
        "eligible_anonymous_records": len(pairs), "pairs": selection,
        "credit": "RISM open data, CC BY 3.0. Matches are candidates, not attributions."})
    print(json.dumps({"eligible_anonymous_records": len(pairs), "sample_size": len(selection),
                      "seed": args.seed, "source_sha256": digest}))

if __name__ == "__main__": main()
