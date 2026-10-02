# Complete real and integer six-point line classification

30 September 2026. PQ1/P3. **[PROVED], computer-assisted, in-house, after separate
fresh-context attack in `2026-09-30-six-integer-review.md`. No novelty claimed.**
This completes the line component; it does not classify every cyclic six-pair.

## Theorem I

Let A and B be distinct six-element subsets of the real line, with identical
multisets of their fifteen positive pair distances, and not equivalent by
translation or reflection. After translating and possibly reflecting each
set separately, and possibly interchanging the sets, they have exactly one
of these two ordered forms:

**I.1**, for real p>0 and q>3p:

    A=(0,q-2p,q,2q-3p,3q-2p,3q-p),
    B=(0,q-p,q+p,2q+p,3q-2p,3q-p).

**I.2**, for real p>0 and 3p/2<q<2p:

    A=(0,q-p,q+p,3q-2p,3q-p,2q+p),
    B=(0,p,2q-p,q+2p,3q-p,2q+p).

Every displayed admissible pair is homometric and noncongruent. Repeated
pair distances are allowed throughout. For integer sets, p and q are
integers. Thus all integer six-point homometry is the classical two-parameter
Bloom mechanism, including the repeated-distance cases. These normal forms
are order chambers of that mechanism, not claims of a new construction.

## 1. Soundness and noncongruence without a solver

Treat each entry as its integer coefficient vector of (p,q). The multiset
of fifteen formal differences A_j-A_i, i<j, is identical to the analogous
multiset for B in each form. This is a finite polynomial identity in the
free abelian group on p,q; the regression test checks the coefficient
multisets exactly. The stated parameter inequalities make each list strictly
increasing, so these formal positive differences prove homometry for real
parameters as well as integers.

For I.1 the consecutive gaps of A are

    (q-2p,2p,q-3p,q+p,p),

and those of B are

    (q-p,2p,q,q-3p,p).

The first gaps differ, so the normalized sets are unequal. A reflected A
starts with gap p, whereas B starts with q-p>2p, so reflection is impossible.

For I.2 the A gaps are

    (q-p,2p,2q-3p,p,2p-q),

and the B gaps are

    (p,2q-2p,3p-q,2q-3p,2p-q).

The first gaps differ because q<2p. A reflected A starts with 2p-q<p,
whereas B starts with p, so reflection is impossible.

The strict normal forms are also unique under the stated normalization.
In both forms the first gap is strictly larger than the last gap, so the
orientation chosen in section 2 is unique for each set. Lexicographic order
fixes the interchange of A and B. After diameter one, I.1 has
1/3<a2<3/8, whereas I.2 has 3/5<a2<5/8; hence the two forms do not overlap.
The recovery formulas below determine p,q uniquely. This uniqueness is
not asserted at the repeated-coordinate boundaries of section 6.

Integer integrality is immediate from the displayed points: in I.1,
p=A_5-A_4 and q=A_2; in I.2, p=A_4-A_3 and q=A_1+p. Hence normalizing
integer sets by rigid motions gives integer parameters. No denominator or
coordinate bound is hidden in this claim.

## 2. Exhaustive normalization

Any six-element real set has positive diameter L. Homometric sets have the
same diameter, since it is the largest positive distance. Translate both
minima to zero, and divide every coordinate by L. Write their increasing
lists as (0,a1,a2,a3,a4,1) and (0,b1,b2,b3,b4,1).

After removing one copy of the diameter 1 from the common distance multiset,
the largest remaining distance is r=max(a4,1-a1): every distance other than
1 is at most one of those two endpoint distances. Reflect A about 1/2 if
necessary so a4=r. Independently do this for B, giving b4=r. This remains
valid when the two candidates tie and when other distances repeat. Thus
both sets have the form

    A=(0,a1,a2,a3,r,1), B=(0,b1,b2,b3,r,1),

with strict ordering and r>=1-a1, r>=1-b1.

The sets are unequal, so swapping them if necessary imposes the strict
lexicographic condition (a1,a2,a3)<(b1,b2,b3). Reflection congruence is
excluded by not(A_i=1-B_(5-i) for every i). These are all linear real
constraints, with no restriction of the coordinate domain to rational,
integer, or bounded-denominator points.

## 3. Exact finite statement checked by the solver

For each of the fifteen A distances d, assert

    sum_(e in distances(A)) [e=d]
      = sum_(f in distances(B)) [f=d].

