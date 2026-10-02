# Two-height six-note fibers reduce to block moves and dyad exchange

30 September 2026. **[PROVED], computer-assisted, after separate adversarial
review in `2026-09-30-six-fibers-review.md`.** No novelty claim. This is a structural completeness result for a
specified branch of the six-note problem, not arbitrary-n completeness.

## 1. Claim and scope

**Theorem TF.** Let A and B be six-element subsets of a finitely generated
abelian group G, with equal ordered-difference multisets. Suppose a real
homomorphism sends their six atoms, including multiplicities, to the same
multiset supported on exactly two heights. Let f:G->Z_n be any homomorphism
whose images each have six distinct points. Then f(A),f(B) are congruent,
or, after independent translation/reflection and a possible swap, are
related by one of the explicit moves D, L2, L3*, L4, L5 below.

The two-height hypothesis is on a lift, not on a homomorphism from a finite
cyclic group to R. It applies to the common-free-height cylinder branch of
the bounded-cylinder reduction. The real height gap is arbitrary and need
not be normalized integrally. The theorem covers both oriented profiles
(r,6-r), since reflecting both pairs exchanges the heights.

The common profile (5,1) is congruent already in G. Profiles (4,2),(3,3)
are resolved by exact finite universal-presentation certificates. The
finite computation is independent of n, heights, and torsion order. Its
118 terminal presentations collapse to five named identities; the
presentations are proof intermediates, not 118 additional mechanisms.
No unit multiplication is used to identify chord classes.

## 2. The five identities

Write set polynomials in Z[G], with x^g x^h=x^(g+h), and P* for inversion
of exponents. All displayed unions must be disjoint and have six points.
These conditions are preserved in any specialization retaining six
points on each side. Independent translations, reflections, and swapping
the pair preserve homometry.

**D, parallelogram dyad exchange.** For a four-set C and a,b in G, put

    A=C union {0,a+b},    B=C union {a,b},
    W=C+x^(a+b) C*+(1+x^a)(1+x^b).

Require (1-x^a)(1-x^b)W=0. Then

    AA*-BB*=x^(-a-b)(1-x^a)(1-x^b)W=0.

This is the reviewed mixed-periodic dyad condition from the six-shadow
note. In a finite cyclic group its nonnegative periodic-weight
parametrization gives the equivalent constructive grammar in that note.
Thus the D conditions are more specific than an unrestricted spectral
unit or a test of the two full autocorrelations.

For the block moves write A=U union V, P=UV*, and retain U.

**L2, periodic block translation.** Replace V by x^t V when x^t P=P.
The cross terms change from P+P* to x^(-t)P+x^t P*, which is the same.

**L3*, generalized cosymmetric block translation.** Replace V by x^t V when
P=x^t P*. The first new cross term is x^(-t)P=P*, and the second is P. This version states the
cosymmetric cross-distribution identity without requiring division of t
by two in G; it includes the usual co-symmetric block swap.

**L4, order-two block translation.** Replace V by x^t V when 2t=0 and
x^t(P+P*)=P+P*. The combined cross distribution is unchanged.

**L5, block reflection.** Replace V by x^t V* when
UV*=x^(-t)UV. The first cross term is unchanged, hence so is its inverse;
the within-block autocorrelation of V is invariant under reflection.

These conditions are sufficient group-ring identities, valid before any
cyclic specialization. Certificates provide U,V,t or C,a,b explicitly.

## 3. The singleton profile

For profile (5,1), independently translate the singleton upper fibers to
the identity. The positive-height component of the autocorrelation is
then exactly the inverse polynomial of the lower fiber. Equality forces
the two lower fibers to agree. Restoring translations proves congruence.
This argument also works for any cardinality with a singleton extreme
fiber and only two heights.

## 4. Cross-height orbit reduction

Label lower vertices 0,...,r-1 and upper vertices r,...,5; independently
anchor A_0=B_0=0. Equality of the positive-height difference multisets
supplies a bijection of the r(6-r) cross edges, with no sign ambiguity.
For its permutation p, impose the integer relations

    A_j-A_i = B_l-B_k,

where p matches lower-upper edge (i,j) with (k,l). The ten remaining
vertex symbols freely generate Z^10 before imposing these relations.
The actual pair is an image of this universal presented abelian group.

Within each side, permutations of lower labels and of upper labels only
change notation. Their adjacent transpositions generate
S_r x S_(6-r). The implementation enumerates the double orbits of cross
bijections under independent source and target actions. Breadth-first
closure applies every generating action to every reached permutation.
The saved orbit sizes sum to the total factorial, with no overlap.

The exact output is:

| profile | raw cross bijections | double orbits |
|---|---:|---:|
| (4,2) | 40,320 | 52 |
| (3,3) | 362,880 | 322 |

This is relabelling of vertices, not an affine or unit equivalence of
chord classes. It is valid with repeated cross differences because any
occurrence bijection is allowed.

## 5. Quotient cancellation is a complete branching rule

After cross relations have been imposed, only the zero-height component
remains. It is the sum of the internal unordered edges of both fibers,
with each edge contributing its difference and its negative. For a group
element d denote its unsigned class by [d]={d,-d}. Equality of the
ordered component is equivalent to equality of the multisets of these
unsigned classes. This remains true for d=0 and elements of order two:
each edge contributes twice to such a singleton class on each side.

