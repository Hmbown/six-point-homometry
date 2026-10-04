#!/usr/bin/env python3
"""Second, solver-free derivation of Theorem Iw (six-atom real multisets).

Theorem Iw (notes/2026-09-30-six-integer-theorem.md, Section 6) states: two
real multisets of total multiplicity six with equal autocorrelation, not
congruent by translation or reflection, are a Bloom pair, with repeated atoms
permitted.  The archived proof is an SMT unsatisfiability certificate.  This
program re-derives the statement with no SMT solver and no floating point.

Method
------
Normalize both configurations to 0 = a_0 <= a_1 <= ... <= a_5 = 1 and
0 = b_0 <= ... <= b_5 = 1 (weak order: coincident atoms allowed).  Equal
autocorrelation of two multisets of the same total mass is the same as equal
multisets of the fifteen interval lengths a_j - a_i, b_j - b_i (i<j), zeros
included.  Any pair with equal length multisets admits sortings of its two
edge lists that agree position by position; among tied lengths the sorting
can always be chosen to list a sub-interval before any interval containing
it.  The search therefore enumerates, position by position, the k-th smallest
A-interval and the k-th smallest B-interval, each drawn from the
inclusion-minimal unplaced intervals, with the equality and the sorted-order
inequalities added as exact linear constraints.  Infeasible branches are cut
with an exact rational simplex.  A branch whose explicit equalities already
force the configuration into a Bloom line or the congruent locus is closed
as good.  Every surviving leaf is a polyhedron; its affine hull (explicit
plus implicit equalities, found by exact LP) must lie in one Bloom line or
in the congruent locus.  A leaf failing that test would be a counterexample
and is printed.

Symmetry breaking (each a linear inequality, each justified by a symmetry
of the problem that preserves the others): reflect A so a_1 + a_4 <= 1;
reflect B so b_1 + b_4 <= 1; swap so a_1 <= b_1.

Soundness of the restriction to inclusion-minimal candidates: lengths are
monotone under interval inclusion, so a sorting respecting inclusion among
ties exists, and every pair is covered by some branch.  Soundness of the
"provably equal" pruning: if two minimal candidates are already equal under
the explicit equalities, the two branches produce identical leaf systems.

Standard library only.  Usage: python tools/iw_enumeration/iw_sorted_order_enumeration.py
[--points 6] [--out DIR].
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent

# --------------------------------------------------------------------------
# Linear forms: tuple of V coefficients followed by a constant term.


class Space:
    def __init__(self, n_points: int):
        self.N = n_points
        self.V = 2 * (n_points - 2)

    def point(self, side: int, i: int):
        """Coordinate of point i as a linear form in the gap variables
        g_1..g_{N-2} of each side (g_{N-1} = 1 - sum of the others)."""
        v = [F(0)] * (self.V + 1)
        if i == 0:
            return tuple(v)
        if i == self.N - 1:
            v[-1] = F(1)
            return tuple(v)
        base = side * (self.N - 2)
        for k in range(1, i + 1):
            v[base + k - 1] = F(1)
        return tuple(v)

    def gap(self, side: int, k: int):
        """Gap g_k = x_k - x_{k-1}, k = 1..N-1."""
        return sub(self.point(side, k), self.point(side, k - 1))

    def from_points(self, coords):
        """Convert (a_1..a_{N-2}, b_1..b_{N-2}) point coordinates to gap coordinates."""
        n = self.N - 2
        out = []
        for side in (0, 1):
            pts = [F(0)] + list(coords[side * n:(side + 1) * n])
            out.extend(pts[k] - pts[k - 1] for k in range(1, n + 1))
        return tuple(out)

    def edge(self, side: int, i: int, j: int):
        return sub(self.point(side, j), self.point(side, i))


def sub(u, v):
    return tuple(x - y for x, y in zip(u, v))


def add(u, v):
    return tuple(x + y for x, y in zip(u, v))


def neg(u):
    return tuple(-x for x in u)


def is_zero(u):
    return all(x == 0 for x in u)


# --------------------------------------------------------------------------
# Exact linear algebra.


def rref(rows):
    """Reduced row echelon form of a list of Fraction rows. Returns (rows, pivots)."""
    m = [list(r) for r in rows]
    pivots = []
    r = 0
    ncols = len(m[0]) if m else 0
    for c in range(ncols):
        if r >= len(m):
            break
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
    return m[:r], pivots


def rank(rows):
    if not rows:
        return 0
    return len(rref(rows)[0])


def in_span(rows, vec):
    """Is vec (an affine form) in the Q-span of rows?"""
    if is_zero(vec):
        return True
    return rank(rows) == rank(list(rows) + [vec])


# --------------------------------------------------------------------------
# Exact two-phase simplex: maximize c.x subject to A x <= b, x >= 0.


def simplex_max(A, b, c):
    m = len(A)
    n = len(c)
    rows = []
    kinds = []
    for i in range(m):
        row = list(A[i])
        rhs = b[i]
        if rhs < 0:
            row = [-x for x in row]
            rhs = -rhs
            kinds.append("ge")
        else:
            kinds.append("le")
        rows.append((row, rhs))
    n_art = sum(1 for k in kinds if k == "ge")
    T = n + m + n_art  # columns excluding rhs
    tab = []
    basis = []
    art_cols = []
    art_index = 0
    for i, (row, rhs) in enumerate(rows):
        full = [F(0)] * (T + 1)
        for j in range(n):
            full[j] = row[j]
        if kinds[i] == "le":
            full[n + i] = F(1)
            basis.append(n + i)
        else:
            full[n + i] = F(-1)
            col = n + m + art_index
            full[col] = F(1)
            art_cols.append(col)
            basis.append(col)
            art_index += 1
        full[T] = rhs
        tab.append(full)

    def pivot(r, col):
        pv = tab[r][col]
        tab[r] = [x / pv for x in tab[r]]
        for i in range(len(tab)):
            if i != r and tab[i][col] != 0:
                f = tab[i][col]
                tab[i] = [x - f * y for x, y in zip(tab[i], tab[r])]
        basis[r] = col

    def run(cost, allowed_cols):
        # cost: list length T (coefficients on columns); maximize.
        while True:
            # reduced costs
            red = list(cost)
            for r, bcol in enumerate(basis):
                cb = cost[bcol]
                if cb != 0:
                    red = [x - cb * y for x, y in zip(red, tab[r][:T])]
            enter = next((j for j in allowed_cols if red[j] > 0), None)
            if enter is None:
                value = sum(cost[bcol] * tab[r][T] for r, bcol in enumerate(basis))
                return "optimal", value
            best = None
            for r in range(len(tab)):
                a = tab[r][enter]
                if a > 0:
                    ratio = tab[r][T] / a
                    key = (ratio, basis[r])
                    if best is None or key < best[0]:
                        best = (key, r)
            if best is None:
                return "unbounded", None
            pivot(best[1], enter)

    allowed = list(range(T))
    if n_art:
        cost1 = [F(0)] * T
        for col in art_cols:
            cost1[col] = F(-1)
        status, value = run(cost1, allowed)
        assert status == "optimal"
        if value < 0:
            return "infeasible", None, None
        # drive artificials out
        for r in range(len(tab)):
            if basis[r] in art_cols:
                col = next((j for j in range(n + m) if tab[r][j] != 0), None)
                if col is not None:
                    pivot(r, col)
        keep = [r for r in range(len(tab)) if basis[r] not in art_cols]
        tab = [tab[r] for r in keep]
        basis = [basis[r] for r in keep]
        allowed = list(range(n + m))
    cost2 = [F(0)] * T
    for j in range(n):
        cost2[j] = c[j]
    status, value = run(cost2, allowed)
    if status != "optimal":
        return status, None, None
    x = [F(0)] * n
    for r, bcol in enumerate(basis):
        if bcol < n:
            x[bcol] = tab[r][T]
    return "optimal", value, x


# --------------------------------------------------------------------------
# Polyhedron {eqs = 0, ineqs >= 0, 0 <= x} handling.


class Infeasible(Exception):
    pass


def eliminate(eqs, V):
    """Return (free_vars, subst) where subst maps each variable index to an
    affine form over the free variables (length len(free)+1)."""
    if not eqs:
        free = list(range(V))
        subst = {}
        for v in range(V):
            f = [F(0)] * (V + 1)
            f[v] = F(1)
            subst[v] = tuple(f)
        return free, subst, list(range(V))
    red, pivots = rref(eqs)
    for row in red:
        if all(x == 0 for x in row[:-1]) and row[-1] != 0:
            raise Infeasible
    red = [row for row in red if not all(x == 0 for x in row[:-1])]
    pivots = pivots[: len(red)]
    pivset = set(pivots)
    free = [v for v in range(V) if v not in pivset]
    pos = {v: k for k, v in enumerate(free)}
    nf = len(free)
    subst = {}
    for v in free:
        f = [F(0)] * (nf + 1)
        f[pos[v]] = F(1)
        subst[v] = tuple(f)
    for row, p in zip(red, pivots):
        # x_p + sum_{f} row[f] x_f + row[-1] = 0
        f = [F(0)] * (nf + 1)
        for v in free:
            f[pos[v]] = -row[v]
        f[-1] = -row[-1]
        subst[p] = tuple(f)
    return free, subst, pivots


def substitute(form, subst, free, V):
    nf = len(free)
    out = [F(0)] * (nf + 1)
    out[-1] = form[-1]
    for v in range(V):
        cv = form[v]
        if cv != 0:
            s = subst[v]
            for k in range(nf + 1):
                out[k] += cv * s[k]
    return out


def lp_max(obj, eqs, ineqs, V):
    """Maximize obj over {eqs=0, ineqs>=0, x>=0}. Returns value or raises Infeasible.
    All variables are gaps, hence nonnegative; the simplex supplies x>=0 for the
    free variables and explicit rows supply it for eliminated ones."""
    free, subst, pivots = eliminate(eqs, V)
    nf = len(free)
    A = []
    b = []
    extra = []
    for v in pivots:
        f = [F(0)] * (V + 1)
        f[v] = F(1)
        extra.append(tuple(f))
    for form in list(ineqs) + extra:
        s = substitute(form, subst, free, V)
        coef = s[:nf]
        const = s[nf]
        if all(x == 0 for x in coef):
            if const < 0:
                raise Infeasible
            continue
        A.append([-x for x in coef])
        b.append(const)
    so = substitute(obj, subst, free, V)
    c = so[:nf]
    const = so[nf]
    if nf == 0:
        return const
    status, value, _ = simplex_max(A, b, c)
    if status == "infeasible":
        raise Infeasible
    assert status == "optimal", status
    return value + const


def feasible(eqs, ineqs, V):
    try:
        lp_max(tuple([F(0)] * (V + 1)), eqs, ineqs, V)
        return True
    except Infeasible:
        return False


def affine_hull(eqs, ineqs, V):
    """Explicit plus implicit equalities of the feasible polyhedron."""
    hull = list(eqs)
    for form in ineqs:
        if in_span(hull, form):
            continue
        top = lp_max(form, hull, ineqs, V)
        if top == 0:
            hull.append(form)
    return hull


# --------------------------------------------------------------------------
# Targets: congruent locus and Bloom lines.


def congruent_targets(sp: Space):
    N = sp.N
    same = [sub(sp.point(1, i), sp.point(0, i)) for i in range(1, N - 1)]
    refl = [sub(add(sp.point(1, i), sp.point(0, N - 1 - i)), sp.point(0, N - 1)) for i in range(1, N - 1)]
    return [("congruent:B=A", same), ("congruent:B=1-rev(A)", refl)]


BLOOM_X = ((0, 0), (1, 0), (-2, 1), (-2, 2), (0, 2), (-1, 3))
BLOOM_Y = ((0, 0), (1, 0), (2, 1), (-1, 2), (1, 2), (-1, 3))


def bloom_lines(sp: Space):
    """All affine lines in R^8 traced by normalized sorted Bloom pairs, under
    reflection of either set and interchange.  Returns list of (name, eqs)."""
    assert sp.N == 6
    # collision slopes q/p where two coordinates of X or of Y coincide
    slopes = set()
    for coords in (BLOOM_X, BLOOM_Y):
        for (a1, b1), (a2, b2) in itertools.combinations(coords, 2):
            da, db = a1 - a2, b1 - b2
            if db != 0:
                slopes.add(F(-da, db))
    slopes = sorted(slopes)
    samples = [slopes[0] - 1] + [(s + t) / 2 for s, t in zip(slopes, slopes[1:])] + [slopes[-1] + 1]
    lines = {}
    for p_sign in (1, -1):
        for s in samples:
            p = F(p_sign)
            q = s * p
            def sorted_forms(coords):
                vals = [(F(a) * p + F(b) * q, a, b) for a, b in coords]
                vals.sort()
                base_a, base_b = vals[0][1], vals[0][2]
                # coefficient vectors (on p, on q) of sorted coordinates minus min
                return [(F(a - base_a), F(b - base_b)) for _, a, b in vals]
            SX = sorted_forms(BLOOM_X)
            SY = sorted_forms(BLOOM_Y)
            assert SX[5] == SY[5], (SX, SY)
            dp, dq = SX[5]
            # two parameter points with diameter 1
            if dq != 0:
                params = [(F(0), 1 / dq), (F(1), (1 - dp) / dq)]
            else:
                params = [(1 / dp, F(0)), (1 / dp, F(1))]
            pts = []
            for pp, qq in params:
                assert dp * pp + dq * qq == 1
                a = [ca * pp + cb * qq for ca, cb in SX]
                b = [ca * pp + cb * qq for ca, cb in SY]
                pts.append((a, b))
            for ra, rb, sw in itertools.product((0, 1), (0, 1), (0, 1)):
                P = []
                for a, b in pts:
                    aa = [1 - x for x in reversed(a)] if ra else list(a)
                    bb = [1 - x for x in reversed(b)] if rb else list(b)
                    if sw:
                        aa, bb = bb, aa
                    P.append(sp.from_points(tuple(aa[1:5] + bb[1:5])))
                eqs = line_equations(P[0], P[1], sp.V)
                key = tuple(tuple(r) for r in rref(eqs)[0])
                if key not in lines:
                    lines[key] = (f"bloom:p={p_sign},slope={s},rA={ra},rB={rb},swap={sw}", eqs)
    return list(lines.values())


def line_equations(P0, P1, V):
    u = [x - y for x, y in zip(P1, P0)]
    assert any(x != 0 for x in u)
    j = next(i for i in range(V) if u[i] != 0)
    eqs = []
    for i in range(V):
        if i == j:
            continue
        w = [F(0)] * (V + 1)
        w[i] = F(1)
        w[j] = -u[i] / u[j]
        w[-1] = -(w[i] * P0[i] + w[j] * P0[j])
        eqs.append(tuple(w))
    return eqs


def contained_in(hull_eqs, target_eqs):
    return all(in_span(hull_eqs, t) for t in target_eqs)


# --------------------------------------------------------------------------
# The search.


class Search:
    def __init__(self, n_points: int, log, largest_first: bool = True):
        self.largest_first = largest_first
        self.sp = Space(n_points)
        self.N = n_points
        self.V = self.sp.V
        self.log = log
        self.edges = list(itertools.combinations(range(n_points), 2))
        self.dA = {e: self.sp.edge(0, *e) for e in self.edges}
        self.dB = {e: self.sp.edge(1, *e) for e in self.edges}
        self.targets = congruent_targets(self.sp)
        if n_points == 6:
            self.targets += bloom_lines(self.sp)
        self.stats = {
            "nodes": 0, "infeasible": 0, "good_prunes": 0, "leaves": 0,
            "leaf_hull_dims": {}, "target_hits": {}, "counterexamples": [],
            "dedupe_skips": 0,
        }
        self.leaf_lines = {}
        self.t0 = time.monotonic()

    def domain(self):
        sp = self.sp
        N = self.N
        ineqs = []
        for side in (0, 1):
            ineqs.append(sp.gap(side, N - 1))  # last gap >= 0; the others are simplex variables
            # reflection normalization: x_1 + x_{N-2} <= 1
            ineqs.append(sub(sp.point(side, N - 1), add(sp.point(side, 1), sp.point(side, N - 2))))
        # swap normalization: a_1 <= b_1
        ineqs.append(sub(sp.point(1, 1), sp.point(0, 1)))
        return ineqs

    def minimal_unplaced(self, placed):
        """Unplaced intervals all of whose proper sub-intervals are placed."""
        out = []
        for (i, j) in self.edges:
            if (i, j) in placed:
                continue
            if j - i == 1 or ((i, j - 1) in placed and (i + 1, j) in placed):
                out.append((i, j))
        return out

    def maximal_unplaced(self, placed):
        """Unplaced intervals all of whose proper super-intervals are placed."""
        N = self.N
        out = []
        for (i, j) in self.edges:
            if (i, j) in placed:
                continue
            if (i == 0 or (i - 1, j) in placed) and (j == N - 1 or (i, j + 1) in placed):
                out.append((i, j))
        return out

    def frontier(self, placed):
        return self.maximal_unplaced(placed) if self.largest_first else self.minimal_unplaced(placed)

    def order_ineqs(self, e, lastA, minA, minB):
        """Sorted-order constraints for placing A-edge e as the next length."""
        out = []
        if self.largest_first:
            if lastA is not None:
                out.append(sub(self.dA[lastA], self.dA[e]))
            for m in minA:
                out.append(sub(self.dA[e], self.dA[m]))
            for m in minB:
                out.append(sub(self.dA[e], self.dB[m]))
        else:
            if lastA is not None:
                out.append(sub(self.dA[e], self.dA[lastA]))
            for m in minA:
                out.append(sub(self.dA[m], self.dA[e]))
            for m in minB:
                out.append(sub(self.dB[m], self.dA[e]))
        return out

    def dedupe(self, cands, d, eqs):
        kept = []
        for e in cands:
            if any(in_span(eqs, sub(d[e], d[k])) for k in kept):
                self.stats["dedupe_skips"] += 1
                continue
            kept.append(e)
        return kept

    def good(self, eqs):
        for name, teqs in self.targets:
            if contained_in(eqs, teqs):
                return name
        return None

    def run(self):
        self.recurse(frozenset(), frozenset(), [], self.domain(), None, 0)
        return self.stats

    def first_level(self, split_depth=3):
        """Feasible, not-yet-closed states at `split_depth`, each a task for one
        process.  Branches closed (infeasible or good) above the split depth are
        counted in the driver's own stats."""
        tasks = []
        self.split_depth = split_depth
        self._tasks = tasks
        self.recurse(frozenset(), frozenset(), [], self.domain(), None, 0)
        del self.split_depth
        return tasks

    def recurse(self, placedA, placedB, eqs, ineqs, lastA, depth):
        self.stats["nodes"] += 1
        if self.stats["nodes"] % 2000 == 0:
            self.log(f"nodes={self.stats['nodes']} leaves={self.stats['leaves']} good={self.stats['good_prunes']} infeasible={self.stats['infeasible']} depth={depth} t={time.monotonic()-self.t0:.1f}s")
        if depth == len(self.edges):
            self.leaf(eqs, ineqs)
            return
        if getattr(self, "split_depth", None) == depth and depth > 0:
            self._tasks.append((placedA, placedB, eqs, ineqs, lastA, depth))
            return
        candA = self.dedupe(self.frontier(placedA), self.dA, eqs)
        candB = self.dedupe(self.frontier(placedB), self.dB, eqs)
        for e in candA:
            newA = placedA | {e}
            minA = self.frontier(newA)
            for f in candB:
                newB = placedB | {f}
                minB = self.frontier(newB)
                new_eqs = eqs + [sub(self.dA[e], self.dB[f])]
                new_ineqs = ineqs + self.order_ineqs(e, lastA, minA, minB)
                if not feasible(new_eqs, new_ineqs, self.V):
                    self.stats["infeasible"] += 1
                    continue
                name = self.good(new_eqs)
                if name is not None:
                    self.stats["good_prunes"] += 1
                    self.stats["target_hits"][name] = self.stats["target_hits"].get(name, 0) + 1
                    continue
                self.recurse(newA, newB, new_eqs, new_ineqs, e, depth + 1)

    def leaf(self, eqs, ineqs):
        self.stats["leaves"] += 1
        hull = affine_hull(eqs, ineqs, self.V)
        dim = self.V - rank(hull)
        self.stats["leaf_hull_dims"][str(dim)] = self.stats["leaf_hull_dims"].get(str(dim), 0) + 1
        name = self.good(hull)
        if name is None:
            # genuine counterexample candidate: describe it
            red, _ = rref(hull)
            self.stats["counterexamples"].append({
                "hull_dim": dim,
                "hull_rref": [[str(x) for x in row] for row in red],
            })
            self.log(f"COUNTEREXAMPLE CANDIDATE dim={dim}: {red}")
        else:
            self.stats["target_hits"][name] = self.stats["target_hits"].get(name, 0) + 1
            key = tuple(tuple(r) for r in rref(hull)[0])
            self.leaf_lines[key] = name


