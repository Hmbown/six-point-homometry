# Six-point foundations exposition audit

30 September 2026. **[COMPUTED]** source and arithmetic audit for the expanded
LaTeX fragment `2026-09-30-six-formal-foundations.tex`. This is a component
draft for integration and a fresh whole-manuscript attack; it is not a new
novelty claim or a full proof-assistant verification.

## Scope and source reading

The fragment expands universal signed occurrence matching, its exact integral
presentation and rank, torsion bounds, finite unions of linear subspaces,
free-quotient alignment, weighted Iw's mathematical interface, BF and HR.
It proves the independent review's proposed direct HR-to-L3* identity.
It preserves the full Iw exact-UNSAT dependency and gives explicit acceptance
predicates plus exhaustiveness arguments for each finite structural step.

The session read README, RESEARCH_PROGRAM, PROGRESS, CONJECTURES and LITERATURE
in order; the root had already run and passed the pinned baseline tests and
recorded the session plan. The mathematical source reading used the dated
six-point paper, generation, integer-theorem, bloom-cylinders, free-rank and
completeness notes, the integer proof attack, the independent Claude review,
and the actual BF/HR builders and arithmetic checker. No protected source,
baseline test driver, data, inherited output, paper or ledger was edited.

## Read-only verification performed

The checker `tests/test_six_cylinder_branches_review.py` was loaded by path in
the pinned Python environment. Its `orbit_audit` and `bloom_audit` functions
were called directly on their saved packages; the main function, which writes
an output, was not called. Both audits pass:

| Component | Replayed obligations |
| --- | --- |
| HR | 120 directions, all 4,176 flats in 25 orbits, all 14,475 signed matchings |
| HR discards | 13,916 collisions, 555 rigid equivalences, 17,246 row identities |
| HR survivors | Four certified C2 direct-sum Z3 decompositions and full master identifications |
| BF | All seven cases, 282 matchings, 21 labelled integral lattices |
| BF arithmetic | 8,460 two-way row identities, all diagonals and 19 explicit Bloom identities |
| BF collisions | Two exact representative collisions |

The arithmetic replay took under one second. A separate short calculation,
with the displayed coefficient lists written independently rather than
importing builder formulas, checked equal formal distance multisets, all
exceptional slopes and the counts 1/128/16/4 and 1/128/4. This uses exact
fractions and bin-factorial counts, not sampled heights.

No solver, large census or new full torsion enumeration was run. The 135
torsion bound is expanded from its existing two-method checked histogram,
with a proof by incidence determinants and Cauchy--Binet of the independent
Laplacian interpretation. The lemma retains its exact finite obligation.

## Direct HR simplification

Let D be the moving dyad, E=C D*, and s=p-2r. The master identity
`(C-x^p C*)(1+x^h)=0`, with 2h=0, gives
`x^(-s)E=x^(r-p)C(1+x^h)=x^r C*(1+x^h)=E*`.
Also `x^s D={p-r,p-r+h}`. Thus the master family is literally L3*,
with no halving assumption. The earlier globally aligned strict L5 proof
is retained as a valid secondary explanation.

## Integration contract

The fragment has three explicit comment-delimited blocks: UNIVERSAL
FOUNDATION, WEIGHTED LINE INPUT AND BF, and HR. All required prior labels
are preserved: `sec:universal`, `lem:bound`, `cor:finite`, `lem:bf`, `lem:hr`.
The weighted-line proof refers to the root algebra fragment's `sec:linefull`.
No new preamble macro is needed; all commands are standard LaTeX/amsthm/
amsmath or already defined in the manuscript. Root owns source integration,
standalone compilation and the fresh final attack.

No actual mathematical defect was found in the source arguments reviewed.
The fragment deliberately distinguishes original integral rank from image
rank, universal torsion from projected collisions, finite-certificate
predicates from numerical summaries, and solver completeness from bounded
integer tests. Initial local typesetting/formula draft errors were corrected
before handoff; no incorrect transitional equation remains in the fragment.
