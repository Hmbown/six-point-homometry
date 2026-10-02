# Adversarial review of the six-note cylinder branches

30 September 2026. Separate fresh-context reviewer from both builders.
No novelty claim. Both complete proof notes have now been read and attacked.

Plan, under the parent's recorded full-six continuation task:
- Independently reconstruct the 120 edge-equality directions, rank-at-most-two flats and permutation orbits; verify generic height specializations introduce no extra equalities.
- Enumerate every compatible signed matching independently, including both signs for zero-height edges; multiply every collision, congruence and lattice certificate using integer arithmetic without Smith computation.
- Verify the four high-free-rank survivors and all noncongruent-projection Bloom presentations as explicit identities in their presented groups; attack all claimed completeness reductions in the written proofs.
- Expected compute: seconds to a few minutes for the saved 14,475 plus 282 presentations; no unbounded search. Read-only builder artifacts; own tests and dated output only.

## Verdict

**Accepted [PROVED], computer-assisted and dependent on reviewed Iw:** the
high-free-rank classification in `notes/2026-09-30-six-free-rank.md` and the
noncongruent-real-projection classification in
`notes/2026-09-30-six-bloom-cylinders.md`, with exactly their stated scopes.
No mathematical defect was found. At review time both notes used the label
Theorem F; the parent was asked to give them distinct labels when integrating.
Here they are called the **high-rank theorem** and **Bloom-projection theorem**.

The first says every nontrivial six-distinct universal signed-edge
presentation of free rank at least three is the displayed antipodal
reflection family in Z^3 direct-sum C2. The second says any homometric
six-subsets in any abelian group with a noncongruent real multiset
projection are already a group-valued classical Bloom pair.

This does not classify T/I-congruent free projections of rank one or two,
or torsion-only configurations. It does not prove an arbitrary-n six-note
classification. The accepted Iw dependency is computer-assisted, with the
exact-solver trust boundary recorded in `2026-09-30-six-integer-review.md`.
This branch review itself uses no SMT, Smith, or Hermite computation.

## 1. Attack on the high-rank completeness reduction

**Finite union of configuration subspaces.** A vector in ker_R(M) gives
two real six-atom multisets with equal directed differences. Coincident
atoms cause no exception: Iw includes them. Zero diameter is congruent and
therefore belongs to the T/I branch. There are finitely many choices of
label permutations, signs and anchors. For each choice the T/I locus is a
linear subspace, and the independently anchored Bloom locus has dimension
at most two. The independent translations are fixed by the selected zero
vertices, so they do not add parameters. A vector space cannot be a finite
union of proper real linear subspaces. Consequently free rank at least
three forces the entire kernel into one fixed T/I alignment subspace.

**Changing anchors does not change the integral problem.** Relabelling,
changing the B anchor, and changing its sign are invertible integral
changes of the anchored generators. A B-edge difference remains a signed
edge difference. Hence one can arrange B_i=A_i on the entire real kernel
without changing the integral relation group or its free rank.

**The height space is actually row-generated.** Once the kernel lies in
the graph B=A, substituting B=A into M gives exactly its A-coordinate
projection, not a larger approximation. The resulting rational relation
space S is spanned by differences of signed edges and has dimension 5-r.
Thus for r>=3 it has a basis consisting of at most two of the listed
directions. This justifies enumerating the spans of pairs; it does not
assume an arbitrary codimension-two space is root-generated. Injectivity
of the A projection also gives r<=5 at this stage.

**All 120 directions occur, including zero-height tests.** Their support
patterns are `(1,-1)`, `(1,1,-2)`, and `(1,1,-1,-1)`. Direct combinatorial
generation gives 15+60+45=120 projective directions. The first pattern
also tests coincident heights: it arises from an edge minus its negative,
whose primitive direction is that edge. Primitive normalization is used
only to identify rational height subspaces. Original integer edge rows
are never divided; the order-two torsion is preserved.

**No missing or duplicated height orbit.** A new rational Gauss-Jordan
checker reconstructs all 4,176 spans independently of the builder's
primitive rank-two elimination. It generates all 720 coordinate
permutations of each saved representative. The 25 resulting orbits are
pairwise disjoint and their union is the complete span set, with every
saved orbit size verified.

**The integer specializations are genuinely generic for the matching
problem.** For each representative and every one of the 120 directions,
the checker verifies `d dot h=0` if and only if adding d leaves the rational
rank unchanged. Therefore the saved specialization neither introduces
nor removes any signed edge equality. No bound on an original real/free
coordinate is inferred from the small selected integers. Every compatible
signed matching is reconstructed by independent edge-by-edge DFS. At a
zero difference the DFS includes both signs. All 14,475 saved matchings
are present exactly once; bucket-factorial counts agree independently.

## 2. Attack on the integral classification and master family

For every collision case the independent checker multiplies the given
integer row witness by the original matching matrix and obtains the
difference of two distinct labels in one tuple. For every T/I case it
checks the sign, anchor, bijection and all six integral row identities.
Every coefficient is required to be an integer, not merely a rational
relation. There are exactly 13,916 collision cases and 555 T/I cases,
giving 17,246 checked discard identities.

