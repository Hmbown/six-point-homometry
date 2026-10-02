# Circle affine-plane SMT feasibility experiment

30 September 2026. **[COMPUTED] benchmark and controls, not a completeness
claim.** This is a bounded exploration for the arbitrary-n six-note goal.
The R catalog is separate, in `2026-09-30-six-templates.md`.

## Exact formulation

Normalize the circumference to one and use sorted anchored real coordinates

    A=(0,a1,a2,a3,a4,a5), B=(0,b1,b2,b3,b4,b5),
    0<a1<...<a5<1, 0<b1<...<b5<1.

Choose each circular gap word to be lexicographically least among all its
rotations and reversed rotations. Comparing the two normalized gap words
strictly excludes all T/I equivalence. This loses no genuine pair: a rigid
motion realizes each least word, and exchanging A,B puts them in order.
The test independently compares this normalization with the immutable
reference for 6,435 six-subsets through n=14.

For the fifteen positive edge differences delta, the folded formulation
uses d=min(delta,1-delta). For every A edge d, assert that its multiplicity
among the fifteen A distances equals its multiplicity among the fifteen B
distances. Because the multiplicities across A total fifteen and B has
fifteen edges, these conditions suffice; no unrepresented B distance can
remain. Every condition is quantifier-free linear real arithmetic with
Boolean cases, not a bounded integer-modulus enumeration.

The alternative direct formulation tests each positive delta using

    equivalent(delta,e) iff delta=e or delta+e=1.

It counts an antipodal edge once, since this is a Boolean disjunction.
These are the same distance classes without introducing folded minima.

A rational model v can be converted to an exact cyclic pair by clearing all
coordinate denominators. For a compatible signed edge matching M,
M*v=k is integral. The complete affine plane M*x=k is homometric on the
circle wherever both six-tuples have distinct coordinates: each matched
signed edge differs by an integer number of turns. Thus excluding this
whole plane is sound for a template-union search. The affine plane can be
parameterized by exact elimination and ultimately by its free/torsion
presentation. A later UNSAT claim would still require a separate review
of the encoding and a complete explicit mechanism classification of the
excluded planes.

## Bounded benchmarks

Two seeded exclusion attempts were unsuccessful within their declared
budgets:

1. Preload one matching plane for every census pair at n=12..24, leaving
   583 distinct planes. The folded encoding returns `unknown` at 15 seconds.
2. Use the direct equality-or-sum-one encoding on the same plane union.
   It returns `unknown` at 30 seconds.

These are timeouts, not evidence that a new six-note mechanism exists.
No huge follow-on job was launched. The independent cylinder/weighted-line
and B-star reductions being studied elsewhere are more promising than
raising this unrestricted SAT budget.

An unseeded discovery control succeeds. Three iterations, about 19 seconds
in total, find:

| n | A | B | Compatible matchings | Newly learned planes | Minimum rank |
|---:|---|---|---:|---:|---:|
|96|0,7,17,24,55,65|0,7,17,55,65,72|512|2|8|
|224|0,15,30,56,127,142|0,15,30,86,112,127|288|1|9|
|12|0,1,2,3,6,8|0,1,2,4,6,7|6912|2|9|

At each model only the first 100 matching matrices are explored. This cap
limits discovery, not the validity of an individual plane. The three
models are checked against the immutable reference. They are not claimed
to be new families or outside the reviewed mechanisms.

The `status: sat` in the original unseeded summary describes the last
query **before** its final learned planes were excluded. Its final SMT
file was saved for continuation and not queried. The current script records
`last_query_status` and `final_formula_checked` explicitly to prevent this
ambiguity. The two seeded final files are the actual timed-out formulas.

## Verification and reproducibility

The tests reconstruct the 588 saved affine row spaces from their signed
matching labels using the previous independent review's exact rational
elimination, not the production plane normalization. They check six fixed
Z3 controls across both encodings, including a trivial pair rejected by
the T/I conditions. These are implementation controls, not a proof of
unsatisfiability for the general formula.

```bash
.venv/bin/python src/six_templates_circle.py --preload 24 --iterations 12 --timeout 15 --matching-cap 100
.venv/bin/python src/six_templates_circle.py --preload 0 --iterations 3 --timeout 30 --matching-cap 100 --out results/2026-09-30-six-templates-circle-unseeded
.venv/bin/python src/six_templates_circle.py --mode direct --preload 24 --iterations 2 --timeout 30 --matching-cap 100 --out results/2026-09-30-six-templates-circle-direct
.venv/bin/python tests/test_six_templates_circle.py
```

Outputs and exact SMT inputs are in the correspondingly named dated
folders; build and test logs use the same topic stem. Z3's model choice
and time to timeout are operational observations, not stable mathematical
counts. Re-running a discovery command may find a different valid model;
the committed saved planes retain exact checkable certificates.
