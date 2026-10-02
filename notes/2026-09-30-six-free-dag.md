# Complete low-free-rank, real-T/I projection branch

Date: 2026-09-30. Status: **[PROVED], computer-assisted**, within Statement
LR's hypotheses. The full mathematical proof and exact certificate package
passed separate adversarial review in
`notes/2026-09-30-six-low-rank-review.md`. The independent structural audit
checks all 315 strata, 4,822,240 cross bijections, 328,473 roots, 974 branches,
and 658,894 integral lattice inclusions. A separate arithmetic checker
verifies every terminal mechanism and cyclic-character quotient. The
halfcoset specialization gap found during review is repaired below.

## Statement LR

Let a signed matching of the fifteen unordered differences of two labelled
six-point sets define its universal abelian presentation
\(G=\mathbb Z^{10}/\langle M\rangle_{\mathbb Z}\), after independently anchoring
the first point of each set at zero. Suppose its real solution space has
positive dimension, and, after a fixed permutation, translation and optional
reflection of the second set, every real solution satisfies \(B=A\) as
labelled point vectors. Suppose also the dimension is at most two.

Then every homomorphism \(G\to\mathbb Z_n\) whose two six-point images are
distinct within each set and are not T/I equivalent is explained by one of:

* the two-parameter Bloom construction;
* periodic block translation (L2);
* cosymmetric block translation (L3*, the direct group-ring version of L3);
* halfturn block translation (L4);
* block reflection with equal cross terms (L5);
* half-per-coset complementation (L7);
* the reviewed parallelogram dyad exchange (D).

The argument is an exhaustive **finite symbolic cover**, with no bound on
the target modulus, the free coordinates, or factor height. It does not
identify target T/I classes under unit multiplication. The branches may
overlap, and some universal terminal presentations have more free parameters
than the original matching; their group-ring identities remain valid for all
those parameters.

The real-T/I hypothesis is obtained elsewhere from the weighted six-point
real theorem Iw and the finite-union-of-linear-subspaces argument. The
complementary real-Bloom projection branch is theorem BF. Rank at least
three in the real-T/I branch is theorem HR. LR does not by itself settle the
finite, rank-zero matching branch.

## 1. Why the finite height arrangement is exhaustive

Write \(A=(0,a_1,\ldots,a_5)\). On the fixed T/I graph, substitute \(B=A\)
in every row of the matching matrix. Each resulting relation is either zero
or the difference of two oriented edges of the complete graph on six
vertices. After dividing out its integer content and ignoring sign, there
are exactly 120 directions, represented in six homogeneous coordinates by
the permutations of

\[
(1,-1,0,0,0,0),\quad(2,-1,-1,0,0,0),\quad
(1,1,-1,-1,0,0).
\]

There are respectively 15, 60, and 45 such projective directions. Let S be
the rational span of the nonzero substituted rows. The full height solution
space is exactly \(S^\perp\) modulo constant translation: no additional
arbitrary real-height relation space is introduced. Thus if the free
dimension is one or two, S has rank four or three.

To enumerate all such spans, extend every lower-rank representative by each
of the 120 directions and quotient by the 720 vertex permutations. Every
span of rank r has a basis of these directions, so by removing its last
basis member it arises from a rank r-1 span; applying a vertex permutation
to that span permutes the direction set. Induction proves completeness.
Independent exterior-coordinate reconstruction gives:

| rank(S) | distinct rational spans | S6 orbits |
|---|---:|---:|
| 3 | 43,770 | 104 |
| 4 | 116,401 | 211 |

For each orbit choose an integer height vector h in \(S^\perp\), with
\(h_0=0\), such that a direction from the 120-direction set annihilates h
if and only if it lies in S. Such an integer vector exists because finitely
many proper rational hyperplanes do not cover a rational vector space.
The saved vector is checked against every direction. Consequently it has
exactly the point and signed-edge coincidences forced by S, including any
repeated heights. This is not a numerical genericity assumption.

Data: `results/2026-09-30-six-free-rank/rank3-orbits.json` and
`rank4-orbits.json`. Independent check:
`tests/test_six_free_rank_growth.py`, output `growth-verification.json`.

## 2. Cross-edge orbit reduction

Orient every edge joining distinct heights upwards. The nonzero projected
differences split into bins by positive height difference. A compatible
matching is precisely one permutation in each bin; an edge cannot match a
different bin or an edge of height zero. Vertex permutations within any
equal-height fiber preserve h. Their independent actions on A and B preserve
the entire completion problem and transport the integer presentation by
relabeling and reanchoring, which are unimodular changes of generators.

We enumerate the product of bin-permutation sets and partition it by the
group generated by adjacent transpositions within every height fiber, on
both source and target. The recorded orbit sizes sum to the full product
of factorials. These are labelled matching symmetries, not an additional
equivalence imposed on actual chord classes.

Across all 315 strata there are **4,822,240** raw nonzero-edge bijections,
in **328,473** orbits. Each orbit representative initializes the integral
lattice L generated by its exact signed edge equalities. No height equation
is added to L merely because it vanishes on h: h is used only to restrict
the subsequent matching choices.

