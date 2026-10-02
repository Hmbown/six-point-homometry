# Prime six-point counting: focused literature pass

30 September 2026. **[OPEN] historical priority; no novelty claim.**
This pass addresses exact counting of the classical two-parameter six-point
locus in prime cyclic groups. It is not an exhaustive bibliography or a proof
that no earlier count exists. `VERIFIED` below means the stated primary scope
was read; it does not upgrade an unread historical proof.

## 1. Counted object and outcome

The research target is the number of **unordered pairs of distinct T/I
classes** arising from the classical six-point family in Z_ell. Multiplication
by a unit may organize those pairs, but quotienting by all units would count
a different object. The target formula supplied to this pass was

    (ell-1)(ell-11)/12, for primes ell >= 13.

It concerns the Bloom locus. The program's existing large-prime corollary
can turn a proved locus count into a total count for primes ell > 131; this
literature note does not prove either statement.

**Focused search outcome:** no read primary source located in this pass
states that exact finite-prime formula or a complete finite-prime
classification with its parameter stabilizers. This negative outcome does
not establish originality. Direct database failures and unread sources
remain explicit below.

The strongest antecedent for the intended parameter geometry is
Postpischil--Gilbert's planar model. The strongest nearby arithmetic
parameter-counting model is Methawisal's five-point paper. Recent finite-field
frame phase retrieval is a different measurement problem and does not supply
the missing six-point count.

## 2. Primary sources read and their exact scopes

### Postpischil--Gilbert: planar geometry of the classical family

