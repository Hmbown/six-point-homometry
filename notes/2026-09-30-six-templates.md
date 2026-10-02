# Thirteen rigid cyclic six-note templates

30 September 2026. PQ1/P3, cardinality six. **[PROVED], in-house, computer-assisted; no novelty claim.** Separate
adversarial attack: `2026-09-30-six-cylinder-templates-review.md`. This is a rigidity and
partial-generation theorem, not a completeness theorem for all six-note
relations.

## 1. Discovery and exact scope

Starting from the independently checked n=12..60 six-note census, retain
T/I classes and connect each family with the inherited strict edges, the
classical Bloom edges, and all saved parallelogram-dyad edges of Theorem D.
The remaining cross-component pairs fall into exactly the following thirteen
organizational classes under simultaneous unit multiplication and inflation.
Unit multiplication does **not** identify distinct chord classes: the saved
inventory retains all actual endpoints and their transport certificates.

| ID | q | X | Y | Signed matchings | Valid image orders |
|---|---:|---|---|---:|---|
| R1 | 17 | 0,1,2,3,8,12 | 0,1,2,6,7,9 | 192 | 17 |
| R2 | 19 | 0,1,2,3,6,10 | 0,1,2,4,5,11 | 96 | 19 |
| R3 | 21 | 0,1,2,4,7,14 | 0,1,3,7,8,10 | 48 | 21 |
| R4 | 21 | 0,1,2,5,6,15 | 0,1,2,6,7,10 | 48 | 21 |
| R5 | 21 | 0,1,3,7,10,15 | 0,1,4,7,14,16 | 48 | 21 |
| R6 | 23 | 0,1,2,3,7,17 | 0,1,2,4,17,18 | 48 | 23 |
| R7 | 24 | 0,1,2,5,7,16 | 0,1,2,6,9,11 | 16 | 12,24 |
| R8 | 27 | 0,1,2,3,7,19 | 0,1,2,3,8,12 | 12 | 27 |
| R9 | 27 | 0,1,2,6,19,22 | 0,1,3,17,21,22 | 8 | 27 |
| R10 | 28 | 0,1,2,4,12,23 | 0,1,3,5,11,12 | 8 | 14,28 |
| R11 | 30 | 0,1,2,6,19,22 | 0,1,3,9,13,14 | 4 | 15,30 |
| R12 | 30 | 0,1,3,5,12,25 | 0,1,6,9,11,13 | 4 | 15,30 |
| R13 | 31 | 0,1,2,5,11,19 | 0,1,2,6,20,23 | 4 | 31 |

"Valid image orders" means the order of the element t used below, after
requiring both images to have six points and to be T/I distinct. These
finite congruence checks are part of the certificate, not a statement
that all other six-note relations are absent. In particular, proper images
at q=24,28,30 must be allowed; omitting them would give an incorrect
parameter condition.

## 2. The rigidity theorem

For a listed seed (X,Y) in Z_q, match its fifteen unordered edges with equal
cyclic distances, taking either sign when an edge is antipodal. Anchor the
first point of each six-tuple at zero. A matching gives the 15-by-10 matrix
M whose row for (i,j) matched to (k,l) with sign epsilon is

    (e_j-e_i | -epsilon(e_l-e_k)),

with the anchored columns omitted. A solution of Mv=0 in a group is a pair
of labelled six-tuples realizing this exact signed edge matching.

**Theorem R (computer-assisted rigidity).** For every one of the 536
compatible signed edge matchings of the thirteen seeds, the abelian group
presented by M is cyclic of order q. More precisely, the coordinate vector
of the seed is the universal solution: in any abelian group G, every
solution of this matching system has the form

    v = (x_1 t,...,x_5 t, y_1 t,...,y_5 t),    q t = 0.

Consequently the corresponding explicit generator in Z_n is

    X_t = {x t mod n : x in X},
    Y_t = {y t mod n : y in Y},   q t = 0 mod n.

Require the order of t to belong to the last column of the table; then
these are six-note Z-pairs. Add arbitrary separate translations/reflections
when comparing actual chord classes. Every faithful image (order(t)=q)
is purely cyclic, including arbitrarily large ambient moduli n divisible
by q. Every six-note pair realizing any signed matching of a seed is one
of these images: there is no free continuous or integer parameter in that
matching component.

The last sentence is a **pattern-restricted completeness statement**. A
pair with an entirely different signed matching pattern is outside its
hypothesis. The conclusion does not license an exhaustive classification
of six-note pairs by the thirteen rows.

### Proof by exact presentation certificates

For each matching the saved certificate gives integer matrices U,V with

    det(U)=+/-1, det(V)=+/-1,
    U M V = D = diag(1,1,1,1,1,1,1,1,1,q),

where D has five additional zero rows. Let w be the last column of V.
Because these are unimodular changes of generators and relations, solutions
of Mv=0 in any abelian group are exactly v=w s with q s=0. The certificate
also supplies a scalar c satisfying

    gcd(w_0,q)=1,   c w = v_seed (mod q).

Here the first non-anchored X-coordinate of every listed seed is one, so
c*w_0=1 modulo q. Put t=w_0 s. Then q t=0 and
w s = v_seed t: the coefficient difference between w and w_0*v_seed is
coordinatewise a multiple of q. Conversely any v_seed t with q t=0
satisfies the matching equations, since M*v_seed is coordinatewise divisible
by q. This proves the universal solution assertion.