Here every edge occurs separately, and [P] is the SMT expression
`(ite P 1 0)`. These equations are equivalent to multiset equality:
for each distinct A distance the multiplicities agree, and their total is
15 on both sides, so B cannot contain any additional distance value.
This expressly retains repeated distances.

Exclude both I.1 and I.2 as linear parameter planes. For a template whose
ten nonzero coordinates have coefficient rows (u_i,v_i), choose two rows
(i,j) of nonzero determinant delta. If the actual coordinate vector is z,
its membership in the plane is exactly the ten equations

    delta*z_k = (u_k*v_j-v_k*u_j)*z_i
                  + (-u_k*v_i+v_k*u_i)*z_j.

This is Cramer's rule, so no existential or universal quantifier is hidden.
Repeated occurrences of r and the two diameter coordinates 1 are substituted
literally. The strict ordered-domain constraints automatically force the
parameter inequalities displayed in I.1 and I.2 (read their consecutive gaps).

The resulting **quantifier-free linear real arithmetic formula is UNSAT**
in the saved Z3 and independent cvc5 runs. Therefore every normalized
homometric pair belongs to one of the two stated planes. Undoing the scale
and rigid motions proves completeness, conditional on the exact solver
certificates and the audited correctness of this encoding.

The unbounded real domain is the reason this is a completeness argument,
not an extrapolation from an integer diameter census. There are seven real
variables; the finite formula encodes all possibilities at once.

## 4. Relation to the classical Bloom family

The inherited explicit mechanism is

    X=(0,p,q-2p,2q-2p,2q,3q-p),
    Y=(0,p,q+2p,2q-p,2q+p,3q-p).

Its signed-factor identity is proved in the preceding shadow theorem.
More directly, I.1 is the pair `(3q-p)-Y, (3q-p)-X`; I.2 is
`(3q-p)-X, Y`. Sorting each resulting set gives the displayed lists in
its parameter chamber. These explicit integer rigid motions establish
that the two normal forms use the same integer p,q as the classical
mechanism; no rational change of parameters is required.
To obtain all its real ordered chambers, take p>0 (simultaneous reflection
absorbs p<0); p=0 gives collisions and is inadmissible. Sort each list as
q/p ranges between the exact collision slopes

    -2,-1,-1/2,0,1/3,1/2,2/3,1,3/2,2,3.

There are no unlisted order changes, since every crossing is an equality
between two coefficient forms. Normalize each sorted list by its minimum,
include separate reflections and interchange A/B. The generated 96 order
templates describe 16 distinct two-dimensional linear planes. Only two
planes meet the normalization in section 2; they are I.1 and I.2.
This chamber calculation is ancillary: the final completeness formula
excludes just the two explicitly written forms, and their soundness is
checked directly. It does not rely on a claim that a sampled chamber list
is exhaustive.

**Corollary [PROVED], with the same exact-solver qualification.** A
six-note cyclic Z-pair is an integer shadow if and only if it is a T/I
image of an admissible modular Bloom pair. For the forward implication,
apply I to its integer lifts and use the explicit rigid motions above;
reduce the integer p,q modulo n. For the reverse implication choose any
integer lifts of the modular parameters: distinct residues guarantee
six distinct integer terms, and the formal Bloom identity gives integer
homometry. Thus testing all n^2 residue parameter pairs is an exact
shadow decision, with no search bound on lifted coordinates.

For the integer-shadow part of the cyclic program, Theorem I combined with
Theorem C1 implies every six-pair in Z_n with all prime divisors greater
than 131 is generated by the Bloom formula modulo n. It also makes
absence from the complete modular Bloom image an exact non-shadow test.
This does not establish the complete list of purely cyclic mechanisms.

## 5. Evidence, controls, and reproducibility

Code: `src/six_integer_smt.py`. Tests: `tests/test_six_integer_smt.py`.
The initial 96-template count encoding returned UNSAT in 1.58 seconds.
Z3 with proof output returned UNSAT in 1.34 seconds; the compressed exact
proof is about 504 KiB. cvc5 1.4.1 independently returned UNSAT in 4.76
seconds with `produce-proofs` and `check-proofs` enabled. The separate
sorting-network encoding timed out at 60 seconds and returned `unknown`;
this is a failed bounded solver approach, not mathematical evidence.
The final two-plane runs have separate dated outputs.

