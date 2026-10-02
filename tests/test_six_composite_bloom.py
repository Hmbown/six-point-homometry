"""Exact reference, singular-stratum, checkpoint and certificate controls."""
from collections import Counter
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import pickle
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from homometry import dihedral_canon, icv
from six_composite_bloom import (canonical, classify, enumerate_composite, factors,
                                is_unit_separated, local_support_profile,
                                parameter_orbit, points, read_certificate,
                                reference_parameter_pairs, summarize)


def certificate_records(path):
    """Stream our public JSON header and records; keep the audit memory bounded."""
    marker = ',"fibers":['
    decoder = json.JSONDecoder()
    with gzip.open(path,"rt") as stream:
        buffer = ""
        while marker not in buffer:
            chunk = stream.read(65536)
            assert chunk, "missing fibre list"
            buffer += chunk
        header,buffer = buffer.split(marker,1)
        yield json.loads(header+"}")
        while True:
            buffer = buffer.lstrip()
            if buffer.startswith("]}"):
                assert not (buffer[2:]+stream.read()).strip(), "trailing certificate text"
                return
            if buffer.startswith(","):
                buffer = buffer[1:].lstrip()
            try:
                record,end = decoder.raw_decode(buffer)
            except json.JSONDecodeError:
                chunk = stream.read(65536)
                assert chunk, "truncated fibre record"
                buffer += chunk
                continue
            assert isinstance(record,dict)
            yield record
            buffer = buffer[end:]


def test_canonical_every_small_parameter_and_subsets():
    for n in range(2, 10):
        for mask in range(1 << n):
            endpoint = tuple(i for i in range(n) if mask >> i & 1)
            assert canonical(endpoint, n) == dihedral_canon(endpoint, n)
    for n in range(2, 44):
        for a in range(n):
            for b in range(n):
                for endpoint in points(a, b, n):
                    distinct = tuple(sorted(set(endpoint)))
                    assert canonical(endpoint, n) == dihedral_canon(distinct, n), (n, a, b)
    assert canonical((-4, 4, 12), 8) == (0,)
    try:
        canonical((1,), 0)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid modulus accepted")


def test_full_reference_parameter_images_through_43():
    for n in range(2, 44):
        direct = enumerate_composite(n)
        actual = {pair: list(codes) for pair, codes in direct.fibers.items()}
        assert actual == reference_parameter_pairs(n), n
        assert sum(direct.counts.values()) == n*n
        assert sum(map(len, direct.fibers.values())) == direct.counts["admissible"]
        for category, codes in direct.excluded.items():
            assert len(codes) == direct.counts[category]
            assert all(classify(*divmod(code, n), n) == (category, None) for code in codes)


