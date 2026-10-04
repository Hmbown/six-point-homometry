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

1. **License.** None has been selected. Zenodo requires one for an
   open-access record, and GitHub readers will assume "all rights reserved"
   without one. Common choices for a proof-and-code package: MIT or
   Apache-2.0 for the code with CC-BY-4.0 for the prose, or a single
   CC-BY-4.0. Add a `LICENSE` file and the matching `license` fields to
   `CITATION.cff` and `.zenodo.json`.
2. **Visibility.** The GitHub repository `Hmbown/six-point-homometry` is
   private. Zenodo's GitHub integration only archives public repositories.
3. **What to call the release.** Suggested tag: `v2026.10.04`. The version
   strings in `CITATION.cff` and `.zenodo.json` match it.

## Steps

```sh
# 1. From the repository root, run the gate and the archive builder.
.venv/bin/python scripts/verify.py
.venv/bin/python scripts/make_release_archive.py          # prints path and SHA-256

# 2. Commit, tag and push (publishing: owner action).
git tag -a v2026.10.04 -m "Archived release for DOI"
git push origin main --tags

# 3. On zenodo.org: Settings -> GitHub -> enable the repository, then publish
#    a GitHub release for the tag. Zenodo creates the record and DOI from
#    .zenodo.json. Alternatively upload the tarball from step 1 by hand.

# 4. Paste the DOI into CITATION.cff (`doi:` field) and README.md, commit.
```

## What the archive is and is not

The archive is the evidence package: proofs, reviews, certificates, code and
the Lean files. It is not a claim of external validation. The README and
`docs/RESULTS.md` state the status of every result; keep those statements
unchanged in any release description.