Non-vacuity controls check that the normalized homometry formula is SAT
without the exclusion; both the collision-free diameter-17 example and the
repeated-distance diameter-11 example are SAT before and UNSAT after their
family is excluded. The domain outside both planes is SAT when homometry
constraints are removed. A fixed nonhomometric pair is rejected. Formal
multiset identities and integer examples are checked independently of SMT.

```bash
.venv/bin/python tests/test_six_integer_smt.py
.venv/bin/python src/six_integer_smt.py --proof --out results/2026-09-30-six-integer-two-plane
# Optional independent solver; isolated install leaves project packages alone:
.venv/bin/python -m pip install --target /tmp/babbitt-six-cvc5 cvc5==1.4.1
.venv/bin/python src/six_integer_cvc5.py --module-dir /tmp/babbitt-six-cvc5 --input results/2026-09-30-six-integer-two-plane/count.smt2 --out results/2026-09-30-six-integer-two-plane/cvc5.json
```

No Lean toolchain is installed. This is a computer-assisted completeness
proof, with explicit exact-solver trust. The separate fresh-context review
checked the mathematical encoding and used a different gap/bijection
formula with eagerly checked cvc5 proofs. Two agreeing solvers alone would
not verify a mistaken encoding.
No novelty claim is made. Literature so far verified the classical formula
and collision-free completeness statements; that does not by itself verify
an earlier repeated-distance completeness theorem. The previous logged
required-venue search and its access gaps remain in force.

## 6. Weighted extension: six atoms with repetitions

**Theorem Iw [PROVED] (same computer-assisted qualification).** Let A,B
be real multisets of total multiplicity six, homometric and not congruent
by translation or reflection. Then their diameter is positive and they
have one of the same two forms, with the relaxed conditions

    I.1: p>0, q>=3p;
    I.2: p>0, 3p/2<=q<2p.

The integer-parameter conclusion remains valid. In particular the only
noncongruent case with fewer than six support positions is, up to rigid
motions and common scaling,

    {0,1,3,3,7,8} / {0,2,4,7,7,8}.

Each multiset here has five support positions, with one double atom. No
noncongruent six-atom homometric multiset has four or fewer support
positions. This statement does not assert that equal projected multisets
are the same configuration before projection from a cylinder or group.

**Proof modification.** Label all six atoms, including repeated locations,
in weak increasing order. Positive diameter permits exactly the same
normalization. After removing one occurrence of the maximum distance,
the largest remaining distance is still max(a4,1-a1), possibly equal to
one. Thus both rightmost interior atom coordinates can again be set to
the common value r by separate reflections. The 15 pair distances now
include a zero for every unordered pair of coincident atoms. Equality of
these multiplicities is exactly multiset homometry (diagonal self-pairs
contribute six additional zeros on both sides of directed autocorrelation).
The same count encoding therefore works, with just the ten strict adjacent
coordinate inequalities replaced by weak ones.

The exact weak-domain formula, with the same two planes excluded, is UNSAT
in the saved run. Plane membership and weak ordered gaps imply p>=0 and
the closed chamber inequalities. In I.1, p=0 makes A=B; diameter positivity
rules out the all-zero parameters. Hence p>0. In I.2, p=0 is incompatible
with positive diameter, and q=2p makes A=B, so that upper endpoint is
excluded by noncongruence. The first/reflected-gap noncongruence arguments
in section 1 remain strict at the allowed lower endpoints. Formal distance
identities remain identities even when a distance becomes zero.

For I.1 the only vanishing consecutive gap is q-3p at q=3p; all other gaps
are strictly positive. At p=1 this gives the displayed weighted pair.
For I.2 the only vanishing consecutive gap is 2q-3p at q=3p/2. At p=2,q=3
this gives {0,1,5,5,7,8}/{0,2,4,7,7,8}; reflecting the first multiset about
4 gives the displayed pair. Consequently the two boundary descriptions
are the same up to allowed rigid motions, and there are no further
support-collision cases. A zero-diameter multiset is six copies of one
point and has only congruent partners, so it was safely excluded.

Reproduce the separate weak-domain certificate without changing the
strict-domain artifacts:

```bash
.venv/bin/python src/six_integer_weighted.py --two --proof --out results/2026-09-30-six-integer-weighted-two
.venv/bin/python tests/test_six_integer_weighted.py
```

The separate fresh-context review also accepts this extension, using an
independent weighted gap/bijection encoding. See its full attack and the
saved exact proofs; the noncongruent-projection restriction is essential.
