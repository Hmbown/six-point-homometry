# Composite six-point Bloom image: focused primary literature search

30 September 2026. **[OPEN] historical priority; no novelty claim.**
This is a bounded continuation of
`notes/2026-09-30-six-prime-literature.md`. It addresses the classical
six-point parameter image in cyclic rings, CRT compatibility of rigid
point identifications, prime-power lifting, and exact parameter counts.
The search was not restricted to music: inverse differences, periodic
binary phase retrieval, arithmetic arrangements, and definable counting
were included. No source was contacted and no account/payment/access
circumvention was attempted.

## 1. Target and search outcome

The object is the **unordered pair of distinct translation/inversion
classes** produced by the two classical lists X_(a,b), Y_(a,b), when each
support has six elements in Z/n. A quotient by arbitrary units, an ordered
parameter count, a pair-edge count, and a maximal-family count are different
objects. This search does not identify them.

**No primary source read in this pass states the exact composite cyclic
Bloom parameter-fiber classification or its complete pair count.** In
particular no read source replaces the needed common global point
permutations with independent local signs. This is a search outcome, not
evidence of absence or originality. Historical unread works and database
access gaps remain below.

The positive result is useful: **the Smith-normal-form/gcd mechanism for
counting arrangement complements modulo every integer is published prior
art**, as is its Tutte quasi-polynomial formulation. Thus an eventual
periodic count arising from finitely many integral congruence conditions
should not by itself be presented as a new phenomenon. The work needed
here is the correct integral data and the exact quotient by chord-class
identifications.

The existing n=221 boundary in `notes/2026-09-30-six-next.md` was read:
the parameters (1,4) and (118,30) have equal moment invariants but different
unordered rigid-class pairs. This note neither re-proves nor extends that
counterexample. It rules out treating the field's moment quotient as an
established composite quotient.

## 2. New primary reading and its limits

### Integral arrangements modulo n

