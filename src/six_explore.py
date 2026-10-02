"""Exact exploratory six-note mechanisms; no novelty or completeness claims."""
from __future__ import annotations
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def canon(s, n):
    s = tuple(sorted(set(x % n for x in s)))
    return min(tuple(sorted((sign * (x - a)) % n for x in s))
               for a in s for sign in (1, -1))


def bloom(p, q, n):
    a = canon((0, p, q - 2*p, 2*q - 2*p, 2*q, 3*q - p), n)
    b = canon((0, p, q + 2*p, 2*q - p, 2*q + p, 3*q - p), n)
    return a, b


def icv(s, n):
    out = [0] * (n // 2)
    for a, b in combinations(s, 2):
        d = (b - a) % n
        out[min(d, n-d) - 1] += 1
    return tuple(out)


def bloom_edges(n):
    edges = {}
    for p in range(n):
        for q in range(n):
            a, b = bloom(p, q, n)
            if len(a) == len(b) == 6 and a != b:
                assert icv(a, n) == icv(b, n), (n, p, q)
                edges.setdefault(tuple(sorted((a, b))), (p, q))
    return edges


def main():
    rows = []
    gaps = []
    for n in range(12, 61):
        path = ROOT / f"results/2026-09-30-six-census/n{n}.json"
        if not path.exists():
            break
        d = json.loads(path.read_text())
        edges = bloom_edges(n)
        nf = len(d["families"])
        pairs = 0
        uncovered = []
        coll_free = 0
        coll_gaps = []
        for f in d["families"]:
            mem = [tuple(a) for a in f["members"]]
            for pair in combinations(mem, 2):
                pairs += 1
                covered = pair in edges
                collisionfree = max(f["icv"]) == 1
                coll_free += collisionfree
                if not covered:
                    uncovered.append(pair)
                    if collisionfree:
                        coll_gaps.append(pair)
        rows.append(dict(n=n, families=nf, pairs=pairs, bloom_pairs=len(edges),
                         collisionfree=coll_free, collisionfree_gaps=len(coll_gaps)))
        gaps.append(dict(n=n, pairs=[[list(a), list(b)] for a,b in uncovered]))
        print(rows[-1], flush=True)
    (ROOT / "results/2026-09-30-six-bloom.json").write_text(json.dumps({"summary":rows, "gaps":gaps},sort_keys=True)+"\n")


if __name__ == "__main__":
    main()
