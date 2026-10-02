# The noncongruent free-projection branch is entirely Bloom

30 September 2026. **[PROVED], computer-assisted, after separate adversarial review**
in `2026-09-30-six-cylinder-branches-review.md`.
Depends on reviewed computer-assisted real/multiset Theorems I and Iw in
`2026-09-30-six-integer-theorem.md`. No novelty claim.

## Theorem BF

Let G be an abelian group and A,B be homometric six-element subsets of G.
Suppose some homomorphism ell:G->R sends A,B to noncongruent real multisets
(counting all six atoms). Then A,B are an image of the classical Bloom pair
in G, allowing independent translations/reflections and interchange:

    X={0,p,q-2p,2q-2p,2q,3q-p},
    Y={0,p,q+2p,2q-p,2q+p,3q-p},       p,q in G.

All six points in each image are distinct because A,B are sets.

In particular, a six-pair in a cyclic cylinder Z x C_q whose integer-height
multisets are noncongruent has only the classical Bloom mechanism. Every
injective cyclic projection of such a pair is an integer shadow. The bound
q<=135 from the bounded-cylinder theorem is unnecessary for this branch:
BF allows every abelian G and every torsion order.

**Contrapositive.** Every non-shadow cyclic six-pair, in every homometric
cylinder lift, must have T/I-equivalent integer-height multisets. After
separate cylinder rigid motions these heights may be made literally equal.
This includes height multiplicities. It reduces the remaining genuinely
cyclic problem to torsion arrangements over a common free configuration;
it does not solve that remaining branch or the finite cyclic seed census.

## 1. Reduce a noncongruent real projection to two forms

Normalize the projected real multisets by their minima, independent
reflections and interchange, as in Iw. Implement those rigid motions in G
by translating by the appropriate actual elements and inverting as needed.
Label each set in weakly increasing projected height, including arbitrary
ordering of atoms with equal heights. The height lists have one of:

    I.1 A=(0,q-2p,q,2q-3p,3q-2p,3q-p)
        B=(0,q-p,q+p,2q+p,3q-2p,3q-p), p>0,q>=3p;

    I.2 A=(0,q-p,q+p,3q-2p,3q-p,2q+p)
        B=(0,p,2q-p,q+2p,3q-p,2q+p), p>0,3p/2<=q<2p.

Here p,q temporarily denote real height parameters. They are not assumed
to lift to G; obtaining group-valued parameters is the content of BF.

Homometry in G provides a bijection of the fifteen unordered edges, with
signs epsilon=+/-1, so matched group differences agree after applying the
sign. To see existence, partition nonzero directed differences into
classes {g,-g}; equal autocorrelations imply equal numbers of unordered
edges in each class, including elements with g=-g. Match within each class
and choose a valid sign. Applying ell gives a signed matching of the real
height differences. Nonzero forward height differences are positive, so
the sign must be +1; for zero height differences both signs are allowed.
Discarding the negative zero signs would miss possible torsion lifts.

## 2. Exhaustive exceptional slopes

For each ordered height list, write each of its fifteen positive-or-zero
forward differences as a coefficient pair (u,v), meaning up+vq. Within
each normal form these fifteen pairs are all distinct, and the A and B
coefficient multisets agree. With t=q/p, two differences can coincide only
at a rational slope

    t=(u'-u)/(v-v'),       v!=v'.

Pairs with v=v' and u!=u' never coincide. Exhausting the 105 unordered
pairs of coefficient forms and retaining slopes in the allowed chamber
(including its admissible endpoint) gives exactly:

    I.1: 3,4,5;
    I.2: 3/2,5/3.

The only point-collision boundaries are t=3 in I.1 and t=3/2 in I.2.
At all other slopes every height difference is distinct. The matching is
therefore the unique formal coefficient matching, independent of how the
numerical distances happen to be ordered. It is enough to examine that
single generic matching in each normal form and every matching at the
five listed slopes. No sampling or bound on real parameters is involved.

At a critical slope, group edges by their exact integer height difference,
using p=denominator(t), q=numerator(t). A bucket of multiplicity k permits
all k! bijections. The zero bucket additionally permits both signs on
each of its edges. These choices exhaust all real-compatible matchings,
including weighted endpoints. Counts are:

| Normal form | Slope | Compatible signed matchings |
| --- | --- | ---: |
| I.1 | generic | 1 |
| I.1 | 3 | 128 |
| I.1 | 4 | 16 |
| I.1 | 5 | 4 |
| I.2 | generic | 1 |
| I.2 | 3/2 | 128 |
| I.2 | 5/3 | 4 |
| **Total** | | **282** |

