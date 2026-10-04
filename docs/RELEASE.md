# Preparing an archived release (DOI)

Prepared 4 October 2026 for the owner, Hunter Bown. Everything below is
reversible except the last two steps, which publish; those are left to the
owner on purpose.

## What is already in place

- `CITATION.cff` (GitHub renders a "Cite this repository" button from it).
- `.zenodo.json` (Zenodo reads it when a GitHub release is archived).
- `scripts/make_release_archive.py` builds a reproducible tarball of the
  public files and prints its SHA-256; the default output is
  `.reproduction/release/`, which is ignored by Git.
- `scripts/verify.py` is the bounded verification gate; `scripts/audit_repository.py`
  checks every public file against `docs/PUBLIC_MANIFEST.json`.

## Decisions only the owner can make

1. **License.** Decided 4 October 2026: MIT for code, CC BY 4.0 for the
   written mathematics, documentation, data and certificates (`LICENSE`,
   `LICENSE-CC-BY-4.0`; fields set in `CITATION.cff` and `.zenodo.json`).
2. **Visibility.** Done 4 October 2026: the former private repository,
   which also held parent-archive branches, is now
   `Hmbown/six-point-homometry-archive` (private); the public
   `Hmbown/six-point-homometry` holds only this package's `main`.
3. **What to call the release.** Suggested tag: `v2026.10.04`. The version
   strings in `CITATION.cff` and `.zenodo.json` match it.

## Steps

```sh
# 1. From the repository root, run the gate and the archive builder.
.venv/bin/python scripts/verify.py
.venv/bin/python scripts/make_release_archive.py          # prints path and SHA-256

# 2. On zenodo.org (browser): log in with GitHub, Settings -> GitHub, flip the
#    switch next to Hmbown/six-point-homometry.  Do this BEFORE the release:
#    Zenodo only archives releases made after the switch is on.

# 3. Then tag and publish a GitHub release; Zenodo creates the record and DOI
#    from .zenodo.json within a few minutes.
git tag -a v2026.10.04 -m "Archived release for DOI"
git push public main --tags
gh release create v2026.10.04 -R Hmbown/six-point-homometry --title "v2026.10.04" \
   --notes "Computer-assisted generating theorem for six-point homometry; see README for status."
#    Alternatively upload the tarball from step 1 by hand at zenodo.org/deposit.

# 4. Paste the DOI into CITATION.cff (`doi:` field) and README.md, commit.
```

## What the archive is and is not

The archive is the evidence package: proofs, reviews, certificates, code and
the Lean files. It is not a claim of external validation. The README and
`docs/RESULTS.md` state the status of every result; keep those statements
unchanged in any release description.

## Suggested note to the authors who posed the problem

Erickson and Jones (arXiv:2412.08997) pose the extension to six and more
points as an open problem. A short message once the DOI exists:

> Subject: A computer-assisted generating theorem for six-point homometry in Z_n
>
> Dear Professors Erickson and Jones,
>
> Your paper on five-point homometric subsets of Z_n poses the extension to
> larger cardinalities as Problem 5.2. I have a result in that direction and
> would value a sanity read before I make any stronger claim about it.
>
> For every n, the translation/reflection classes of six-element subsets of
> Z_n with equal interval multisets are exactly the connected components of
> an explicit construction graph (Bloom's two-parameter family, four
> conditional block moves, a dyad exchange, half-coset complementation, a
> conditional unit move and thirteen rigid templates). It is a generation
> theorem, not the classification-with-counts you ask for. The proof lifts
> any homometric pair to a universal signed-matching group, bounds its
> torsion by 135, and exhausts the positive-rank cases by a weighted
> real-line theorem and finite certificates. The repository (DOI below)
> has the full proofs, the certificates, Lean proofs of the soundness
> lemmas, and an Ethos replay of the SMT certificates.
>
> I should be clear that the work was done with substantial AI assistance
> under my direction and has not been peer reviewed. I would be grateful
> for any objection, especially to the real-line encodings or the
> completeness of the quotient-DAG cover, and for any prior work I have
> missed (Yovanof 1988, Soderberg 1995, Patterson 1944 and Bullough 1961
> are already compared).
>
> DOI: [to be filled]
>
> With thanks, Hunter Bown
