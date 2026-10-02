"""Baseline regression tests. Run:  python tests/run_tests.py
Any faster/rewritten implementation MUST pass these (and match src/homometry.py
on every n it is used for) before its results are recorded."""
import os, random, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from homometry import *

def test_classic_tetrachords():
    A, B = (0, 1, 4, 6), (0, 1, 3, 7)
    assert icv(A, 12) == icv(B, 12) == (1, 1, 1, 1, 1, 1)
    assert dihedral_canon(A, 12) != dihedral_canon(B, 12)
    assert dft_magnitudes(A, 12) == dft_magnitudes(B, 12)
    # NOT homometric as integer sets (distance multisets differ on the line)
    lin = lambda s: sorted(abs(a - b) for a, b in combinations(s, 2))
    assert lin(A) != lin(B)

def test_z12_census():
    fams = z_families(12)
    assert len(fams) == 23
    by = Counter(len(c[0]) for c in fams.values())
    assert by == Counter({6: 15, 5: 3, 7: 3, 4: 1, 8: 1})
    assert max(len(c) for c in fams.values()) == 2

def test_bracelet_counts():
    # number of T_n/I classes of all subsets of Z_12 is 224 (incl. empty & full)
    assert sum(1 for k in range(13) for _ in bracelets(12, k)) == 224

def test_hexachord_theorem():
    for n in (8, 10, 12, 14):
        for s in bracelets(n, n // 2):
            assert icv(s, n) == icv(complement(s, n), n)

def test_complement_transfer():
    # ICV of complement is determined by ICV of the set (all sizes)
    n = 12
    seen = {}
    for k in range(2, 11):
        for s in bracelets(n, k):
            key = (k, icv(s, n))
            val = icv(complement(s, n), n)
            assert seen.setdefault(key, val) == val

def test_direct_sum_flip_is_sound():
    rng = random.Random(0)
    hits = 0
    for _ in range(4000):
        n = rng.randint(8, 24)
        B = {0} | set(rng.sample(range(1, n), rng.randint(1, 3)))
        C = {0} | set(rng.sample(range(1, n), rng.randint(1, 3)))
        S = {(b + c) % n for b in B for c in C}
        F = {(b - c) % n for b in B for c in C}
        if len(S) == len(B) * len(C) == len(F):
            hits += 1
            assert icv(sorted(S), n) == icv(sorted(F), n)
    assert hits > 100

def test_k2_deck_is_z_relation():
    n = 12
    for k in (4, 5, 6):
        g2 = sorted(sorted(x) for x in higher_order_families(n, 2, sizes=[k]))
        gz = sorted(sorted(c) for c in z_families(n, sizes=[k]).values())
        assert g2 == gz

def test_no_3deck_families_small():
    for n in range(8, 15):
        assert higher_order_families(n, 3) == []

def test_erickson_jones_k5_reproduction():
    from validate_literature import brute_k5, ej_types, ej_gf_coeffs
    h = ej_gf_coeffs(24)
    for n in range(5, 25):
        brute = brute_k5(n)
        typed = sorted({tuple(sorted(cl)) for _, cl in ej_types(n, True)})
        assert [list(t) for t in typed] == brute, n
        assert len(brute) == h[n], n

def test_integer_shadow_pair():
    A, B = (0, 1, 4, 10, 12, 17), (0, 1, 8, 11, 13, 17)
    lin = lambda s: sorted(abs(a - b) for a, b in combinations(s, 2))
    assert lin(A) == lin(B)
    for n in range(18, 60):
        assert icv(A, n) == icv(B, n) and dihedral_canon(A, n) != dihedral_canon(B, n)

if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print("PASS", name)
            except AssertionError as e:
                fails += 1; print("FAIL", name, e)
    sys.exit(1 if fails else 0)