## 3. Universal group presentations and finite certificates

For each matching make the 15 x 10 integer relation matrix M with rows

    e_j-e_i - epsilon(f_l-f_k),

anchoring e_0=f_0=0. The formal vertex configurations are homometric in
G_M=Z^10/<rows(M)>. The actual group-valued coordinates define a homomorphism
G_M->G, by the signed edge equalities. Thus any identity established in
G_M transfers to the original pair.

The exhaustive certificate file contains every matching's labels and
reduces its relation lattice to one of 21 labelled representatives. Both
lattice inclusions are certified by explicit integer matrices C,C' with

    C*M = M_rep,       C'*M_rep = M.

These equalities can be verified by integer multiplication; no Hermite
normal form implementation must be trusted. Each representative has
integer unimodular U,V and diagonal D satisfying U*M_rep*V=D. Unimodularity
and this matrix identity determine its group presentation exactly. In the
resulting coordinates (torsion coordinates first, then free coordinates),
the old generator e_j has coordinates given by the appropriate row of V.

The resulting finite inventory is:

| Presentations | Group | Vertex distinction | Result |
| ---: | --- | --- | --- |
| 8 | Z^2 | six points each | explicit Bloom identity |
| 3 | Z | six points each | explicit Bloom identity |
| 8 | Z x C_2 | six points each | explicit Bloom identity |
| 2 | Z | repeated formal vertices | cannot map to six-element sets |

For each of the 19 admissible representatives the file exhibits p,q in
G_M, independent translations, the choice of which endpoint is X, and
whether the Y endpoint is inverted. Directly evaluating the twelve
classical coefficient formulas in G_M gives exactly its two six-point
sets. This is an exact identity, not a claim that a capped search found
no alternative. The two inadmissible representatives identify distinct
labelled vertices in G_M, and consequently under every homomorphism; they
cannot be the source of the assumed six-element sets A,B.

Every one of the 282 matchings therefore either forces a forbidden point
collision or gives a Bloom identity. Transfer the identity through G_M->G.
This proves F, subject to the finite certificate audit and Iw.

## 4. The apparent torsion twist is already classical

The only nontrivial torsion invariant among these presentations is C_2,
and it occurs only over the weighted boundary pattern. It initially looks
like an additional cyclic construction. For 2h=0, one representative is

    A={0,g,3g,3g+h,7g,8g+h},
    B={0,2g+h,4g+h,7g,7g+h,8g+h}.

But take classical Bloom parameters p=g+h and q=3g. Reflect Y and X
respectively about 8g+h. The resulting pair is exactly A,B. Thus the
presentation's 2-torsion does not imply a new non-shadow mechanism.
The other labelled C_2 presentations have separate exact certificates in
the file; no unproved equivalence reduction is needed for completeness.

This illustrates why presence of torsion in one matched-distance
presentation is not a proof that the resulting cyclic pair is purely
cyclic. The finite audit closes this entire noncongruent projection branch
with the already-understood signed-factor Bloom mechanism.

## 5. Stronger free-quotient reading

For a finitely generated abelian G, write its free quotient as Z^d. If the
projected vertex multisets in Z^d are not congruent by translation or
inversion, there is a real linear functional whose real projected
multisets are still not congruent. Indeed, a congruence of six projected
atoms uses one of finitely many signs, vertex permutations and translated
anchors. A fixed invalid vector congruence can become true under a linear
functional only on a proper linear subspace of the dual. Finitely many
proper real subspaces cannot cover the dual. Choose a functional outside
all of them.

Applying F then gives a Bloom identity already in G. Hence any six-pair
in a finitely generated presentation that is not a group-valued Bloom
image has congruent multisets in the entire free quotient, not merely for
a specially chosen height projection. This does not eliminate torsion
arrangements above common free heights. Such arrangements can have free
rank three: the separate order-two mechanism supplies examples.

## 6. Reproduction and limits

```bash
.venv/bin/python src/six_bloom_cylinders.py
.venv/bin/python tests/test_six_bloom_cylinders.py
```

Artifacts: `results/2026-09-30-six-bloom-cylinders.json` and its dated log.
The initial 282 Smith decompositions took 0.31 seconds; adding explicit
lattice-inclusion certificates changes runtime modestly. No enumeration
of larger cyclic groups or all cardinalities is needed here.

The important scope is structural: this is a completeness theorem for
one mathematically intrinsic branch, conditional on Iw and the reviewed
finite identities. It does not claim the arbitrary-n six-note problem
solved. Every remaining non-shadow must live over T/I-congruent free
projections, including torsion-only finite cyclic seeds. No novelty claim.
