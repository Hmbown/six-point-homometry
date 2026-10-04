# What the low-rank (LR) checkers verify, stated without the code

Date: 4 October 2026. Author: Hunter Bown, with AI assistance.

Branch LR of Theorem G (free rank $d\in\{1,2\}$, all real projections
congruent) is the one component of the proof that rests on a large saved
computation: 315 height strata, a quotient DAG of 10,602 nodes, and 620
homometric terminals. The proof note
[`notes/2026-09-30-six-free-dag.md`](../notes/2026-09-30-six-free-dag.md)
gives the mathematics. This page states, in prose, exactly which finite
facts the two independent checking programs establish, which facts they
take as input, and which parts of the argument remain prose and are not
checked by any program. A referee can read this page and the proof note
and know what has and has not been machine-verified.

The two programs are
`tests/test_six_free_dag_review.py` (the **cover checker**) and
`tests/test_six_low_rank_mechanisms_review.py` (the **mechanism checker**).
Both are standard-library Python plus two small exact-integer helpers
(`mul`, `det`, `linear`, `autocorrelation`) imported from
`tests/test_six_cylinder_branches_review.py`. Neither imports the builder,
SymPy, or any Smith/Hermite normal-form routine. Every arithmetic step is
exact integer or exact rational arithmetic.

## 0. Setting and notation

Label the two six-point configurations $A=(a_0,\dots,a_5)$ and
$B=(b_0,\dots,b_5)$ with $a_0=b_0=0$. The ten coordinates
$(a_1,\dots,a_5,b_1,\dots,b_5)$ generate $\mathbb Z^{10}$. An **edge** is an
unordered pair $\{i,j\}$, $i<j$; the 15 edges of $A$ and of $B$ are fixed in
lexicographic order. The **edge row** of $(i,j)$ on side $s$ is the integer
vector $e_j-e_i$ in the five coordinates of that side (with $e_0=0$),
embedded in $\mathbb Z^{10}$. A **signed matching row** is
$\text{row}_A(i,j)-\varepsilon\,\text{row}_B(k,l)$ with
$\varepsilon\in\{\pm1\}$.

A **node** is an integer matrix $M$ (rows in $\mathbb Z^{10}$) and the group
$G_M=\mathbb Z^{10}/\text{row}_{\mathbb Z}(M)$. The **universal points** are
the images of the ten generators and zero in $G_M$, giving six points on each
side with coordinates in $\mathbb Z^r\oplus\bigoplus_i C_{d_i}$.

A **stratum** is a rational height vector $h\in\mathbb Z^6$, $h_0=0$, read as
heights of the six points of $A$ (and, after the congruence alignment of
Section 3.3 of the synthesis, of $B$).

## 1. Inputs the checkers take as given

These are **inputs**, not conclusions. Their provenance is a separate
obligation.

1. The list of 315 strata: `results/2026-09-30-six-free-rank/rank3-orbits.json`
   (104 strata) and `rank4-orbits.json` (211 strata), each with its height
   vector $h$. That these are all $S_6$-orbits of rank-3 and rank-4 spans of
   the 120 signed-edge directions, and that each $h$ is generic for its span
   (annihilated by a direction exactly when that direction lies in the span),
   is checked by a **third** program, `tests/test_six_free_rank_growth.py`,
   not by the two checkers described here.
2. For each stratum, a gzipped DAG file `rank{r}-orbit{k}.json.gz` and a
   cross-orbit file `rank{r}-orbit{k}-cross.json.gz` written by the builder.
   The checkers verify their contents; they do not regenerate them.
3. The SHA-256 of each pair of input files is recorded in the per-stratum
   report; a resumed run is only accepted when the hashes match.
4. The mechanism checker additionally takes the builder's exploratory
   mechanism atlas (`results/2026-09-30-six-low-rank-review/exploratory-mechanisms.json`
   and `results/2026-09-30-six-free-mechanisms/atlas.json`) as a list of
   *claimed* certificates to be verified.

## 2. The cover checker: obligations verified per stratum

For each of the 315 strata the cover checker asserts all of the following.
A single failed assertion aborts the run; there is no tolerance.

### 2.1 The nonzero-edge bijection orbits are complete

Let $E_h$ be the list of edges $(i,j)$ with $h_i\neq h_j$, oriented upward
and grouped into **bins** by the value $|h_j-h_i|$. A compatible matching of
nonzero-height edges is a permutation of $E_h$ that preserves bins.

- The checker recomputes $E_h$ and its bin order from $h$ alone and asserts
  it equals the file's edge list.
- It recomputes the group of vertex relabelings that preserve $h$ (all
  permutations within each equal-height fiber, acting independently on the
  $A$ side and the $B$ side) and, for every recorded orbit representative
  $p$, recomputes the full orbit $\{\,b\circ p\circ a\,\}$ under that group.
- It asserts that each recorded orbit size equals the recomputed orbit size,
  that the orbits are pairwise disjoint, and that their union has exactly
  $\prod_{\text{bins}}(\text{bin size})!$ elements, i.e. **every**
  bin-preserving permutation lies in exactly one recorded orbit.