def _worker(args):
    n_points, largest_first, state = args
    placedA, placedB, eqs, ineqs, lastA, depth = state
    s = Search(n_points, lambda m: None, largest_first)
    s.recurse(placedA, placedB, eqs, ineqs, lastA, depth)
    return (sorted(placedA), sorted(placedB), s.stats, {str(k): v for k, v in s.leaf_lines.items()})


def merge(stats_list):
    total = {"nodes": 0, "infeasible": 0, "good_prunes": 0, "leaves": 0, "dedupe_skips": 0,
             "leaf_hull_dims": {}, "target_hits": {}, "counterexamples": [], "branches": []}
    lines = {}
    for e, f, st, ll in stats_list:
        for k in ("nodes", "infeasible", "good_prunes", "leaves", "dedupe_skips"):
            total[k] += st[k]
        for k, v in st["leaf_hull_dims"].items():
            total["leaf_hull_dims"][k] = total["leaf_hull_dims"].get(k, 0) + v
        for k, v in st["target_hits"].items():
            total["target_hits"][k] = total["target_hits"].get(k, 0) + v
        total["counterexamples"].extend(st["counterexamples"])
        total["branches"].append({"a_edges": [list(x) for x in e], "b_edges": [list(x) for x in f], "nodes": st["nodes"], "leaves": st["leaves"]})
        lines.update(ll)
    return total, lines


