# Separate adversarial review of the cylinder reduction and rigid templates

30 September 2026. Reviewer: root agent, separately from the two builder
agents. This is an in-house mathematical attack, not external peer review.
Reviewed `2026-09-30-six-completeness.md` and `2026-09-30-six-templates.md`
in full, together with their source and independent arithmetic tests.

## Attacks on C, C1, C2 and E

1. **Does the presentation lift a set, or only a weighted configuration?**
   All matched edges give equality of directed difference multisets in the
   presented group, including zero and involutory differences. The map to
   the original cyclic group is injective on each six-tuple, so neither the
   universal configuration nor its intermediate cylinder image can collide.
   Independent anchor translations do not change homometry. No gap found.
2. **Can compression of several free directions lose needed information?**
   The chosen integer linear functional is dictated by arbitrary integer
   lifts of the original residue images. Its composition with the cylinder
   projection is the original map. That identity, rather than a genericity
   assumption, proves distinctness and T/I distinction. The torsion image,
   rather than the entire possibly noncyclic torsion group, is cyclic. This
   distinction is essential and is correctly made.
3. **Is 135 a determinant bound or an unsupported observed Smith bound?**
   For rank at most nine, expansion along the incidence blocks gives 126.
   For rank ten, the first-block nonzero cofactors are exactly the spanning
   trees of the selected ten-edge graph. Ignoring signs only enlarges the
   bound. The two exhaustive calculations use every labelled graph, with
   no unverified isomorphism reduction. Both sum to 3,003 and give maximum
   135. The gcd of maximal minors bounds the torsion order, hence its cyclic
   image order. C1 correctly uses the largest prime at most 135, namely 131;
   it does not claim 131 is sharp. C2 requires a full-rank matching.
4. **Does a nontrivial cylinder certificate prove non-shadow status?**
   No. Another matching could have a trivial-torsion lift. The theorem
   explicitly withholds that inference and does not classify the cylinders.
5. **Energy identity and antipodal multiplicities.** The cross-correlation
   second moment is the inner product of the two autocorrelations. Their
   equality gives the stated identity. If intersections are at most two,
   the second moment is at most 72. An ordinary double interval adds four
   to the baseline 66; one antipodal pair adds two, two add twelve. The
   necessary low-collision regime is correct. The universal three-common-
   note conjecture remains open; the finite histogram does not prove it.

## Attacks on R

6. **Do the certificates present the whole group?** Checked that every
   stored U and V is square unimodular and U M V has the claimed Smith
   diagonal, not merely one nonzero selected minor. Independent DFS
   reconstructs all 536 compatible signed matchings, including antipodal
   signs. Exact integer matrix multiplication and Bareiss determinants
   independently verify the presentation certificates.
7. **Does the seed generate all group-valued solutions?** The first
   non-anchored X coordinate is one. The checked scalar relation therefore
   makes the corresponding entry of the final V column a unit modulo q.
   Changing the torsion parameter by this unit proves the universal solution
   is exactly the seed times an element killed by q. This works in arbitrary
   abelian target groups, not only fields or cyclic groups.
8. **Can embedding create an ambient T/I equivalence missed in Z_d?** Both
   images contain zero. A rigid equivalence sending a source point to zero
   forces its translation into the image subgroup. Thus checking in Z_d is
   necessary and sufficient. Proper images at orders 12,14,15 cannot be
   omitted. The table includes them and does not assert their non-shadow
   status using only faithful-image arguments.
9. **Does faithful inflation preserve the no-integer-lift obstruction?**
   Anchor a hypothetical lift at the point mapping to zero. All lifted
   coordinates are divisible by n/q. Divide and multiply by an integer
   inverse of the unit parameter modulo q. This would give an integer
   homometric lift of the original seed, contradicting full rank of every
   compatible matching. Signs, independent anchors and arbitrarily large
   integer coordinates do not evade this argument.
10. **Does observed residual coverage prove completeness?** No. The 186
    edges are relative to inherited strict/Bloom/D discovery. R's independent
    graph check validates R edges and that conditional finite coverage,
    not completeness of the older search or an arbitrary-n catalog. The
    proof states this boundary. Unit multiplication organizes generators
    and never merges the actual T/I endpoints.

## Rerun and disposition

The root reviewer reran, with the pinned environment:

```bash
.venv/bin/python tests/test_six_completeness.py
.venv/bin/python tests/test_six_templates.py
```

Both pass. C's checks take 2.38 seconds and R's approximately 1.2 seconds.
They check the 3,003-graph bound, exact cylinder projections and inflated /
independently translated cases, all 32,106 census pair intersections, all
536 presentation identities, 5,870 transports through n=150 and all 186
conditional residual edges. The census itself remains independently checked
only through n=60; testing transports through 150 does not extend it.

**Accepted [PROVED], computer-assisted where stated:** C, C1, C2, E and R
with precisely the scopes above. No mathematical repair was needed.
The older 252/251 bounds are superseded by the sufficient 135/131 bounds.
**Not accepted as a claim:** a complete cyclic six-note classification,
sharp torsion bound, or novelty. The finite catalog and bounded-cylinder
reduction are further partial progress. Positive-free-rank cylinder
classification and a complete finite torsion catalog remain unfinished.