## 3. Exact quotient DAG and its coverage lemma

At a node take \(G_L=\mathbb Z^{10}/L\). Exact Smith data with unimodular
left and right witnesses gives coordinates for the twelve points in
\(\mathbb Z^r\oplus T\). Compute both multisets of fifteen unoriented
difference classes \(\{\pm(x_j-x_i)\}\). Cancel the common multiplicities
of classes already equal in \(G_L\).

If no classes remain, the two universal point multisets are homometric;
the node is a terminal. If two points on one side coincide universally,
every quotient fails the six-distinct-points condition. If the two point
sets are universally T/I, every quotient remains T/I. These are terminal
discards.

Otherwise select any residual A edge. For every residual B class choose
one edge representative and both signs whose exact signed real heights
agree. Add that edge equality to L and recurse. Equal B classes need only
one representative: their equality up to sign is already a relation in L;
the two signs account for its orientation.

**Coverage lemma.** Let a full homometric presentation \(G_0\) of this
height stratum be a quotient of a node. The universally cancelled classes
remain equal in \(G_0\), so cancelling them preserves equality of the two
remaining multisets in \(G_0\). The chosen residual A class therefore
equals some residual B class up to sign in \(G_0\). Its projection to the
chosen real heights agrees exactly, so this choice is among the recorded
branches. The full presentation factors through that child. Induction
gives a path to a surviving homometric terminal unless the realization is
already a discarded collision or T/I pair.

Termination also follows directly: adding a chosen residual equality cancels
at least one additional unsigned edge occurrence. Existing cancellations
remain valid under quotienting, so the residual multiplicity strictly
decreases from at most fifteen. Cache merging does not affect this argument.

This argument reasons inside the original universal presentation, where
the real-height projection is defined. It does **not** assume a map from
the eventual finite cyclic target back to the real line.

To identify duplicate nodes we use the row Hermite lattice, **not** the
rational row span. For each initial root and each parent-plus-branch row,
two integral witness matrices C,C' certify

\[
C\,M_{\rm source}=H_{\rm child},\qquad
C'\,H_{\rm child}=M_{\rm source}.
\]

Thus torsion information is preserved exactly. Verification needs only
integer matrix products, the Smith identities, and unimodularity; it need
not trust the normalization library.

The full saved DAG cover has **10,602** nodes:

| terminal or branch | count |
|---|---:|
| forced T/I | 7,429 |
| forced point collision | 2,207 |
| universally homometric | 620 |
| branching | 346 |

All 315 strata completed without reaching the 10,000-node-per-stratum cap.
Both complete branching lists and two-way normalization certificates are
stored in `results/2026-09-30-six-free-dag-all/`.

## 4. Sufficient identities at homometric terminals

Use the integral group ring of an arbitrary abelian group, involution *,
and write a disjoint partition as A=U+W. Multiplication by a monomial is
translation. Let P=UW*. The saved certificates explicitly align B and give
U and the motion of W; they verify the following sufficient conditions.

* **L2:** for translation by s, \(x^sP=P\). Its involution gives invariance
  of the other cross term, and W's autocorrelation is unchanged.
* **L3*:** for translation by s, \(x^{-s}P=P^*\). The two new cross terms
  exchange the old two. Equivalently \(P=x^sP^*\). This does not require
  solving \(2t=-s\); when such t exists it is the familiar conjugated-swap
  form. The direct identity is valid without that divisibility condition.
* **L4:** \(2s=0\) and \(x^s(P+P^*)=P+P^*\). The complete cross sum is
  unchanged by the halfturn.
