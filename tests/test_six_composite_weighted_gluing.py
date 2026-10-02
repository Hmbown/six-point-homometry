"""Independent controls for actual ring collisions and weighted label gluing."""
from collections import Counter, defaultdict
from itertools import permutations, product
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import six_composite_weighted_gluing as proof


def modular_values(rows, v, modulus):
    return tuple((a * v[0] + b * v[1]) % modulus for a, b in rows)


def block_autos(values):
    # Independent generation by equal-coordinate blocks, rather than filtering S6.
    blocks = defaultdict(list)
    for index, value in enumerate(values):
        blocks[value].append(index)
    groups = list(blocks.values())
    out = set()
    for choices in product(*(tuple(permutations(block)) for block in groups)):
        perm = list(range(6))
        for block, image in zip(groups, choices):
            for source, target in zip(block, image):
                perm[source] = target
        out.add(tuple(perm))
    return out


def test_collision_partitions_stable_in_actual_prime_power_rings():
    for p in (13, 17, 19, 31):
        modulus = p * p
        for line in proof.LINES:
            for scale in (1, 2, p - 1):
                v = tuple(scale * coordinate % modulus for coordinate in line)
                for rows in (proof.CX, proof.CY):
                    actual = block_autos(modular_values(rows, v, modulus))
                    rational = set(proof.positive_autos(rows, line))
                    assert actual == rational


def test_near_collision_is_distinct_at_actual_ring_modulus():
    p = 13
    modulus = p * p
    for a, b in proof.LINES:
        # The normal(b,-a) takes a unit value on the chosen perturbation.
        v = (a + p, b) if b else (a, b + p)
        for rows in (proof.CX, proof.CY):
            assert len(set(modular_values(rows, v, p))) < 6
            actual = modular_values(rows, v, modulus)
            assert len(set(actual)) == 6
            assert block_autos(actual) == {tuple(range(6))}


def test_collision_lists_do_not_reflect_at_boundary_primes():
    for p in (13, 17, 19, 31):
        for line in proof.LINES:
            for rows in (proof.CX, proof.CY):
                values = modular_values(rows, line, p)
                assert Counter(values) != Counter((-value) % p for value in values)


def test_independent_block_generation_covers_all_gluing_patterns():
    rotations = {}
    R = ((0, -1), (1, -1))
    for name, rows in (("X", proof.CX), ("Y", proof.CY)):
        transformed = tuple(tuple(sum(row[h] * R[h][j] for h in range(2))
                                  for j in range(2)) for row in rows)
        rho = tuple(rows.index(row) for row in transformed)
        rotations[name] = (tuple(range(6)), rho,
                           tuple(rho[rho[i]] for i in range(6)))
    paired = defaultdict(set)
    single = {"X": defaultdict(set), "Y": defaultdict(set)}
    for li, line in enumerate(proof.LINES):
        groups = {name: block_autos(modular_values(rows, line, 169))
                  for name, rows in (("X", proof.CX), ("Y", proof.CY))}
        for i in range(3):
            for hx, hy in product(groups["X"], groups["Y"]):
                px = tuple(hx[rotations["X"][i][j]] for j in range(6))
                py = tuple(hy[rotations["Y"][i][j]] for j in range(6))
                paired[px, py].add((i, li))
                single["X"][px].add((i, li))
                single["Y"][py].add((i, li))
    certificate = proof.gluing_certificate()
    recorded = {(tuple(row["permutation_X"]), tuple(row["permutation_Y"])):
                set(row["witnesses"]) for row in certificate["paired_patterns"]}
    assert paired == recorded
    assert len(paired) == 219
    for name in ("X", "Y"):
        saved = {tuple(row["permutation"]): set(row["witnesses"])
                 for row in certificate["endpoint"][name]["positive_patterns"]}
        assert saved == single[name]
        assert len(saved) == 57


def test_reflection_cosets_from_actual_field_point_matchings():
    for name, rows, slopes in (("X", proof.CX, {13: 10, 19: 8}),
                               ("Y", proof.CY, {13: 4, 19: 12})):
        negatives = []
        for p, slope in slopes.items():
            values = modular_values(rows, (1, slope), p)
            assert len(set(values)) == 6
            chi = tuple(values.index((-value) % p) for value in values)
            assert chi == proof.CHI[name][p]
            rho = proof.RHO_X if name == "X" else proof.RHO_Y
            for rotation in proof.powers(rho):
                negatives.append(tuple(chi[rotation[i]] for i in range(6)))
        assert len(set(negatives)) == 6
        positives = {tuple(row["permutation"]) for row in
                     proof.gluing_certificate()["endpoint"][name]["positive_patterns"]}
        assert positives.isdisjoint(negatives)


def test_moment_and_weighted_collision_lift_certificates():
    assert set(proof.moment_certificate()) == {"X", "Y"}
    extension = proof.weighted_lift_extension()
    assert sum(row["patterns"] for row in extension.values()) == 64
    assert all(row["all_collision_branches_give_w_v"] for row in extension.values())


if __name__ == "__main__":
    tests = [value for name, value in globals().items()
             if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
        print("PASS", test.__name__)
    print(f"PASS {len(tests)}/{len(tests)} weighted gluing groups")