**VERIFIED primary scope; [PROVED-LIT] for the stated general counting
theorem:** Hidehiko Kamiya, Akimichi Takemura and Hiroaki Terao,
*Periodicity of hyperplane arrangements with integral coefficients modulo
positive integers*, Journal of Algebraic Combinatorics **27** (2008),
317–330, [doi:10.1007/s10801-007-0091-2](https://doi.org/10.1007/s10801-007-0091-2).
[arXiv:math/0703904v2 primary PDF](https://arxiv.org/pdf/math/0703904v2).
Read §1.1, §2.1 with Lemmas 2.1/2.3 and Theorem 2.4, and §2.3's
Theorem 2.5/proof. Visually checked p.7. Identifier: v2, 2 April 2007;
downloaded PDF typesetting date: 2 July 2018. Hash below fixes the copy.

For an integral matrix C_J of rank r_J with nonzero Smith invariants
d_(J,1),...,d_(J,r_J), its kernel modulo n has cardinality

    n^(m-r_J) * product_i gcd(n,d_(J,i)).

Inclusion–exclusion counts kernel avoidance. Theorem 2.4 gives its monic
degree-m quasi-polynomial with gcd-dependent coefficients and an lcm
period bound; Theorem 2.5 identifies the coprime constituent with the real
characteristic polynomial. This counts parameters, not Bloom pairs.

**Application boundaries:** reduction depends on C, not merely its real
arrangement. Retain actual integral differences: dividing by 2 can change
even-modulus kernels. Values must be nonzero, not necessarily units.
Global support distinctness need not hold in each CRT component.
No minimum period for our arrangement is inferred.

### Tutte quasi-polynomials over finite abelian groups

**VERIFIED primary scope; [PROVED-LIT] for the general formula:** Petter
Brändén and Luca Moci, *The multivariate arithmetic Tutte polynomial*,
Transactions of the American Mathematical Society **366**(10) (2014),
5523–5540,
[doi:10.1090/S0002-9947-2014-06092-3](https://doi.org/10.1090/S0002-9947-2014-06092-3).
[arXiv:1207.3629v4 primary PDF](https://arxiv.org/pdf/1207.3629v4).
Read §7 definitions, Lemma 7.3, Theorems 7.4, 7.6, 7.7 and their proofs,
Remark 7.2, and §9 through Theorem 9.1/proof. Visually checked printed p.19.
Publication metadata was cross-checked against the
[institutional record](https://cris.unibo.it/handle/11585/676812).

For a finite list in a finitely generated abelian group, their partition
function sums over homomorphisms into a finite abelian target. Expansion
counts homomorphisms annihilating sublists using quotient torsion; putting
each weight equal to -1 counts avoidance of all kernels. Theorems 7.4 and
9.1 give the cyclic-target quasi-polynomial and its Tutte specialization.
Remark 7.2 explicitly warns that this quasi-polynomial retains information
about the group/list beyond the arithmetic matroid. This is a relevant
general counting framework, not a twelve-fiber theorem and not a statement
that cyclic Z/(p^r) is the additive group of F_(p^r).

### Definable counting and rational generating functions

**VERIFIED primary scope; [PROVED-LIT] for the general counting theorem:**
Kevin Woods, *Presburger arithmetic, rational generating functions, and
quasi-polynomials*, Journal of Symbolic Logic **80**(2) (2015), 433–449,
[doi:10.1017/jsl.2015.4](https://doi.org/10.1017/jsl.2015.4).
[arXiv:1211.0020v2 primary PDF](https://arxiv.org/pdf/1211.0020v2).
Read Definitions 1.1, 1.6, 1.8–1.9, Theorem 1.10 and its full §4.1 proof,
and the one-dimensional observation in §4.3. Primary author bibliography:
https://www2.oberlin.edu/faculty/kwoods/papers.html.

Theorem 1.10 sends finite Presburger counting functions to piecewise
quasi-polynomials and rational generating functions; in one parameter,
piecewise quasi-polynomial means quasi-polynomial beyond a finite threshold.
**Inference to investigate, [OPEN]:** fixed-cardinality cyclic homometry
counts appear amenable to this theorem. Coordinates lie in a bounded box;
distance equality is a finite disjunction of matchings; bounded congruences
can be expanded into finitely many constant multiples of n; lexicographic
least rigid representatives can be quantified. This pass does not supply
the full encoding/adversarial review or an exact period/formula. Mere
rationality or eventual quasi-polynomiality should be attributed to known
definable-counting machinery if that encoding is completed.

## 3. Refreshed nearby primary scopes

These papers were already read in the prime search. Their particular
boundary sections were fetched again; this is not a new six-point result.

- **VERIFIED, UNREFEREED:** P. Methawisal,
  *Unit Actions on Homometric Five-Point Subsets of Cyclic Groups*,
  [arXiv:2608.11414v1](https://arxiv.org/html/2608.11414v1), §6 and the
  start of Appendix A. The conclusion leaves comparable larger-cardinality
  arithmetic parameterizations/unit actions open within its stated scope.
  The appendix realizes parameter identities by actual dihedral maps.
  It illustrates how to separate intrinsic class identification from a
  subsequent unit action; it does not give a composite six-point count.
- **VERIFIED:** W. Q. Erickson and N. B. Jones,
  *Homometric subsets of Z_n with cardinality 5: classification and
  enumeration*, [arXiv:2412.08997v4](https://arxiv.org/html/2412.08997v4),
  end of §4 and §5 Problem 5.2. Its rational generating function follows
  from its disjoint five-point types; the next-cardinality extension is
  still posed there. This records that paper's stated frontier, not the
  frontier of every other paper.
- **VERIFIED refreshed scope:** Guy Capuzzo, *Maximally Alpha-Like
  Operations*, Music Theory Online **14**(3) (2008),
  [primary HTML](https://mtosmt.org/issues/mto.08.14.3/mto.08.14.3.capuzzo.php),
  paragraphs 1–12. Its operations concern the standard mod12 Z-pairs. No
  composite arbitrary-n parameter-count theorem is present in this scope.

## 4. Required-venue searches and access limitations

All searches below were run on 30 September 2026 with the web search tool.
Search-index hits were used to locate primary sources; unrelated physiology,
different Blooms, and secondary exposition were not treated as evidence.

| Venue | Exact query or endpoint | Actual access/result |
|---|---|---|
| arXiv | `homometric six composite cyclic prime power Bloom site:arxiv.org`; direct primary URLs in §§2–3 | No matching six-ring count located. The three general counting papers and the two refreshed homometry boundary sections were read. |
| MathSciNet | `homometric six composite cyclic site:mathscinet.ams.org`; `https://mathscinet.ams.org/mathscinet/search/publications.html?pg1=TI&s1=homometric+six+composite` | Direct endpoint inaccessible (tool Internal Error); indexed search produced no usable targeted review. No MathSciNet review read. |
| zbMATH | `homometric six finite rings site:zbmath.org`; `https://zbmath.org/?q=homometric+six+composite` | Direct endpoint inaccessible (tool Internal Error); indexed results were irrelevant/noisy. No targeted review read. |
| Google Scholar | `https://scholar.google.com/scholar?q=homometric+six+composite+Bloom` | Direct endpoint inaccessible (tool Internal Error). General indexed title/topic searches are not a Scholar corpus search. |
| OEIS | `homometric six Bloom site:oeis.org`; `https://oeis.org/search?q=homometric+six&fmt=json` | Direct search/API inaccessible (tool Internal Error); indexed hits were unrelated sequences. No sequence match is asserted and no sequence was submitted. |
| Journal of Mathematics and Music | `"homometric" "six" site:tandfonline.com/doi "Mathematics and Music"`; `"Zhao" "From Fourier phase to musical realization"`; direct URL below | Zhao metadata/abstract accessible through indexed publisher result; full primary text returned HTTP403. It remains an unread overlap lead. |
| Journal of Music Theory | `"Z-related" "composite" site:read.dukeupress.edu/jmt`; `"Z-related" "composite" site:read.dukeupress.edu`; `https://www.jstor.org/stable/843899` | No usable composite count located; JSTOR delivered no Soderberg article text. No unseen-content claim made. |
| Music Theory Online | `"Z-related" "six" "cyclic" site:mtosmt.org`; direct Capuzzo primary URL in §3 | Targeted indexed search located no count; refreshed primary Capuzzo paragraphs show the mod12 transformation scope. |

Qiuwan Zhao, *From Fourier phase to musical realization: paths between
homometric pitch-class distributions*, Journal of Mathematics and Music
**20**(2) (2026), 136–153,
https://www.tandfonline.com/doi/full/10.1080/17459737.2025.2563675.
Metadata/abstract **VERIFIED**, full paper **[LIT-VERIFY]**; no conclusion
about its unseen theorem scope is taken. Stephen Soderberg, *Z-Related Sets
as Dual Inversions*, Journal of Music Theory **39**(1) (1995), 77–100,
doi:10.2307/843899, remains full-text **[LIT-VERIFY]**.

## 5. Other exact topic queries

```text
"homometric" "six" "composite"
"homometric" "Bloom" "cyclic"
"homometric" "Chinese remainder"
"characteristic quasi-polynomial" "Z/qZ" arrangement
Kamiya Takemura Terao Periodicity hyperplane arrangements integral coefficients 2008 arxiv
Moci arithmetic Tutte polynomial toric arrangements quasi polynomial 2012 arxiv
"homometric" "Hensel"
"Bloom" "homometric" "finite ring"
"homometric" "prime powers"
"homometric" "six-point" "cyclic"
"homometric" "CRT"
"homometric" "Hensel" "lifting"
"homometric" "Bloom" "enumeration"
"homometric" "prime powers" -physiology -medical
"homometric" "finite rings"
"homometric" "prime-power"
"homometric" "Z/nZ" "six"
Woods Presburger arithmetic rational generating functions quasi polynomials arxiv
"homometric" "composite" "Bloom" -physiology
"Bloom" "homometric" "orbit"
"homometric" "six" "quasipolynomial"
"homometric" "count" "rings" -physiology
"The multivariate arithmetic Tutte polynomial" "5523"
"Presburger arithmetic, rational generating functions, and quasi-polynomials" "433"
"homometric" "six" "normal form" -physiology
"homometric" "six" "prime power" -physiology
```

No original Bekir–Golomb, Bullough, Patterson, Bloom/Bloom–Golomb,
Hosemann–Bagchi, Yovanof thesis, or unread Zhao/Soderberg proof was upgraded.
Their previous reading/access gaps in the prime and formal-reference notes
remain. A human priority review and stronger bibliographic access are needed
before any first/new claim.

## 6. Retained evidence and reproduction

Directory: `results/2026-09-30-six-composite-literature/`. Primary copies
were fetched with standard-library HTTP requests, a 15-second per-source
timeout and no authentication. `source-manifest.json` records requested and
final URLs, HTTP status, byte size, content type, and SHA256. Exact hashes:

```text
kamiya-takemura-terao2007v2.pdf
  93f42a4c6d97195ebc21d077e17f4f1a140f3b2f75cfe4a3d540f0b6ece14657
branden-moci2013v4.pdf
  1d8d1ae81f526b8c17fa3e619f083fc538357cb599256970931b4a1ce37f6d3d
woods2015v2.pdf
  5cf8927f4a966eba78f248ab1c972a6a007c9f579aebd1e0d09be088c55b2c4d
methawisal2026v1.html
  a496ac43d1435d08df48d94b9637c3c0dc89de7ea4ed131a2faa8b57f6432bf9
erickson-jones2026v4.html
  3e8da3ba3d113d43ccef0c047d6286cebaa658e0e11df5821d41074a5f7e9f3d
capuzzo2008.html
  d85a98313d1ec5809e7c4f998b55a12552059f007a1db6ba61ae3a9eb3f502d1
```

Text extractions and the two inspected PNG pages are retained. Commands:

```bash
.venv/bin/python tests/run_tests.py
pdftotext -layout results/2026-09-30-six-composite-literature/kamiya-takemura-terao2007v2.pdf results/2026-09-30-six-composite-literature/kamiya-takemura-terao2007v2.txt
pdftotext -layout results/2026-09-30-six-composite-literature/branden-moci2013v4.pdf results/2026-09-30-six-composite-literature/branden-moci2013v4.txt
pdftotext -layout results/2026-09-30-six-composite-literature/woods2015v2.pdf results/2026-09-30-six-composite-literature/woods2015v2.txt
pdftoppm -f 7 -singlefile -scale-to 1600 -png results/2026-09-30-six-composite-literature/kamiya-takemura-terao2007v2.pdf results/2026-09-30-six-composite-literature/ktt-theorem24
pdftoppm -f 19 -singlefile -scale-to 1600 -png results/2026-09-30-six-composite-literature/branden-moci2013v4.pdf results/2026-09-30-six-composite-literature/bm-theorem91
```

Startup reference suite passed all ten tests. An initial system `python`
invocation was unavailable; all project verification used `.venv/bin/python`.
No census, solver, orbit enumeration, mathematical headline number or new
code test was added by this literature pass. No ledger, protected file,
working manuscript, outside contact, commit or submission was changed.

## 7. Follow-up after the full coefficient classification, 1 October2026

The parent ran a further bounded online search with these exact queries:

```text
"homometric" "Bloom" "coprime"
"homometric" "six" "count" "12"
"homometric" "six" "Chinese remainder"
"homometric" "Bloom" "prime powers"
```

The returned results were mostly broad crystallography/music exposition,
graph homometry, and secondary pointers to the already-read five-point
classification. No returned primary statement supplied the proposed
coprime-to-six Bloom fiber/count theorem. These search-index results were
not used as theorem evidence or to clear historical reading gaps. The
original primary construction proofs, unread overlap leads and restricted
database gaps above still prevent a novelty claim. This follow-up adds no
new primary source or conclusion of absence.