The fifteen matched edges imply equality of the directed difference
multisets of the two images, with multiplicity. The valid-order test checks
all divisors d of q by reduction to Z_d, discards colliding six-tuples, and
uses exact T/I canonical forms. An element of order d identifies Z_d with
its image subgroup. Since both images contain zero, any ambient T/I
equivalence between them must use a translation in that subgroup: a point
of the source is sent to zero, so the translation is its signed negative.
Thus this same test is necessary and sufficient in every Z_n. Separate translations or reflections leave interval content unchanged.

Every seed has been exhaustively checked to have only full-rank matching
matrices. If integer homometric six-set lifts existed, their equality of
fifteen absolute lengths would induce one compatible signed matching and
a nonzero integer kernel vector after anchoring. Full rank rules this out.
This is the exact obstruction argument of Theorem S, including arbitrary
integer coordinates and repeated lengths.

For a faithful image in Z_n, q divides n and t=(n/q)u with gcd(u,q)=1.
If integer homometric lifts reduced to that image, their anchored points
would all be divisible by n/q, since the residues are. Dividing gives an
integer homometric lift of uX,uY modulo q. Multiplying those integer points
by any integer inverse of u modulo q gives an integer homometric lift of
X,Y, contradiction. Thus all faithful images are purely cyclic. Proper
images can acquire extra matchings; their being purely cyclic is **not**
inferred by this argument. QED subject to the finite certificate audit.

The exact presentation is stronger than finding a large nonzero determinant
of a selected minor. For example, the first R2 matching has a chosen
10-by-10 minor of determinant -38, yet its full presentation has Smith
invariant 19. Unimodular identities establish the actual group, not just an
upper bound on its torsion.

## 3. Independent audit and finite coverage

`src/six_templates.py` computes the Smith decompositions. The independent
checks use the previous fresh-context review's edge-by-edge DFS, integer
Bareiss determinants and rational Gaussian elimination; they never invoke
production matching enumeration or SymPy for checking the saved matrices.
All 536 labelled matchings are recovered independently, with no duplicates
or omissions; every U M V identity and both unimodular determinants are
checked exactly. All matrix ranks are ten. The transport code is checked
in 5,870 cases through n=150 against the immutable reference's interval
vectors and T/I canonical forms. These finite tests validate the generator;
the arbitrary-n conclusion follows from the group presentation argument.

The residual inventory contains **186 actual cross-component T/I pairs**
through 60, in thirteen unit/inflation organizational classes. An independent
forward generator tests every t satisfying q*t=0, without using the
production normalization into primitive classes. Independent graph
reachability then verifies that strict + Bloom + D + R connects all saved
six-note families through 60. Residual pair counts by modulus are:

    17:8, 19:9, 21:13, 23:11, 24:4, 27:18, 28:6, 30:8, 31:15,
    34:8, 38:9, 42:13, 46:11, 48:4, 51:8, 54:18, 56:6, 57:9, 60:8.

This coverage statement is relative to the inherited strict/Bloom/D edge
labels. The current independent check reconstructs R edges and graph
connectivity, and the earlier shell review audited all saved D edges;
it does **not** rerun strict-menu discovery. The underlying census itself
was independently checked by two methods through 60. The residual list
has no newly primitive modulus above 31 in that range; this is finite
support for a conjecture, not an arbitrary-n bound.

The first test run had a manually mistyped expected aggregate count 194;
it was corrected to the independently recomputed 186. No data or scope
was changed to fit the test.

## 4. Exact remaining obstruction

A full theorem would need to prove that every six-point signed matching
system admitting a nontrivial binary cyclic realization belongs to one of:

1. An integer-shadow component, with its repeated-distance integer
   classification supplied separately.
2. A component generated by the reviewed strict moves or Theorem D.
3. One of the thirteen finite cyclic presentations above, after the
   allowed relabellings, rigid motions, compositions and homomorphic images.

The present computation visits only matchings of observed residual seeds;
it does not enumerate all 15! edge bijections and all sign assignments.
Nor does it prove a bound of 31 on the torsion of all unvisited components.
The improved universal bound 135 on matching minors from C is insufficient:
it bounds possible torsion primes, but does not classify free components,
noncyclic torsion, realizability, or the mechanisms connecting their images.

R5 is the existing n=21 benchmark. Its known cyclic factor flip and
Z_3 x Z_7 difference-set mechanism are compatible with this result. The
presentation supplies a finite cyclic explanation and rigid realization
condition, while the previous independent integer-shadow rejection remains
in force. This catalog is not claimed to provide thirteen new constructions;
classical seed inflation and homomorphic transport are prior mechanisms,
and a novelty search for each row has not been completed.

## 5. Reproduction

```bash
.venv/bin/python src/six_templates.py
.venv/bin/python tests/test_six_templates.py
```

Outputs are `results/2026-09-30-six-templates/inventory.json`, `smith.json`,
`verification.json` and the dated build/test logs. The generator takes about
one second for the current saved inventory and 536 Smith decompositions;
the independent tests take about 1.2 seconds on this machine. No new
all-cardinality enumeration was run. Source, tests, proofs and outputs are
new files; the immutable reference and inherited jobs remain untouched.