* **L5:** for reflection \(W'=x^cW^*\), require \(UW^*=x^{-c}UW\).
  This is equality of the original and new first cross terms; involution
  proves equality of the second terms.
* **L7:** let H be a finite cyclic subgroup, and let every occupied
  H-coset contain \(|H|/2\) points of A. Put \(J=\sum_H x^h\) and let
  S be the union of those cosets. Then B=S-A. The coset-count condition
  gives \(SA^*+AS^*=SS^*\), so \(BB^*=AA^*\). Here S has twelve
  elements and H has order 2,4,6 or12.
* **Bloom:** the displayed six coordinates are exactly
  \(\{0,p,q-2p,2q-2p,2q,3q-p\}\) and
  \(\{0,p,q+2p,2q-p,2q+p,3q-p\}\), up to independent T/I. The known
  polynomial identity holds in every abelian group.
* **D:** after translation and alignment, the pairs have the form
  \(A=C+1+x^{a+b}\), \(B=C+x^a+x^b\), where C has four points and
  the additions are disjoint. Let
  \(R=C+x^{a+b}C^*+(1+x^a)(1+x^b)\). The certificate verifies
  \((1-x^a)(1-x^b)R=0\). The reviewed exact identity
  \(AA^*-BB^*=x^{-a-b}(1-x^a)(1-x^b)R\) proves homometry. In a cyclic
  target, theorem D's periodic-kernel parameterization gives the previously
  reviewed generation mechanism. This is the prescribed parallelogram
  exchange, not an unrestricted spectral-unit existence test.

Each identity transports through any group homomorphism. We retain only
realizations with six distinct points on each side and, for Z-relations,
different T/I classes. The conditions impose no bound on the free parameter
values or on n.

**Specialization of L7.** Transporting its identity needs a small extra
argument to recover the stated move grammar, because previously distinct
occupied H-cosets can merge. Let m=|H| and let k be the kernel size of the
map on H. If k>2, the m/2 points of A in an occupied coset cannot inject into
its image of size m/k. If k=2, both half-coset point sets fill that image,
so the two endpoints agree. Hence a surviving nontrivial six-set pair has
k=1. At most two source cosets can now merge in the target: each contributes
m/2 distinct points of A. If two merge, both A and B fill the resulting
H-coset, which becomes a common fixed full coset. The possibilities are:

* m=2: on each remaining unmerged coset, the one-point complement is the
  same translation by the nonzero element of H. All merged full cosets are
  H-periodic and hence invariant under that translation, so the endpoints
  are globally translation equivalent.
* m=4: there are three occupied source cosets. At most one pair can merge,
  leaving a common full four-coset and complementary two-subsets of one
  other four-coset. Every two-subset of C4 is a translate of its complement
  (adjacent and antipodal pairs are the two cases). The common four-coset
  is invariant under the same translation, so the endpoints are globally
  translation equivalent.
* m=6: there are two occupied cosets; if they merge the endpoints agree.
* m=12: there is one occupied coset and no merger.

Without a merger the image remains literal L7. Thus every non-T/I
six-distinct specialization of the saved L7 templates is literal L7. This
also covers the sixteen L7 certificates after character reduction.

The builder's fixed priority yields the following direct certificates:

| mechanism | count |
|---|---:|
| L4 halfturn | 271 |
| L3* cosymmetric translation | 135 |
| L7 cyclic halfcoset | 114 |
| L5 reflection | 53 |
| L2 periodic translation | 16 |
| Bloom | 14 |
| D dyad | 8 |
| requiring finite-character reduction | 9 |

A separate discovery implementation with different mechanism priority
obtains a different distribution but the same nine unresolved noncyclic
torsion presentations. Discovery agreement is useful but not substituted
for certificate verification.

## 5. Cyclic character reduction closes the nine presentations

Let \(G=\mathbb Z^r\oplus T\), \(T=\bigoplus_i C_{d_i}\), and
\(E=\operatorname{lcm}(d_i)\). Enumerate the \(|T|\) characters
\(\chi:T\to C_E\) given by coefficients
\(c_i=(E/d_i)j_i\), \(0\le j_i<d_i\). Set
\(g=\gcd(E,c_1,\ldots,c_k)\) and \(q=E/g\), and divide the values by g
to view the image as C_q. Retain the free coordinates unchanged.

For any homomorphism \(f:G\to C_n\), the restriction to T has cyclic
image of order q dividing both E and n. Composing it with the canonical
embedding of that cyclic image into the E-th roots of unity produces one
enumerated character, with the same kernel. Thus f factors through the
corresponding \(\mathbb Z^r\oplus C_q\) quotient. The restriction to the
actual image order matters: requiring all of C_E to embed into C_n would
be incorrect when E does not divide n. The free generators remain
arbitrary, independently of the torsion image.

Seven residual presentations have torsion C2 x C2. All four characters of
each force an intra-set point collision. The other two have torsion
C2 x C8. Each has sixteen characters: eight force collisions, and the
other eight have exact cyclic halfcoset certificates. In total the
**60 character quotients give 44 collisions and 16 L7 certificates**, with
no residual template. An independent mechanism search certifies the same
sixteen surviving quotients by D instead.

This exhausts every cyclic realization of every homometric terminal and
completes LR. The independent finite audits of the supplied certificate
package have passed; the separate review logs the logical attacks and the
halfcoset repair.

## Reproduction and evidence boundary

```
.venv/bin/python tests/test_six_free_rank_growth.py
.venv/bin/python src/six_free_dag_batch.py --resume
.venv/bin/python src/six_free_dag_certify.py --resume
.venv/bin/python src/six_free_mechanisms.py --resume
.venv/bin/python tests/test_six_free_mechanisms.py
.venv/bin/python tests/test_six_free_dag_review.py --resume --require-complete
.venv/bin/python tests/test_six_low_rank_mechanisms_review.py
```

The mechanism atlas is
`results/2026-09-30-six-free-mechanisms/atlas.json`; every row identifies its
stratum and terminal node. The normalizations summary is
`results/2026-09-30-six-free-dag-all/normalizations.json`.
Independent coverage and mechanism audit outputs are respectively
`results/2026-09-30-six-free-dag-review/summary.json` and
`results/2026-09-30-six-low-rank-review/verification.json`.

Exploratory failures remain preserved: direct factorial matching workers
were stopped after the quotient cover proved cheaper; a height-only empty
root at the heaviest 1+4+1 stratum reached its node cap. Preseeding with
the complete nonzero-edge orbit cover reduced that same stratum to 248
nodes and completed it. Neither interrupted/capped artifact is used as a
complete certificate. No new construction is claimed novel here.
