"""Independent adversarial audit of the six-point line classification.

Imports none of the classification/SMT builders.  The solver model uses
positive consecutive gaps and a bijection of edge occurrences, whereas the
builder uses point coordinates and equality of multiplicity counts.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
from itertools import combinations, combinations_with_replacement
import json
from math import comb
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from homometry import icv


def normalize(points):
    p = sorted(points)
    p = tuple(x - p[0] for x in p)
    return p if p[-2] >= p[-1] - p[1] else tuple(p[-1] - x for x in p[::-1])


def member(a, b):
    """Recover parameters from actual points, without any matrix helper."""
    a, b = sorted((normalize(a), normalize(b)))
    p, q = a[5] - a[4], a[2]
    one = p > 0 and q > 3*p and a == (0,q-2*p,q,2*q-3*p,3*q-2*p,3*q-p) and b == (0,q-p,q+p,2*q+p,3*q-2*p,3*q-p)
    p, q = a[4] - a[3], a[1] + a[4] - a[3]
    two = p > 0 and 3*p < 2*q < 4*p and a == (0,q-p,q+p,3*q-2*p,3*q-p,2*q+p) and b == (0,p,2*q-p,q+2*p,3*q-p,2*q+p)
    return int(one) + int(two)


def distance_multiset(p):
    return tuple(sorted(y-x for x,y in combinations(p,2)))


def formal_audit():
    normal_forms=[
        (((0,0),(-2,1),(0,1),(-3,2),(-2,3),(-1,3)),
         ((0,0),(-1,1),(1,1),(1,2),(-2,3),(-1,3))),
        (((0,0),(-1,1),(1,1),(-2,3),(-1,3),(1,2)),
         ((0,0),(1,0),(-1,2),(2,1),(-1,3),(1,2)))]
    def diff(u,v): return tuple(x-y for x,y in zip(u,v))
    for a,b in normal_forms:
        assert Counter(diff(v,u) for u,v in combinations(a,2)) == Counter(diff(v,u) for u,v in combinations(b,2))
    x=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3))
    y=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3))
    assert Counter(diff(u,v) for u in x for v in x)==Counter(diff(u,v) for u in y for v in y)
    endpoint=(-1,3)
    assert set(normal_forms[0][0])=={diff(endpoint,v) for v in y}
    assert set(normal_forms[0][1])=={diff(endpoint,v) for v in x}
    assert set(normal_forms[1][0])=={diff(endpoint,v) for v in x}
    assert set(normal_forms[1][1])==set(y)
    pair=((0,1,4,10,12,17),(0,1,8,11,13,17))
    for sign_a in (-1,1):
        for sign_b in (-1,1):
            for swap in (False,True):
                a=tuple(sign_a*x+131 for x in pair[0])
                b=tuple(sign_b*x-73 for x in pair[1])
                assert member(*( (b,a) if swap else (a,b) ))==1
    return dict(formal_normal_form_identities=2,formal_bloom_autocorrelation=True,
                explicit_bloom_rigid_motions=True,rigid_motion_controls=8)


def finite_audit(maximum):
    start = time.monotonic()
    classes = pairs = repeated = 0
    all_pairs = set()
    histogram = Counter()
    for diameter in range(5, maximum+1):
        fibres = defaultdict(list)
        for middle in combinations(range(1,diameter),4):
            p = (0,*middle,diameter)
            if p > tuple(diameter-x for x in p[::-1]):
                continue
            classes += 1
            fibres[distance_multiset(p)].append(p)
        for distances, fibre in fibres.items():
            for a,b in combinations(fibre,2):
                assert member(a,b) == 1, (a,b)
                # At modulus 2L+1 all positive line distances are unchanged.
                assert icv(a,2*diameter+1) == icv(b,2*diameter+1)
                pairs += 1
                all_pairs.add((a,b))
                repeated += len(set(distances)) < 15
                histogram[diameter] += 1
    assert classes == sum((comb(d-1,4)+comb((d-1)//2,2))//2 for d in range(5,maximum+1))
    generated=set()
    for p in range(1,maximum+1):
        for q in range(1,maximum+1):
            if q>3*p:
                a=(0,q-2*p,q,2*q-3*p,3*q-2*p,3*q-p)
                b=(0,q-p,q+p,2*q+p,3*q-2*p,3*q-p)
            elif 3*p<2*q<4*p:
                a=(0,q-p,q+p,3*q-2*p,3*q-p,2*q+p)
                b=(0,p,2*q-p,q+2*p,3*q-p,2*q+p)
            else: continue
            if a[-1]<=maximum:
                a=min(a,tuple(a[-1]-v for v in a[::-1]))
                b=min(b,tuple(b[-1]-v for v in b[::-1]))
                generated.add(tuple(sorted((a,b))))
    assert generated==all_pairs,(generated-all_pairs,all_pairs-generated)
    return dict(max_diameter=maximum, reflection_classes=classes, pairs=pairs,
                class_count_independent_formula=True, pair_count_independent_generation=True,
                repeated_distance_pairs=repeated, pairs_by_diameter=dict(histogram),
                seconds=time.monotonic()-start)


def sum_expr(parts):
    return parts[0] if len(parts)==1 else "(+ " + " ".join(parts) + ")"


def conjunction(parts):
    return "(and " + " ".join(parts) + ")"


def model(exclude=True, distances=True, fixed=None, weighted=False, order_matches=False):
    """Exact independent SMT-LIB: positive gaps + edge bijection."""
    a = [f"x{i}" for i in range(4)] + ["t"]
    b = [f"y{i}" for i in range(4)] + ["t"]
    variables = a[:-1]+b
    lines = ["(set-logic QF_LRA)"]
    lines += [f"(declare-fun {v} () Real)" for v in variables]
    inequality = ">=" if weighted else ">"
    assertions = [f"({inequality} {v} 0)" for v in variables]
    assertions += [f"(= {sum_expr(a)} 1)", f"(= {sum_expr(b)} 1)","(>= x0 t)","(>= y0 t)"]
    lex = [conjunction([f"(= {a[j]} {b[j]})" for j in range(i)]+[f"(< {a[i]} {b[i]})"]) for i in range(4)]
    assertions += ["(or " + " ".join(lex) + ")"]
    assertions += ["(not " + conjunction([f"(= {u} {v})" for u,v in zip(a,b[::-1])]) + ")"]
    # The endpoint triangle has distances 1-t, 1 and t in both sets.
    # Cancel these three OCCURRENCES, also when their values coincide with
    # other edges.  The remaining twelve occurrences need a bijection.
    edges = [(i,j) for i,j in combinations(range(6),2) if (i,j) not in ((0,4),(0,5),(4,5))]
    left = [sum_expr(a[i:j]) for i,j in edges]
    right = [sum_expr(b[i:j]) for i,j in edges]
    if distances:
        # Equal-distance occurrences can always be matched in increasing
        # edge-index order.  This removes factorial duplicate matchings and
        # does not remove any equality of multisets, including zero values.
        if order_matches:
            lines += [f"(declare-fun index_{i} () Real)" for i in range(12)]
        for i in range(12):
            for j in range(12):
                lines.append(f"(declare-fun m_{i}_{j} () Bool)")
                assertions.append(f"(=> m_{i}_{j} (= {left[i]} {right[j]}))")
                if order_matches:
                    assertions.append(f"(=> m_{i}_{j} (= index_{i} {j}))")
            assertions.append("(or " + " ".join(f"m_{i}_{j}" for j in range(12)) + ")")
        # One selection per row and at most one per column gives a bijection
        # by pigeonhole, without assuming the distance values are distinct.
        for j in range(12):
            for i,k in combinations(range(12),2):
                assertions.append(f"(not (and m_{i}_{j} m_{k}_{j}))")
        if order_matches:
            for i,k in combinations(range(12),2):
                assertions.append(f"(=> (= {left[i]} {left[k]}) (< index_{i} index_{k}))")
    if exclude:
        one = ["(= x1 (* 2 t))", "(= x2 (- x0 t))", "(= x3 (+ x0 (* 3 t)))",
               "(= y0 (+ x0 t))", "(= y1 (* 2 t))", "(= y2 (+ x0 (* 2 t)))", "(= y3 (- x0 t))"]
        two = ["(= x1 (* 2 x3))", "(= x2 (- (* 2 x0) x3))", "(= t (- x3 x0))",
               "(= y0 x3)", "(= y1 (* 2 x0))", "(= y2 (- (* 2 x3) x0))", "(= y3 (- (* 2 x0) x3))"]
        assertions += ["(not " + conjunction(one) + ")", "(not " + conjunction(two) + ")"]
    if fixed:
        p,q = sorted((normalize(fixed[0]),normalize(fixed[1])))
        assert p[-1] == q[-1] and p[-2] == q[-2]
        gaps_a = [Fraction(v-u,p[-1]) for u,v in zip(p,p[1:])]
        gaps_b = [Fraction(v-u,q[-1]) for u,v in zip(q,q[1:])]
        for v,z in zip(variables,gaps_a[:-1]+gaps_b):
            assertions.append(f"(= {v} (/ {z.numerator} {z.denominator}))")
    lines += [f"(assert {p})" for p in assertions]
    lines.append("(check-sat)")
    return "\n".join(lines)+"\n"


def run_cvc5(source, module_dir, timeout, proof_path=None):
    sys.path.insert(0,module_dir)
    import cvc5
    solver = cvc5.Solver()
    solver.setOption("tlimit-per",str(timeout*1000))
    solver.setOption("produce-proofs","true")
    solver.setOption("check-proofs","true")
    solver.setOption("proof-check", "eager")
    parser = cvc5.InputParser(solver)
    parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6,source,"independent-gap-bijection")
    symbols = parser.getSymbolManager()
    outputs = []
    start = time.monotonic()
    while True:
        cmd = parser.nextCommand()
        if cmd.isNull(): break
        value = cmd.invoke(solver,symbols).strip()
        if value: outputs.append(value)
    proof_metadata = {}
    if outputs == ["unsat"] and proof_path:
        proof = solver.proofToString(solver.getProof()[0])
        if isinstance(proof,bytes): proof=proof.decode()
        with gzip.open(proof_path,"wt") as f: f.write(proof)
        proof_metadata = dict(proof_path=str(proof_path), proof_sha256=hashlib.sha256(proof.encode()).hexdigest(), proof_bytes=len(proof))
    return dict(solver="cvc5", version=cvc5.__version__, outputs=outputs,
                seconds=time.monotonic()-start, source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                check_proofs=True, proof_check="eager", **proof_metadata)


def controls(module_dir):
    examples = [((0,1,4,10,12,17),(0,1,8,11,13,17)),
                ((0,1,2,6,8,11),(0,1,6,7,9,11))]
    results = []
    for pair in examples:
        assert member(*pair)==1
        for exclude,want in [(False,"sat"),(True,"unsat")]:
            result=run_cvc5(model(exclude=exclude,fixed=pair),module_dir,15)
            assert result["outputs"]==[want],result
            results.append(dict(pair=pair,exclude=exclude,**result))
    for name,source,want in [
        ("outside_without_homometry",model(distances=False),"sat"),
        ("nonhomometric",model(exclude=False,fixed=((0,1,4,10,12,17),(0,1,8,10,13,17))),"unsat")]:
        result=run_cvc5(source,module_dir,15)
        assert result["outputs"]==[want],result
        results.append(dict(control=name,**result))
    return results


def weighted_audit(maximum=20):
    """All unordered integer six-atom multisets, not just six-point sets."""
    start=time.monotonic()
    classes=pairs=collisions=0
    all_pairs=set()
    for diameter in range(1,maximum+1):
        fibres=defaultdict(list)
        for middle in combinations_with_replacement(range(diameter+1),4):
            a=(0,*middle,diameter)
            reflected=tuple(diameter-x for x in a[::-1])
            if a>reflected: continue
            classes+=1
            fibres[distance_multiset(a)].append(a)
        for fibre in fibres.values():
            for a,b in combinations(fibre,2):
                pairs+=1
                all_pairs.add((a,b))
                aa,bb=sorted((normalize(a),normalize(b)))
                p,q=aa[5]-aa[4],aa[2]
                one=(p>0 and q>=3*p and aa==(0,q-2*p,q,2*q-3*p,3*q-2*p,3*q-p) and bb==(0,q-p,q+p,2*q+p,3*q-2*p,3*q-p))
                p,q=aa[4]-aa[3],aa[1]+aa[4]-aa[3]
                two=(p>0 and 3*p<=2*q<4*p and aa==(0,q-p,q+p,3*q-2*p,3*q-p,2*q+p) and bb==(0,p,2*q-p,q+2*p,3*q-p,2*q+p))
                assert one or two,(a,b)
                if len(set(a))<6 or len(set(b))<6:
                    collisions+=1
                    assert len(set(a))==len(set(b))==5
                    assert diameter%8==0
                    scale=diameter//8
                    boundary_a=tuple(scale*z for z in (0,1,3,3,7,8))
                    boundary_b=tuple(scale*z for z in (0,2,4,7,7,8))
                    boundary_a=min(boundary_a,tuple(diameter-v for v in boundary_a[::-1]))
                    boundary_b=min(boundary_b,tuple(diameter-v for v in boundary_b[::-1]))
                    assert (a,b)==tuple(sorted((boundary_a,boundary_b)))
    expected=sum((comb(d+4,4)+comb((d+1)//2+1+(d%2==0),2))//2 for d in range(1,maximum+1))
    assert classes==expected,(classes,expected)
    generated=set()
    for p in range(1,maximum+1):
        for q in range(1,maximum+1):
            if q>=3*p:
                a=(0,q-2*p,q,2*q-3*p,3*q-2*p,3*q-p)
                b=(0,q-p,q+p,2*q+p,3*q-2*p,3*q-p)
            elif 3*p<=2*q<4*p:
                a=(0,q-p,q+p,3*q-2*p,3*q-p,2*q+p)
                b=(0,p,2*q-p,q+2*p,3*q-p,2*q+p)
            else: continue
            if a[-1]<=maximum:
                a=min(a,tuple(a[-1]-v for v in a[::-1]))
                b=min(b,tuple(b[-1]-v for v in b[::-1]))
                generated.add(tuple(sorted((a,b))))
    assert generated==all_pairs,(generated-all_pairs,all_pairs-generated)
    return dict(max_diameter=maximum,reflection_classes=classes,pairs=pairs,
                class_count_independent_formula=True,pair_count_independent_generation=True,
                collision_pairs=collisions,seconds=time.monotonic()-start)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="results/2026-09-30-six-integer-review")
    parser.add_argument("--max-diameter",type=int,default=40)
    parser.add_argument("--module-dir",default="/tmp/babbitt-six-cvc5")
    parser.add_argument("--timeout",type=int,default=60)
    parser.add_argument("--solver-only",action="store_true")
    parser.add_argument("--weighted",action="store_true")
    parser.add_argument("--order-matches",action="store_true")
    args=parser.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    result={"status":"COMPUTED independent review", "encoding":"positive gaps and edge-occurrence bijection"}
    result["formal"]=formal_audit()
    if not args.solver_only:
        result["finite"]=weighted_audit(min(args.max_diameter,20)) if args.weighted else finite_audit(args.max_diameter)
        print(json.dumps(result["finite"]),flush=True)
        if args.weighted:
            pair=((0,1,3,3,7,8),(0,2,4,7,7,8))
            result["controls"]=[]
            for exclude,want in [(False,"sat"),(True,"unsat")]:
                check=run_cvc5(model(exclude=exclude,weighted=True,fixed=pair,order_matches=args.order_matches),args.module_dir,15)
                assert check["outputs"]==[want],check
                result["controls"].append(dict(exclude=exclude,**check))
            print("PASS weighted non-vacuity controls",flush=True)
        else:
            result["controls"]=controls(args.module_dir)
            print("PASS six non-vacuity controls",flush=True)
    source=model(weighted=args.weighted,order_matches=args.order_matches)
    (out/"gap-bijection.smt2").write_text(source)
    result["solver"]=run_cvc5(source,args.module_dir,args.timeout,out/"gap-bijection.proof.gz")
    (out/"review.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result["solver"],indent=2),flush=True)
    assert result["solver"]["outputs"]==["unsat"],result["solver"]


if __name__=="__main__": main()
