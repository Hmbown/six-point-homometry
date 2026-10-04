"""Checks for the solver-free Iw enumerator (tools/iw_enumeration).

Fast (under a minute).  The full six-point run is the separate certificate
in tools/iw_enumeration/evidence/; this file checks the building blocks.
"""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import itertools
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("iw", HERE.parent / "iw_sorted_order_enumeration.py")
iw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(iw)


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def test_simplex():
    # max x + y s.t. x + y <= 1, x >= 0, y >= 0  ->  1
    st, v, _ = iw.simplex_max([[F(1), F(1)]], [F(1)], [F(1), F(1)])
    check((st, v) == ("optimal", 1), f"simplex basic: {st} {v}")
    # x >= 1/2, y >= 3/5, x + y <= 1 : infeasible   (rows as A x <= b)
    st, _, _ = iw.simplex_max([[F(-1), F(0)], [F(0), F(-1)], [F(1), F(1)]], [F(-1, 2), F(-3, 5), F(1)], [F(0), F(0)])
    check(st == "infeasible", f"simplex infeasible: {st}")
    # x >= 1/2, y >= 2/5, x + y <= 1 : feasible, max x = 3/5
    st, v, _ = iw.simplex_max([[F(-1), F(0)], [F(0), F(-1)], [F(1), F(1)]], [F(-1, 2), F(-2, 5), F(1)], [F(1), F(0)])
    check((st, v) == ("optimal", F(3, 5)), f"simplex tight: {st} {v}")
    # unbounded
    st, _, _ = iw.simplex_max([[F(-1)]], [F(0)], [F(1)])
    check(st == "unbounded", f"simplex unbounded: {st}")
    # random cross-check against vertex enumeration in 2 variables
    import random
    rnd = random.Random(7)
    for _ in range(60):
        A = [[F(rnd.randint(-3, 3)), F(rnd.randint(-3, 3))] for _ in range(4)] + [[F(1), F(0)], [F(0), F(1)]]
        b = [F(rnd.randint(-2, 5)) for _ in range(4)] + [F(5), F(5)]
        c = [F(rnd.randint(-3, 3)), F(rnd.randint(-3, 3))]
        st, v, _ = iw.simplex_max(A, b, c)
        # brute force: vertices of {Ax<=b, x>=0}
        rows = A + [[F(-1), F(0)], [F(0), F(-1)]]
        rhs = b + [F(0), F(0)]
        best = None
        for (i, j) in itertools.combinations(range(len(rows)), 2):
            det = rows[i][0] * rows[j][1] - rows[i][1] * rows[j][0]
            if det == 0:
                continue
            xx = (rhs[i] * rows[j][1] - rows[i][1] * rhs[j]) / det
            yy = (rows[i][0] * rhs[j] - rhs[i] * rows[j][0]) / det
            if all(r[0] * xx + r[1] * yy <= q for r, q in zip(rows, rhs)):
                val = c[0] * xx + c[1] * yy
                best = val if best is None else max(best, val)
        if best is None:
            check(st == "infeasible", f"random LP should be infeasible: {st}")
        else:
            check(st == "optimal" and v == best, f"random LP mismatch {st} {v} vs {best}")


def normalize_pair(A, B):
    """Sort, scale to diameter 1, apply the search's reflection/swap normalization,
    return gap coordinates."""
    A = sorted(A); B = sorted(B)
    def norm(S):
        lo, hi = S[0], S[-1]
        return [F(s - lo, hi - lo) for s in S]
    a, b = norm(A), norm(B)
    if a[1] + a[4] > 1:
        a = [1 - t for t in reversed(a)]
    if b[1] + b[4] > 1:
        b = [1 - t for t in reversed(b)]
    if a[1] > b[1]:
        a, b = b, a
    sp = iw.Space(6)
    return sp.from_points(tuple(a[1:5] + b[1:5]))


def lies_on(point, eqs):
    return all(sum(c * x for c, x in zip(e[:-1], point)) + e[-1] == 0 for e in eqs)


def test_targets():
    sp = iw.Space(6)
    lines = iw.bloom_lines(sp)
    check(len(lines) == 16, f"expected 16 Bloom lines, got {len(lines)}")
    X = lambda p, q: [0, p, q - 2 * p, 2 * q - 2 * p, 2 * q, 3 * q - p]
    Y = lambda p, q: [0, p, q + 2 * p, 2 * q - p, 2 * q + p, 3 * q - p]
    hits = 0
    for p, q in [(1, 4), (1, 5), (2, 7), (1, 6), (3, 10), (2, 5), (-1, 3), (1, -2)]:
        A, B = X(p, q), Y(p, q)
        if len(set(A)) < 6 or len(set(B)) < 6:
            continue
        pt = normalize_pair(A, B)
        check(any(lies_on(pt, eqs) for _, eqs in lines), f"Bloom pair ({p},{q}) not on any Bloom line")
        hits += 1
    check(hits >= 5, "too few Bloom pairs tested")
    # the repeated-atom weighted pair of Theorem Iw (slope q/p = 3)
    pt = normalize_pair([0, 1, 3, 3, 7, 8], [0, 2, 4, 7, 7, 8])
    check(any(lies_on(pt, eqs) for _, eqs in lines), "weighted Bloom pair not on a Bloom line")
    # a congruent pair is detected by the congruent targets, not the Bloom lines
    pt = normalize_pair([0, 1, 4, 9, 11, 13], [0, 1, 4, 9, 11, 13])
    cong = iw.congruent_targets(sp)
    check(any(lies_on(pt, eqs) for _, eqs in cong), "equal sets not detected as congruent")
    check(not any(lies_on(pt, eqs) for _, eqs in lines), "non-Bloom set lies on a Bloom line")


def test_four_points():
    s = iw.Search(4, lambda m: None)
    s.run()
    check(s.stats["nodes"] > 50, "four-point search too small")
    check(not s.stats["counterexamples"], "four-point search found a counterexample")
    check(s.stats["leaves"] == 0 and s.stats["good_prunes"] > 0, "four-point search should close every branch as congruent")


def test_hull():
    # polyhedron {x + y = 1, x >= 0, y >= 0, x <= 0} has affine hull {x=0, y=1}
    sp = iw.Space(4)  # V = 4 variables; use first two
    V = sp.V
    def form(c, const=0):
        v = [F(0)] * (V + 1)
        for k, val in c.items():
            v[k] = F(val)
        v[-1] = F(const)
        return tuple(v)
    eqs = [form({0: 1, 1: 1}, -1)]
    ineqs = [form({0: -1})]
    hull = iw.affine_hull(eqs, ineqs, V)
    check(iw.in_span(hull, form({0: 1})) and iw.in_span(hull, form({1: 1}, -1)), "implicit equality not detected")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("PASS", name)