def test_formal_directed_differences_and_parameter_action():
    # Independent integer coefficient configurations; not obtained from points().
    x = ((0,0), (1,0), (-2,1), (-2,2), (0,2), (-1,3))
    y = ((0,0), (1,0), (2,1), (-1,2), (1,2), (-1,3))
    def differences(config):
        return Counter((a-c,b-d) for a,b in config for c,d in config)
    assert differences(x) == differences(y)
    for n in (8, 9, 12, 13, 25, 35, 49, 169, 221):
        for a, b in ((0,0), (0,1), (1,4), (2,7), (n-1,n//2)):
            category, pair = classify(a, b, n)
            for code in parameter_orbit(a,b,n):
                assert classify(*divmod(code,n),n) == (category,pair), (n,a,b,code)


def test_local_support_and_unit_separation_exactly():
    for n in (25, 35, 49, 169, 221, 289):
        result = enumerate_composite(n)
        primes = tuple(p for p,_ in factors(n))
        unit_parameters = 0
        for a in range(n):
            for b in range(n):
                xx, yy = points(a,b,n)
                local = tuple(tuple(sorted((len({x % p for x in xx}),
                                             len({y % p for y in yy})))) for p in primes)
                assert local_support_profile(a,b,primes) == local
                if all(sizes == (6,6) for sizes in local):
                    assert classify(a,b,n)[0] == "admissible"
                    unit_parameters += 1
        summary = summarize(result)
        assert summary["unit_separated_parameters"] == unit_parameters
        if n in (25,35,49):
            assert unit_parameters == 0
        else:
            assert summary["unit_separated_candidate"]["matches"]
        assert sum(sum(s["parameter_counts"].values()) for s in summary["local_support_strata"]) == n*n
        assert sum(s["pairs"] for s in summary["local_support_strata"]) == summary["pairs"]


def test_exact_benchmarks_and_unquotiented_crt_signs():
    expected = {169: (2212,338), 221: (3850,192), 289: (6672,2312)}
    for n,(total,unit) in expected.items():
        summary = summarize(enumerate_composite(n))
        assert (summary["pairs"], summary["unit_separated_pairs"]) == (total,unit)
        assert summary["fiber_histogram"] == {12:total}
        assert summary["G_orbits_per_fiber_histogram"] == {1:total}
        assert summary["full_graph"]["component_size_histogram"] == {2:total}
    n,t = 221,118
    assert t*t % n == 1 and t not in (1,n-1)
    assert t % 13 == 1 and t % 17 == 16
    first = classify(1,4,n)[1]
    second = classify(118,30,n)[1]
    assert first is not None and second is not None and first != second
    assert 118*n+30 not in parameter_orbit(1,4,n)
    for pair in (first,second):
        assert pair[0] != pair[1] and icv(pair[0],n) == icv(pair[1],n)
        assert all(dihedral_canon(endpoint,n) == endpoint for endpoint in pair)
    def key(a,b):
        return ((a*a-a*b+b*b) % n, (a*b*(a-b))**2 % n)
    assert key(1,4) == key(118,30) == (13,144)


def test_resumable_checkpoint_and_digest_bound():
    with TemporaryDirectory() as temporary:
        checkpoint = Path(temporary)/"checkpoint.gz"
        first = enumerate_composite(13,checkpoint=checkpoint,checkpoint_seconds=0)
        assert checkpoint.exists()
        resumed = enumerate_composite(13,checkpoint=checkpoint,resume=True)
        assert first.fibers == resumed.fibers
        assert first.counts == resumed.counts and first.local_counts == resumed.local_counts
        with gzip.open(checkpoint,"rb") as stream:
            saved = pickle.load(stream)
        assert 0 < saved["enumeration"].next_row < 13
        saved["source_sha256"] = "bad-digest"
        with gzip.open(checkpoint,"wb") as stream:
            pickle.dump(saved,stream)
        try:
            enumerate_composite(13,checkpoint=checkpoint,resume=True)
        except ValueError as error:
            assert "digest" in str(error)
        else:
            raise AssertionError("wrong source checkpoint accepted")


def test_every_saved_fiber_and_parameter_partition():
    source_hash = hashlib.sha256((ROOT/"src/six_composite_bloom.py").read_bytes()).hexdigest()
    reference_hash = hashlib.sha256((ROOT/"src/homometry.py").read_bytes()).hexdigest()
    directory = ROOT/"results/2026-09-30-six-composite-count"
    for path in sorted(directory.glob("n*.json.gz")):
        records = certificate_records(path)
        certificate = next(records)
        assert certificate["source_sha256"] == source_hash
        assert certificate["reference_sha256"] == reference_hash
        summary = certificate["summary"]
        n = summary["n"]
        primes = tuple(p for p,_ in factors(n))
        visited = bytearray(n*n)
        histogram, orbit_histogram, unit_histogram = Counter(),Counter(),Counter()
        previous_pair = None
        pair_count = 0
        for record in records:
            pair_count += 1
            pair = tuple(tuple(endpoint) for endpoint in record["pair"])
            assert pair[0] < pair[1]
            assert previous_pair is None or previous_pair < pair
            previous_pair = pair
            codes = record["parameter_codes"]
            assert codes == sorted(codes) and len(set(codes)) == len(codes)
            assert classify(*divmod(codes[0],n),n) == ("admissible",pair)
            profile = local_support_profile(*divmod(codes[0],n),primes)
            assert tuple(tuple(s) for s in record["local_support_sizes"]) == profile
            remaining,orbits = set(codes),0
            while remaining:
                orbit = parameter_orbit(*divmod(min(remaining),n),n)
                assert orbit <= remaining
                remaining -= orbit
                orbits += 1
            orbit_histogram[orbits] += 1
            histogram[len(codes)] += 1
            if is_unit_separated(profile):
                unit_histogram[len(codes)] += 1
            for code in codes:
                assert 0 <= code < n*n and visited[code] == 0
                visited[code] = 1
        for category,codes in certificate["excluded_parameter_codes"].items():
            assert len(codes) == summary[category+"_parameters"]
            for code in codes:
                assert 0 <= code < n*n and visited[code] == 0
                visited[code] = 1
            # Full small controls; excluded samples spread throughout large rings.
            controls = codes if n <= 43 else codes[::max(1,len(codes)//16)]
            assert all(classify(*divmod(code,n),n) == (category,None) for code in controls)
        assert all(visited)
        assert dict(histogram) == {int(k):v for k,v in summary["fiber_histogram"].items()}
        assert dict(orbit_histogram) == {int(k):v for k,v in summary["G_orbits_per_fiber_histogram"].items()}
        assert dict(unit_histogram) == {int(k):v for k,v in summary["unit_separated_fiber_histogram"].items()}
        assert sum(k*v for k,v in histogram.items()) == summary["admissible_parameters"]
        assert sum(unit_histogram.values()) == summary["unit_separated_pairs"]
        assert pair_count == summary["pairs"]


def test_validation_and_graph_boundary():
    for bad in (0,1,-5,True,1.5):
        try:
            enumerate_composite(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted {bad!r}")
    assert factors(637) == ((7,2),(13,1))
    # The established characteristic31 boundary must remain a shared endpoint.
    summary = summarize(enumerate_composite(31))
    assert summary["pairs"] == 50
    assert summary["full_graph"]["shared_endpoint_classes"] > 0
    assert summary["full_graph"]["maximum_degree"] > 1
    boundary = enumerate_composite(31)
    degrees = Counter(endpoint for pair in boundary.fibers for endpoint in pair)
    shared = {endpoint for endpoint,d in degrees.items() if d > 1}
    edges = {pair for pair in boundary.fibers if any(endpoint in shared for endpoint in pair)}
    assert len(shared) == len(edges) == 5 and all(degrees[endpoint] == 2 for endpoint in shared)
    for n,multiplier in ((403,13),(961,31)):
        path = ROOT/f"results/2026-09-30-six-composite-count/n{n}.json.gz"
        if not path.exists():
            continue
        expected_shared = {tuple(multiplier*x for x in endpoint) for endpoint in shared}
        expected_edges = {tuple(tuple(multiplier*x for x in endpoint) for endpoint in pair)
                          for pair in edges}
        records = certificate_records(path)
        metadata = next(records)
        graph = metadata["summary"]["full_graph"]
        assert graph["shared_endpoint_classes"] == 5 and graph["maximum_degree"] == 2
        assert {tuple(rec["endpoint"]) for rec in graph["shared_endpoint_examples"]} == expected_shared
        assert metadata["summary"]["unit_separated_graph"]["shared_endpoint_classes"] == 0
        actual_edges = set()
        for rec in records:
            pair = tuple(tuple(endpoint) for endpoint in rec["pair"])
            if any(endpoint in expected_shared for endpoint in pair):
                actual_edges.add(pair)
        assert actual_edges == expected_edges


if __name__ == "__main__":
    for test in (test_canonical_every_small_parameter_and_subsets,
                 test_full_reference_parameter_images_through_43,
                 test_formal_directed_differences_and_parameter_action,
                 test_local_support_and_unit_separation_exactly,
                 test_exact_benchmarks_and_unquotiented_crt_signs,
                 test_resumable_checkpoint_and_digest_bound,
                 test_every_saved_fiber_and_parameter_partition,
                 test_validation_and_graph_boundary):
        test()
        print("PASS",test.__name__,flush=True)