def main():
    import multiprocessing as mp
    ap = argparse.ArgumentParser()
    ap.add_argument("--points", type=int, default=6)
    ap.add_argument("--jobs", type=int, default=max(1, mp.cpu_count() - 1))
    ap.add_argument("--out", type=Path, default=TOOL_DIR / "evidence")
    ap.add_argument("--order", choices=("largest", "smallest"), default="largest",
                    help="process lengths from the largest (default) or the smallest")
    ap.add_argument("--split-depth", type=int, default=4, help="depth at which branches are handed to processes")
    args = ap.parse_args()
    largest_first = args.order == "largest"
    args.out.mkdir(parents=True, exist_ok=True)
    logf = open(args.out / f"log-{args.points}.txt", "a")

    def log(msg):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        logf.write(line + "\n")
        logf.flush()

    t0 = time.monotonic()
    log(f"start points={args.points} jobs={args.jobs}")
    s = Search(args.points, log, largest_first)
    log(f"order={args.order} targets={len(s.targets)} ({sum(1 for n,_ in s.targets if n.startswith('bloom'))} Bloom lines, 2 congruent subspaces)")
    states = s.first_level(args.split_depth)
    tasks = [(args.points, largest_first, st) for st in states]
    log(f"driver: nodes={s.stats['nodes']} infeasible={s.stats['infeasible']} good={s.stats['good_prunes']} to depth {args.split_depth}; tasks={len(tasks)}")
    results = []
    with mp.Pool(args.jobs) as pool:
        for r in pool.imap_unordered(_worker, tasks):
            results.append(r)
            e, f, st, _ = r
            log(f"branch A{e} B{f} done: nodes={st['nodes']} leaves={st['leaves']} good={st['good_prunes']} infeasible={st['infeasible']} ce={len(st['counterexamples'])} ({len(results)}/{len(tasks)}) t={time.monotonic()-t0:.0f}s")
    stats, lines = merge(results)
    # add the driver's own counts above the split depth
    for k in ("nodes", "infeasible", "good_prunes", "dedupe_skips"):
        stats[k] += s.stats[k]
    for k, v in s.stats["target_hits"].items():
        stats["target_hits"][k] = stats["target_hits"].get(k, 0) + v
    stats["order"] = args.order
    stats["split_depth"] = args.split_depth
    stats["seconds"] = time.monotonic() - t0
    stats["points"] = args.points
    stats["jobs"] = args.jobs
    stats["distinct_leaf_hulls"] = len(lines)
    stats["leaf_hull_targets"] = sorted(set(lines.values()))
    stats["bloom_lines_known"] = sum(1 for n, _ in s.targets if n.startswith("bloom"))
    stats["verdict"] = ("every feasible leaf lies in a Bloom line or the congruent locus"
                        if not stats["counterexamples"] else "COUNTEREXAMPLE CANDIDATES FOUND")
    (args.out / f"summary-{args.points}.json").write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n")
    log(json.dumps({k: v for k, v in stats.items() if k not in ("counterexamples", "branches")}, sort_keys=True))
    log(f"verdict: {stats['verdict']}")


if __name__ == "__main__":
    main()
