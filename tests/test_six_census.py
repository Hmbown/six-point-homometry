"""Independent six-subset census regressions; pinned Python."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from homometry import bracelets, z_families
from six_census import point_census, gap_census


def test_reference():
    for n in range(6, 19):
        families, classes = point_census(n)
        reference = {v: sorted(m) for v, m in z_families(n, sizes=[6]).items()}
        assert families == reference == gap_census(n), n
        assert classes == sum(1 for _ in bracelets(n, 6)), n


def test_known_and_two_word_signatures():
    for n in (12, 21, 32, 33, 34):
        families, _ = point_census(n)
        assert families == gap_census(n), n
        if n == 12:
            assert len(families) == 15
        if n == 21:
            pair = [(0, 1, 3, 7, 10, 15), (0, 1, 4, 7, 14, 16)]
            assert pair in families.values()


if __name__ == "__main__":
    test_reference()
    print("PASS reference six-note families and class counts n=6..18", flush=True)
    test_known_and_two_word_signatures()
    print("PASS independent gap enumeration and 64-bit boundary", flush=True)
