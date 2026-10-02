# All-modulus classical Bloom matching evidence

The mathematical statement and current review status are in
`notes/2026-10-01-six-bloom-primary.md`. These outputs are exact
**[COMPUTED]** certificates; no novelty claim and no total six-subset
census claim.

- `benchmark.json`: the first 72,000 universal pair systems, explicitly
  incomplete. It establishes affordability before the full run.
- `pair-certificate.json`: all 4,147,200 raw labelled pair matchings;
  rank counts 12/864/4,146,324; complete invariant histograms and one
  reconstructible matching witness per histogram class.
- `endpoint-certificate.json`: all 5,760 raw single-endpoint systems;
  the rank-one even-modulus survivors are retained, not ruled out.
- `small-gap-images.json` and `small-reference-images.json`: independent
  complete parameter images for every divisor that can survive the
  paired minor-gcd table. They retain full image fibres and G-orbits.
- `even-endpoint-controls.json`: all 120 even moduli 18..256 for the
  separately proved infinite shared-endpoint family; actual sets,
  immutable-reference T/I classes, and interval vectors. This is a
  construction check, not a six-subset census.
- `tests.log`: six meaningful test groups, including direct original
  equation checks at nonunit 2/3, complete finite controls against the
  immutable reference, exact integer difference identity, larger
  primary controls, and the shared-endpoint family.

Reproduce from the repository root with `.venv/bin/python`, using the
commands in proof §6. The immutable `src/homometry.py` is imported
read-only; no protected reference or data files were edited. Neither
centering nor inversion of six occurs in the matching generator.

The separate fresh attack independently reconstructs the full matching
histograms using a different endpoint pivot and retains its own review
and evidence; consult the root-linked review for the acceptance decision.