- For each representative it rebuilds the signed matching rows
  (sign $+1$ on upward-oriented edges) and asserts they equal the recorded
  root matrix.

Consequence: every compatible nonzero-edge matching of the stratum is, up to
a relabeling that is a unimodular change of generators, one of the recorded
roots. The totals over all strata are 4,822,240 permutations in 328,473
orbits.

### 2.2 Every node's group data is exactly right

For each node, with matrix $M$ and recorded Smith data $U, V, D$:

- $U$ and $V$ are square integer matrices with determinant $\pm1$ (computed
  exactly by the checker's own `det`).
- $U\,M\,V=D$ with $D$ the recorded diagonal (exact integer products).
- The recorded rank, free rank $10-\text{rank}$, and torsion list (the
  diagonal entries larger than 1) agree with $D$.
- The recorded coordinates of the twelve universal points in
  $\mathbb Z^r\oplus\bigoplus C_{d_i}$ are exactly the appropriate rows of $V$
  reduced modulo the torsion orders.
- Every row of $M$ annihilates the height vector $(h_1,\dots,h_5,h_1,\dots,h_5)$;
  that is, every relation added is consistent with the stratum's real heights.
- The recorded `forced_collision` flag equals "some two points on one side
  coincide in $G_M$", and the recorded `already_homometric` flag equals
  "the two autocorrelation multisets in $G_M$ agree", both recomputed.

### 2.3 Residuals and branching are exhaustive

For each non-terminal node the checker recomputes the two multisets of
unoriented difference classes $\{\pm(x_j-x_i)\}$ in $G_M$, cancels common
multiplicities, and asserts:

- the recomputed residual $A$ classes and residual $B$ classes equal the
  recorded ones, and both are nonempty;
- the recorded chosen $A$ edge lies in a residual $A$ class;
- the recorded branch set equals **exactly** the set of pairs
  (one representative edge of each residual $B$ class, sign $\pm1$) whose
  signed real height equals the chosen edge's real height. Nothing fewer,
  nothing more;
- for each branch, the child's matrix is the parent's matrix plus the
  branch's signed matching row, up to the recorded two-way integer witnesses
  (Section 2.4);
- the child's residual multiplicity is strictly smaller than the parent's
  (this is the termination measure).

Why one representative per residual $B$ class suffices: two $B$ edges in the
same class are already equal up to sign in $G_M$, so matching the chosen $A$
edge to either gives the same quotient; the two signs cover the orientation.

### 2.4 Node identification preserves the integral lattice

Nodes are shared when two different paths produce the same **integer row
lattice**, not merely the same rational row space. For each root and each
branch, the file records two integer matrices $C, C'$ and the checker
asserts

$$C\cdot M_{\text{source}}=H_{\text{child}},\qquad
C'\cdot H_{\text{child}}=M_{\text{source}},$$

by exact integer multiplication. This proves the two row lattices coincide,
so torsion is preserved by cache merging. The total over all strata is
658,894 such identities.

### 2.5 Terminals are what they claim to be

- `collision`: the forced-collision flag is set (two universal points on
  one side coincide; every image collides).
- `ti`: the recorded sign and shift carry the universal $A$ onto the
  universal $B$ in $G_M$ (so every image is translation/inversion related).
- `homometric`: the residuals are empty and both sides have six distinct
  universal points.
- No other terminal kind is accepted.

### 2.6 Reachability and completeness

Every node in the file is reached by the depth-first traversal from the
recorded roots; the file's `complete` flag is set and its `error` is empty;
no stratum hit the node cap. The summary totals are 10,602 nodes,
974 branches, and 620 homometric terminals.

## 3. The mechanism checker: obligations verified per terminal

The 620 homometric terminals are the nodes where the two universal point
multisets are homometric in $G_M$. Each must be shown to be an instance of
the grammar, **in $G_M$ itself**, so that every image in every $\mathbb Z_n$
is an instance too. For each terminal, with group orders
$(d_1,\dots,d_k,0,\dots,0)$, the checker recomputes the autocorrelation of
both universal sets (exact arithmetic in $\mathbb Z^r\oplus\bigoplus C_{d_i}$)
and asserts they agree and that both sets have six distinct points. It then
verifies the claimed certificate by the following **sufficient conditions**,
which are exactly the soundness identities of Section 2 of the synthesis:

- **Bloom.** With $X=\{0,p,q-2p,2q-2p,2q,3q-p\}$ and
  $Y=\{0,p,q+2p,2q-p,2q+p,3q-p\}$ evaluated at the recorded group elements
  $p,q$, the recorded shifts and sign reproduce the two universal sets as
  multisets (which side is $X$ is recorded).
- **Alignment** for all other mechanisms: the recorded sign and shift carry
  universal $B$ to an aligned set $B'$.
- **D (dyad).** With recorded four-point $C$, steps $s,t$, anchor and
  centre $s+t$: $C$ is disjoint from $\{0,s+t\}$ and from $\{s,t\}$;
  $A=C\cup\{0,s+t\}$ and $B'=C\cup\{s,t\}$ after the anchor shift; and
  the kernel $K=C+(s+t-C)+\{0,s,t,s+t\}$ (a multiset of mass 12) satisfies
  $(1-x^s)(1-x^t)K=0$, checked coefficientwise.
- **L2.** With fixed block $U$, moving block $W$ ($U\sqcup W=A$) and shift
  $t$: $x^tP=P$ where $P=UW^*$, and $U\sqcup(W+t)=B'$.
- **L3\*.** $x^{-t}P=P^*$ and $U\sqcup(W+t)=B'$.
- **L4.** $2t=0$, $x^t(P+P^*)=P+P^*$, and $U\sqcup(W+t)=B'$.
- **L5.** $P=x^{-t}\,UW$ (with $UW$ the convolution $u+w$) and
  $U\sqcup(t-W)=B'$.
- **L7 (half-coset).** In the builder atlas: a generator $g$ of order
  $d\in\{2,4,6,12\}$; the union of $H=\langle g\rangle$-cosets through $A$
  has twelve points; each coset meets $A$ in exactly $d/2$ points; and
  $B'$ equals that union minus $A$.

The exact histogram of accepted certificates is asserted:
481 D, 71 L5, 24 L3\*, 20 L4, 14 Bloom, 1 L2, and 9 terminals that have no
direct certificate and are closed by the character cover below.

### 3.1 The nine cyclic-character covers

For a terminal with torsion $\bigoplus_i C_{d_i}$ and exponent
$E=\operatorname{lcm}(d_i)$, the checker enumerates **all**
$\prod d_i$ characters $(j_1,\dots,j_k)$, recomputes the coefficients
$c_i=(E/d_i)j_i$, the image order $q=E/\gcd(E,c_1,\dots,c_k)$, and the
images of the twelve points in $C_q\oplus\mathbb Z^r$ (free coordinates kept).
It asserts the file's quotient records are exactly these, and for each
quotient verifies one of: an explicit collision (two listed indices on one
side coincide), an explicit T/I witness, or a mechanism certificate checked
as in Section 3. The asserted totals are 60 characters: 44 collisions and
16 D certificates (the builder's own atlas certifies the same 16 by L7, and
the checker verifies both).

The mathematical fact that every homomorphism of the torsion part into a
cyclic group factors through one of these characters is proved in prose in
the proof note, Section 5; the checker verifies only that the enumeration is
complete and each quotient's disposition is correct.

### 3.2 Half-coset degeneration controls

Independently of the saved data, the checker enumerates every way the
subgroup $H$ can lose order under a homomorphism (all non-unit multipliers)
and every way occupied cosets can merge (all partitions into blocks of size
at most two, all choices of half-subsets) and asserts the prose lemma's
conclusion in each case: an injective six-point image is globally T/I. This
is a finite confirmation of the lemma repaired during review; the lemma's
proof remains the prose argument.

## 4. What is **not** checked by any program

These remain prose arguments or external trust, and are the right targets
for a human reader.

1. **The coverage lemma** (proof note, Section 3): that any full
   homometric presentation of a stratum factors through some recorded
   terminal. The checker verifies that the recorded branches are *exactly*
   the residual matches with equal real heights; that this is the right
   branching rule is the lemma, proved in prose.
2. **The reduction to strata** (synthesis Section 3.3): the
   finite-union-of-subspaces argument and the claim that the substituted
   rows span exactly rank $5-d$. (A Lean formalization of the
   finite-union step is in `formal/`.)
3. **Completeness of the 120 directions and of the span enumeration**:
   checked by `tests/test_six_free_rank_growth.py`, not by these two programs.
4. **The builder's choice of which residual $A$ edge to branch on** is
   arbitrary; any choice is valid for the lemma. The checker verifies the
   choice lies in the residual, nothing more.
5. **Soundness of the certificate conditions themselves** (that the L2,
   L3\*, L4, L5, L7, D and Bloom conditions imply equal autocorrelation) is
   proved in prose in the synthesis and the component notes; the checker
   also recomputes autocorrelations directly at each terminal, so a wrong
   sufficient condition would be caught at the terminal but the general
   implication is prose. (Lean proofs of L2, L3\*, L4, L5 and L7 are in
   `formal/`.)
6. **The Python runtime and the two small exact-arithmetic helpers.**
7. **Provenance of the input files.** The checkers bind input hashes into
   their reports; they cannot know how the files were produced.

## 5. How to rerun, and what to expect

From the repository root with the pinned environment:

```sh
.venv/bin/python tests/test_six_free_rank_growth.py
.venv/bin/python tests/test_six_free_dag_review.py --out .reproduction/dag-review --require-complete
.venv/bin/python tests/test_six_low_rank_mechanisms_review.py
```

Omit `--resume` for a fresh audit (resumed records skip already-verified
strata). Expected summary: 315 strata, 4,822,240 cross bijections,
328,473 roots, 10,602 nodes, 974 branches, 658,894 lattice inclusions;
620 terminals with the histogram above; 60 characters giving 44 collisions
and 16 constructions. A recorded run with input hashes is in
`docs/STRUCTURAL_REPLAY.json`.