At a current universal group, cancel identical unsigned classes from
the two internal-edge multisets, with multiplicities. These equalities
survive under every further homomorphism. If no classes remain, the
universal pair is homometric. Otherwise choose one remaining A edge e.
For every distinct remaining B class choose a representative edge f and
make two branches, imposing e=f or e=-f. These branches cover every
homometric image: after subtracting already-common contributions, the
image of e must equal one of the remaining B classes. Choosing just one
representative per class loses nothing; all representatives are already
equal up to sign in the current group.

The child universal group is the quotient by the selected relation.
At least one additional pair of unsigned occurrences cancels there, so
along any path the residual edge count strictly decreases. There are
initially 7 internal edges for (4,2) and 6 for (3,3). Thus the recursion
terminates even without caching. Equal integer row lattices are cached.

A node may be discarded if two vertices on one side coincide in its
universal group, because every homomorphism retains that collision. It
may also stop at universal T/I congruence, inherited by every image. All
other zero-residual nodes are retained as homometric templates.

The complete certificate counts are:

| profile | nodes | homometric leaves | T/I leaves | collision leaves | branch nodes |
|---|---:|---:|---:|---:|---:|
| (4,2) | 258 | 51 | 23 | 95 | 89 |
| (3,3) | 381 | 67 | 44 | 197 | 73 |

For every node the files contain integer matrices U,V,D with UMV=D,
U,V unimodular. The quotient coordinates of each vertex are rows of V,
retaining nonunit torsion coordinates modulo their diagonal entries and
all free coordinates. Each root and branch includes **both** integer
row-lattice inclusion witnesses, checked by direct multiplication. Thus
canonicalization can be audited without trusting a normal-form routine.
Saved residual classes and all signed branches permit independent checks
of the exhaustive branching rule. No finite modulus scan occurs here.

## 6. Structural reduction and cyclic torsion characters

The certificates recognize the following identities directly in each
universal group:

| profile | D | L2 | L3* | L4 | L5 | remaining |
|---|---:|---:|---:|---:|---:|---:|
| (4,2) | 32 | 1 | 0 | 4 | 11 | 3 |
| (3,3) | 49 | 0 | 10 | 0 | 8 | 0 |

Each row includes its independent B-alignment and the indicated move
parameters. These are verified by exact group-ring arithmetic, not by
sampling parameter values.

It remains to cover cyclic images of three (4,2) groups. For a finitely
generated abelian group H=Z^d direct-sum T, any homomorphism H->Z_n
restricts on T to a finite cyclic image. Embed that image in Q/Z. If
T=direct-sum_i C_(d_i), every such character is represented by

    chi_k(t_1,...,t_m)=sum_i k_i t_i/d_i mod 1,
    0<=k_i<d_i.

Consequently it suffices to inspect exactly product_i d_i characters,
retaining the free coordinates independently. Each actual cyclic map
factors through one of these quotients Z^d direct-sum chi_k(T), followed
by a homomorphism into Z_n. A collision already forced in a character
quotient invalidates every specialization through it.

The three exceptional nodes are fully handled as follows:

| (4,2) node | universal group | all characters | forced collision | D |
|---|---|---:|---:|---:|
| 71 | Z direct-sum C2 direct-sum C8 | 16 | 8 | 8 |
| 76 | Z direct-sum C2 direct-sum C8 | 16 | 8 | 8 |
| 185 | Z^2 direct-sum C2 direct-sum C2 | 4 | 4 | 0 |

For every collision the file gives the side and coincident vertex
indices. For every surviving quotient it gives the exact D identity.
No order bound on Z_n is introduced by this finite character argument.
Together with Sections 3--5 and the direct move certificates this proves
Theorem TF, conditional only on the finite certificate verification.

## 7. Reproduction, limits, and provenance

Run with the pinned environment:

```
.venv/bin/python src/six_fibers.py --profile 4,2 --quotients
.venv/bin/python src/six_fibers.py --profile 3,3 --quotients
.venv/bin/python src/six_fibers_certify.py
.venv/bin/python src/six_fibers_mechanisms.py --cyclic
.venv/bin/python tests/test_six_fibers.py
```

Exact outputs are in `results/2026-09-30-six-fibers/`. The cross-orbit
passes take about 0.2 and 1.4 seconds; quotient DAG construction takes
about 0.2 and 0.3 seconds. Attaching all integer inclusion witnesses
takes about 5 seconds. Mechanism recognition takes under one second.
These timings are local observations, not complexity claims.

This result does not classify common-height projections with three or
more heights, or the finite torsion-only branch. It does not establish
that a particular cyclic output is purely cyclic: Bloom membership is
still the exact integer-shadow decision. It shows that the entire
two-height branch adds no move beyond the displayed block identities
and parallelogram dyad exchange. The result concerns all cyclic images,
including inflation and additional quotient identifications preserving
six points. No novelty claim is made for either the identities or this
branch organization. Source code and proof certificates are new files;
the immutable reference and data are unchanged.