**VERIFIED:** Eric Postpischil and Peter Gilbert, *There Are No New Homometric
Golomb Ruler Pairs with 12 Marks or Less*, Experimental Mathematics **3**(2)
(1994), 147--152, [doi:10.1080/10586458.1994.10504286](https://doi.org/10.1080/10586458.1994.10504286).
[Primary scan](https://emis.de/ft/52010). Read Sections 2--3 and 7, including
a fresh visual inspection of printed p.151 and Figure 1.

Section 3 gives exactly the two endpoint lists used by the program, in
parameters a,b. Section 7 starts with an equilateral triangle and three
half-length parallel extensions. Its six points have no reflection symmetry,
but their directed difference vectors agree with those of the mirror image.
Projection produces the Section 3 family. In the scan the projection
functional is

    -b*x/2 - a*y*sqrt(3)/3 + b*y*sqrt(3)/6.

Text extraction lost leading minus signs; the rendered page is the authority.
The triangular model is prior art for the two-dimensional coefficient
geometry. Rotational/mirror parameter permutations are a useful **inference
to investigate**, not a finite-field orbit theorem stated there. The source
requires distinct distances (Golomb rulers); it neither counts the prime
cyclic locus nor handles all modular coincidences or repeated distances.

### Ranieri--Chebira--Lu--Vetterli: linear support matrices

**VERIFIED:** Juri Ranieri, Amina Chebira, Yue M. Lu and Martin Vetterli,
*Phase Retrieval for Sparse Signals: Uniqueness Conditions*,
[arXiv:1308.3058v2](https://arxiv.org/abs/1308.3058v2),
[primary PDF](https://arxiv.org/pdf/1308.3058v2). Read Section IV.A,
Theorem 1 and Corollaries 1--2 (PDF p.6), and Theorem 2 (p.7).

The displayed six-point lists and 6-by-2 support matrices coincide with the
program's family. The article organizes its real-line supports into a finite
union of permuted two-dimensional subspaces; ordering permutations depend
on parameter direction. This is a relevant antecedent for linear equations
between labeled endpoint lists. Its completeness statement is quoted from
Bekir--Golomb and assumes collision-free real-line differences. It does not
prove finite-prime nonredundancy or a modular orbit count. The original
Bekir--Golomb proof remains **[LIT-VERIFY]** in this pass.

### Jedrzejewski--Johnson: earlier small-prime family counts

**VERIFIED:** Franck Jedrzejewski and Tom Johnson, *The Structure of
Z-Related Sets*, [arXiv:1304.6608v1](https://arxiv.org/abs/1304.6608v1),
[primary PDF](https://arxiv.org/pdf/1304.6608v1), Section 3, printed pp.4--5.
Published in MCM 2013, LNCS **7937**, 128--137,
[doi:10.1007/978-3-642-39357-0_10](https://doi.org/10.1007/978-3-642-39357-0_10).

The table explicitly counts nontrivial interval-vector **families**, with
sets taken modulo transposition/inversion. For six notes it gives
2,16,21,33 at moduli 13,17,19,23. These are not labeled Bloom counts and are
not by definition pair-edge counts. Thus the table alone must not be used
to conflate those two objects. At small primes where the program's separate
census verifies every family has size two, it provides a literature comparison
for the total pair count. Section 3 and the conclusion still leave general
enumeration open in the 2013 source.

### Althuis--Gobel: odd cyclic constructions, not the proposed count

**VERIFIED:** T.A. Althuis and F. Göbel, *Z-related pairs in microtonal
systems*, University of Twente Memorandum **1524** (April 2000).
[Institutional record](https://research.utwente.nl/en/publications/z-related-pairs-in-microtonal-systems/),
[primary PDF](https://ris.utwente.nl/ws/files/5115044/1524.pdf).
Read the complete eight-page text. Browser PDF access failed, but direct
retrieval of the institutional PDF succeeded.

Section 5, Property 7 supplies odd-modulus pairs whose cardinality varies
with the modulus. The displayed n=17 instance has six notes. This is an
explicit cyclic construction, not an all-prime six-point classification or
enumeration of the two-parameter line-family locus. Sections 2--3 discuss
parameter double counting for particular four/five-note constructions,
reinforcing the need to verify a quotient rather than infer its denominator.

### Erickson--Jones and Methawisal: nearby classification and orbit methods

**VERIFIED scopes:** W.Q. Erickson and N.B. Jones,
*Homometric subsets of Z_n with cardinality 5: classification and
enumeration*, [arXiv:2412.08997v4](https://arxiv.org/html/2412.08997v4),
Section 4 and Section 5, Problem 5.2. The read version gives disjoint
five-point types and a counting generating function; Problem 5.2 asks for
cardinality at least six. A publisher journal record was also found, but
the source used here remains arXiv v4.

**VERIFIED scopes, UNREFEREED:** P. Methawisal,
*Unit Actions on Homometric Five-Point Subsets of Cyclic Groups*,
[arXiv:2608.11414v1](https://arxiv.org/html/2608.11414v1),
Proposition 2.2 and its proof, Section 5.3, Section 6, and Appendix A.
It distinguishes intrinsic parameter identifications of unordered
homometry classes from the unit action on those classes, then computes
stabilizers/orbit sizes. Appendix A exhibits dihedral transformations
realizing the claimed identifications. Section 6 leaves larger-cardinality
arithmetic parameterizations open. This is a useful proof model, not a
six-point counting input.

### Recent phase retrieval: relevant contexts with different scopes

**VERIFIED scopes:** David Bartusel, Hartmut Führ and Vignon Oussa,
*Phase retrieval for affine groups over prime fields*,
[arXiv:2109.07123v2](https://arxiv.org/html/2109.07123v2),
Section 1, the group-frame definitions in Section 2, the affine-group setup
in Section 3 and Remark 6.11. The measurement system is the magnitudes of
inner products against a group frame; its strongest result recovers matrices
from a rank-one projection orbit. Remark 6.11 uses many frequency-deletion
projections. These are richer measurements than one binary signal's DFT
magnitudes. The title's prime-field group does not make its result an
enumeration of binary homometric six-subsets of Z_ell.

**VERIFIED scopes:** Tamir Bendory, Dan Edidin and Ivan Gonzalez,
*Finite Alphabet Phase Retrieval*,
[arXiv:2301.10647v2](https://arxiv.org/html/2301.10647v2),
Sections 1--3, Proposition 5.5's proof, and Section 6.1.
Published in Applied and Computational Harmonic Analysis **66** (2023),
151--160, [doi:10.1016/j.acha.2023.04.005](https://doi.org/10.1016/j.acha.2023.04.005).
The source reduces periodic finite-alphabet recovery to homometric support
partitions and discusses finite abelian groups. The binary case is the
usual difference-multiset problem. It does not give a six-subset prime count.
Finite *alphabet* must also not be confused with Fourier measurements valued
in a field of positive characteristic.

**VERIFIED scopes:** Tamir Bendory, Dan Edidin and Oscar Mickelin,
*The beltway problem over orthogonal groups*,
[arXiv:2402.03787v2](https://arxiv.org/html/2402.03787v2),
Sections 1--3, the Gram-matrix setup in Section 4.1, and Section 5.
Published in Applied and Computational Harmonic Analysis **74** (2025),
101723, [doi:10.1016/j.acha.2024.101723](https://doi.org/10.1016/j.acha.2024.101723).
It identifies periodic binary phase retrieval with regular-polygon beltway
reconstruction and then treats Euclidean orthogonal-group autocorrelations.
Its collision-free bounds and sphere/generic statements have that latter
scope. They do not enumerate prime cyclic six-point pairs. In particular,
generic weighted uniqueness does not eliminate constant-weight Bloom pairs.

## 3. Required-venue search and access record

| Venue | Exact focused search or endpoint | What was actually accessible |
|---|---|---|
| arXiv | `"homometric" "prime" site:arxiv.org`; direct primary URLs above | EJv4, Methawisalv1, affine-groupv2, finite-alphabetv2, orthogonal-beltwayv2 HTML; Ranieriv2 and JJv1 PDFs read. No matching count located in these scopes. |
| MathSciNet | `https://mathscinet.ams.org/mathscinet/search/publications.html?pg1=TI&s1=homometric+six+prime`; indexed `homometric six prime site:mathscinet.ams.org` | Direct endpoint returned tool Internal Error. Indexed fallback returned no usable matching record. No MathSciNet review read. |
| zbMATH | `https://zbmath.org/?q=homometric+six+prime`; indexed `homometric six finite fields site:zbmath.org` | Direct endpoint returned tool Internal Error. Indexed fallback was noisy/unusable. No targeted review read. |
| Google Scholar | `https://scholar.google.com/scholar?q=homometric+six+prime+Bloom` | Direct endpoint returned tool Internal Error. General indexed title searches were used; they are not a Scholar corpus search. |
| OEIS | `"homometric" "six" site:oeis.org`; direct `https://oeis.org/search?q=2%2C8%2C12%2C22%2C42%2C50%2C78&fmt=json` | API/search endpoint returned tool Internal Error; indexed search did not locate a relevant sequence. These numbers are the proposed formula's prime values, not a new census. No assertion of OEIS absence. |
| Journal of Mathematics and Music | `"homometric" "six" site:tandfonline.com/doi/ Journal Mathematics Music`; `Zhao "Paths" "homometric" 2026` | Zhao publisher abstract/record located: *From Fourier phase to musical realization: paths between homometric pitch-class distributions*, **20**(2) (2026),136--153, doi:10.1080/17459737.2025.2563675. Full-text fetch failed. Its unseen content remains **[LIT-VERIFY]** for overlap. |
| Journal of Music Theory | `"Z-related" site:read.dukeupress.edu/jmt six prime`; `"Z-related sets as dual inversions"`; direct `https://www.jstor.org/stable/843899` | Soderberg1995 JSTOR metadata endpoint returned no article text. Original remains **[LIT-VERIFY]**. No scope/content conclusion is taken from it. |
| Music Theory Online | `"homometric" site:mtosmt.org`; `"Z-related" "prime" site:mtosmt.org`; direct Capuzzo URL below | Guy Capuzzo, *Maximally Alpha-Like Operations*, **14**(3) (2008), primary full HTML read, especially paragraphs 2--5 and Appendix definitions. It concerns the usual mod12 Z-pairs and transformations, not the prime-count target. |

Capuzzo primary source:
https://mtosmt.org/issues/mto.08.14.3/mto.08.14.3.capuzzo.php.
An initial MTO query used the unproductive domain
`mto.societymusictheory.org`; the correct `mtosmt.org` search above followed.

Other primary-access failures: the publisher full-text page for
Zhao2026 returned Internal Error; primary University of Michigan PDFs
`S0108767311007616.pdf` and `S0108767312002231.pdf` returned429, and the
IUCr article endpoints could not be fetched. These were title-based
crystallographic-enumeration leads, not read counting dependencies.
No account, payment, access circumvention, author contact or external
message was attempted.

## 4. Additional exact topic queries

The following general/indexed searches were run in addition to the
venue-specific queries in Section 3. They were often noisy; unrelated
road-turnpike, homomorphism and prime-metric hits were discarded.

```text
homometric six point prime cyclic groups Bloom enumeration count
"homometric" "finite fields" six
"Bloom" "homometric" enumeration parameters symmetry
turnpike six points prime cyclic beltway classification homometric
"homometric" "six" "prime" -site:crystal-symmetry.com -site:matpic.com
"Bloom" "Bekir" "symmetries"
"homometric" "finite field" phase retrieval
"turnpike" "six" "enumeration"
homometric sets prime modulus Bloom count six points
phase retrieval finite fields cyclic sparse six points homometric
Bekir Golomb six point counterexamples Piccard theorem 2007 pdf
Postpischil Gilbert 1994 geometric model homometric six marks pdf
"finite alphabet phase retrieval" Bendory Edidin Gonzalez pdf
"beltway problem over orthogonal groups" arxiv
"homometric" "p-11"
"2, 8, 12, 22, 42, 50, 78"
"Z-related" "prime" "six"
"homometric" "Bloom" "count"
"Z-related" "microtonal" Althuis Gobel
"homometric" "enumeration" "six" Bloom -turnpike -transportation
"S0108767311007616"
"S0108767312002231"
"cyclic" "homometric" "finite field"
"six" "homometric" "Burnside"
```

The logged historical reading/access gaps in
`notes/2026-09-30-six-formal-references.md` remain, especially the original
Hosemann--Bagchi, Bloom/Bloom--Golomb, Yovanof1988 thesis and Bullough.
This pass does not replace them with search snippets. Neither the label
"Bloom locus" nor this search settles earliest priority of the formulas.

## 5. Reproduction and retained source evidence

Source copies and one inspected rendering are in
`results/2026-09-30-six-prime-literature/`:

```text
postpischil-gilbert1994.pdf
  URL https://emis.de/ft/52010
  SHA256 e9d7cb927f3bcd41a07eeb59252fb8df6bafdc930fe7eafc17679cb977a7637b
althuis-gobel2000.pdf
  URL https://ris.utwente.nl/ws/files/5115044/1524.pdf
  SHA256 c59e4cc61679acba297df5cd15ba955b7a0e16661f17b21be447ba538097640e
ranieri2013v2.pdf
  URL https://arxiv.org/pdf/1308.3058v2
  SHA256 89c87b6bb558bc61ade2f73fd9570e59fce79f7c77235662ccebace21b642eaa
postpischil-gilbert1994-p151.png
  Fresh visual check of Figure1 and projection signs.
althuis-gobel2000.txt, ranieri2013v2.txt
  Local text extraction for the stated reading scopes.
```

PDF fetching used `.venv/bin/python` with standard-library HTTP requests.
Text/render reproduction commands:

```bash
pdftotext -layout results/2026-09-30-six-prime-literature/althuis-gobel2000.pdf results/2026-09-30-six-prime-literature/althuis-gobel2000.txt
pdftotext -layout results/2026-09-30-six-prime-literature/ranieri2013v2.pdf results/2026-09-30-six-prime-literature/ranieri2013v2.txt
pdftoppm -f 5 -singlefile -scale-to 1600 -png results/2026-09-30-six-prime-literature/postpischil-gilbert1994.pdf results/2026-09-30-six-prime-literature/postpischil-gilbert1994-p151
.venv/bin/python tests/run_tests.py
```

Startup/reference tests passed10/10. PDF extraction/rendering reported
recoverable xref/Type3 font warnings; the critical PG page was inspected
visually. No enumerator, solver, symbolic identification search or census
was run by this literature pass; no mathematical headline number is newly
certified here. No ledgers, protected reference files or concurrent agent
outputs were edited.
