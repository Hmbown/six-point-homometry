"""Six-note-only inventory: exact families, inherited menus, and structural gaps.

Unit multiplication organizes orbits without merging distinct T/I classes.
The new structural pass excludes complement-of-direct-sum on dense complements;
the inherited menu remains separately labelled, never a completeness assertion.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import time
import sys

import p3_coverage as pc
from six_explore import bloom_edges, canon

ROOT = Path(__file__).resolve().parents[1]


def inherited_menu(n):
    path = ROOT / f"results/p3_menu/menu_n{n}.tsv"
    if not path.exists():
        return {}
    result = {}
    for line in path.read_text().splitlines():
        if line.startswith("#") or not line.startswith("6\t"):
            continue
        fields = line.split("\t")
        members = tuple(sorted(ast.literal_eval(s) for s in fields[4].split()))
        result[members] = dict(inherited_cZ=fields[2], inherited_cQ=fields[3],
                               integral_certificates=json.loads(fields[5]))
    return result


def components(members, edges):
    parent = {a:a for a in members}
    def find(a):
        while parent[a] != a:
            a = parent[a]
        return a
    for a,b in edges:
        parent[find(a)] = find(b)
    return len({find(a) for a in members})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nmin", type=int, default=12)
    parser.add_argument("--nmax", type=int, default=60)
    parser.add_argument("--out", type=Path, default=ROOT / "results/2026-09-30-six-inventory")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    for n in range(args.nmin,args.nmax+1):
        dest = args.out / f"n{n}.json"
        if args.resume and dest.exists():
            continue
        start=time.monotonic()
        families=json.loads((ROOT/f"results/2026-09-30-six-census/n{n}.json").read_text())["families"]
        menu=inherited_menu(n)
        bloom=bloom_edges(n)
        rows=[];counts=Counter()
        for family in families:
            members=tuple(sorted(tuple(a) for a in family["members"]))
            strict={}
            for a in members:
                hits=pc.strict_partners(a,n,flags=pc.ALLFLAGS & ~4)
                for b in members:
                    if b!=a and b in hits:
                        strict.setdefault(tuple(sorted((a,b))),set()).update(hits[b])
            bloom_inside={pair:cert for pair,cert in bloom.items() if pair[0] in members and pair[1] in members}
            nstrict=components(members,strict)
            ncombined=components(members,set(strict)|set(bloom_inside))
            counts["families"]+=1
            counts["strict_connected"]+=nstrict==1
            counts["strict_or_bloom_connected"]+=ncombined==1
            rows.append(dict(members=members,icv=family["icv"],
                             strict_edges=[dict(a=a,b=b,labels=sorted(labels)) for (a,b),labels in sorted(strict.items())],
                             bloom_edges=[dict(a=a,b=b,p=p,q=q) for (a,b),(p,q) in sorted(bloom_inside.items())],
                             strict_components=nstrict, combined_components=ncombined,
                             inherited=menu.get(members),
                             status="COMPUTED-UNVALIDATED coverage; exact census independently COMPUTED"))
        payload=dict(n=n,excluded=["dense-complement direct-sum", "cconj search", "unrestricted/rational spectral menus"],
                     summary=dict(counts),seconds=round(time.monotonic()-start,3),families=rows)
        tmp=dest.with_suffix(".tmp");tmp.write_text(json.dumps(payload,sort_keys=True)+"\n");tmp.replace(dest)
        print(n,dict(counts),payload["seconds"],flush=True)


if __name__=="__main__":
    main()