The four remaining cases, orbit 20 indices 43,53,107,117, have independently
verified U M V identities and det(U)=det(V)=+/-1 using integer Bareiss
determinants. Their actual diagonals are `(1,1,1,1,1,1,2,0,0,0)`.
No normal-form solver is invoked. Multiplication by the supplied V then
gives exact universal coordinates in C2 direct-sum Z^3. The checker verifies
six distinct vertices on each side, the explicit block-reflection witness,
and the master identity

    C={0,p,q,p-q+h},
    A=C union {r,r+h},
    B=C union {p-r,p-r+h},  2h=0.

It checks h is nonzero and killed by two, and the free coordinate matrix
of p,q,r has determinant +/-1. Thus p,q,r,h generate the full presented
group; the parametrization is not a proper sublattice. Independent
36-term directed-difference counters in C2 direct-sum Z^3 verify the
formal family identity. The written group-ring factorization was also
expanded and checked by hand; its defect factor `(1-H)` annihilates the
dyad factor `(1+H)`.

The n=22 example `{0,1,3,6,13,17}/{0,1,3,8,13,19}` is homometric and T/I
distinct under the immutable reference implementation. It is obtained by
p=3,q=13,r=6,h=11, so it is a real obstruction to the discarded proposed
bound r<=2. The accepted theorem retains this family rather than changing
the definition of the problem.

## 3. Attack on the Bloom-projection branch

**Abelian-group homometry supplies the required signed matching.** Partition
directed differences into classes `{g,-g}`. An ordinary class has two
orientations; an involutory nonzero class has one value with twice the
unordered-edge multiplicity. Equal autocorrelation determines the same
number of unordered edges in either case. Matching each class gives a
signed edge bijection. A group difference may have zero real height while
remaining nonzero torsion; both signs must remain available there, and do.

**Normalizing in the group is legitimate.** The minimum and reflected
anchor heights are heights of actual vertices, so the required translations
can be made by actual group elements. Equal projected heights may be
labelled arbitrarily. Only the real normal-form parameters are initially
assumed; the proof does not assume those parameters already lift to G.

**The five slopes plus generic cases are exhaustive.** Independently form
all fifteen coefficient differences from the two explicit normal forms.
Each coefficient list has fifteen distinct entries and A/B lists agree.
Solving all pair-equality equations and all zero-distance equations yields,
inside the permitted closed chambers, precisely `3,4,5` and `3/2,5/3`.
Away from those slopes, signed equality means identical formal coefficient
vectors. The relative numerical order of different lengths cannot create
additional matchings. Independent DFS recovers exactly 1,128,16,4 and
1,128,4 signed matchings, including every zero sign: 282 in total.

**Every representative really represents its claimed integer lattice.**
For each of the 282 matchings the checker reconstructs M from labels and
multiplies both inclusion matrices, proving both integer row-lattice
inclusions. This verifies 8,460 row identities without trusting HNF.
It checks each representative's U,V unimodularity and exact U M V=D.
As an additional attack, every one of the 210 pairs of representatives
is shown different: an original row from one has a nonzero class in the
other's certified quotient, in at least one direction. Thus the count of
21 labelled integer lattices is independently justified too.

The certified coordinates show two representatives force point collisions.
For all remaining nineteen the checker directly evaluates the twelve
classical Bloom coefficient formulas using the saved group parameters,
translations and signs, and obtains exactly the original universal tuples
as multisets. The group inventory is eight Z^2, three Z, and eight Z x C2.
Every identity survives homomorphism to the actual abelian group. The
special C2 boundary example in the proof also agrees with the proposed
substitution p=g+h, q=3g and separate reflections.

**The free-quotient corollary is valid.** For each candidate rigid alignment
that fails in Z^d, the real functionals making it accidentally true form
a proper linear subspace of the dual. There are finitely many alignments,
so one real functional avoids all of them. Therefore a non-Bloom pair
must be congruent in the whole free quotient, not just under one chosen
projection. This does not classify torsion arrangements over that common
free configuration.

## 4. Reproduction, status and evidence boundary

```bash
.venv/bin/python tests/test_six_cylinder_branches_review.py
```

The reviewer implementation imports neither builder nor SymPy; it uses
independent rational elimination, integer matrix products/determinants,
DFS matching and direct group arithmetic. Its only project import is the
immutable reference `homometry` for the n=22 example. The final run takes
about one second and checks both complete saved branches.

Output: `results/2026-09-30-six-cylinder-branches-review.json`, including
matching/classification totals, all case counts, the four surviving
presentations, 210 lattice distinctions and hashes of every input artifact.
No checksum is treated as mathematical evidence by itself; every substantive
certificate is reconstructed or multiplied by the checker. No checker
failure or mathematical repair occurred during this branch review. The
duplicate theorem label is editorial and was reported before acceptance.

The complete proofs were written before this verdict. Both theorems may be
promoted to **[PROVED], computer-assisted**, with dependency on reviewed Iw
and its stated SMT trust. No novelty or peer-review status is inferred.
The remaining low-free-rank congruent-projection and finite torsion branches
must remain open until separately completed and attacked.
