# Weighted cyclic phase retrieval: literature and statement attack

1 October 2026. Independent read-only literature subtask for the newly
authorized weighted phase-retrieval research. Baseline command
`.venv/bin/python tests/run_tests.py` passed all 10 groups. The root's plan
is already recorded in PROGRESS.md. This note does not certify the new
in-house mathematical proof and makes **no novelty claim**.

## Findings and their scope

**[OPEN: priority; statement comparison verified]** The proposed
`N=21`, `H={0,7,14}`, `S={0,1,3}+H` example is not excluded by an extra
primitive, aperiodic-support, or positivity hypothesis in the freshly read
2020 arXiv statement. If the independent mathematical attack validates
the continuous same-support orbit, it contradicts Conjecture 4.11 **as
stated in arXiv:2002.10081v2**, and therefore Conjecture 4.7 there.
This example alone does not contradict the distinct-support recovery
Conjecture 4.8 or the separate measure-zero/transversality conjecture.

**[PROVED-LIT: classical antecedents, proofs/scopes read]** Neither real
spectral-unit circles nor continuous positive cyclic ambiguities are new
phenomena. The 2011 musical phase-retrieval paper explicitly describes the
real order-three spectral-unit circle. Il'inskaya 2016 proves positive
order-three ambiguity, including embedding into a larger cyclic group.
The specific nine-variable, three-coset application to the 2020
fixed-support conjecture was not located in this limited search.
Access gaps below prevent a historical-priority conclusion.

## Primary reading: exact statements

### Bendory--Edidin 2020

Tamir Bendory and Dan Edidin, *Toward a mathematical theory of the
crystallographic phase retrieval problem*, SIAM J. Math. Data Sci. 2(3)
(2020), 809--839, DOI [10.1137/20M132136X](https://doi.org/10.1137/20M132136X).
Freshly read [arXiv:2002.10081v2](https://arxiv.org/pdf/2002.10081v2),
especially §§1.1,1.3,4.1--4.3,5.1--5.2. Publisher full PDF returned 403;
the journal wording was not independently compared in full.

**[VERIFIED: arXiv formulation]** `S-S` counts difference classes modulo
sign, including zero. For each fixed support, genericity means a nonempty
Zariski-open subset of `L_S`, rather than random support choice.

| Location in v2 PDF | Mathematical condition/conclusion, paraphrased |
|---|---|
| Conjecture 4.7, p.13 | `|S-S|>|S|`; generic `x` in `L_S` is recovered modulo the intrinsic group `D`. |
| Conjecture 4.8, p.13 | For distinct dihedral support classes of equal cardinality `K` and equal difference-set cardinality greater than `K`, generic `a(x)` avoids the competing support image. |
| Conjecture 4.11, p.16 | `|S-S|>|S|`; another `x'` in the same `L_S` with equal autocorrelation must equal `g x` for `g in D_S`. |

For real vectors `D` is sign times dihedral symmetries and `D_S` preserves
`L_S`; this does not include arbitrary real spectral units. Odd `N` is
allowed (§1.3). The arithmetic-progression obstruction (§4.2) is not an
extra assumption. The latest arXiv version is still v2, 2 July 2020.
HTML renumbers these conjectures globally as 9,10,13; use the PDF numbers.

### Mandereau--Ghisi--Amiot--Andreatta--Agon 2011

John Mandereau, Daniele Ghisi, Emmanuel Amiot, Moreno Andreatta and Carlos
Agon, *Discrete phase retrieval in musical structures*, Journal of
Mathematics and Music 5(2) (2011), 99--116, DOI
[10.1080/17459737.2011.608820](https://doi.org/10.1080/17459737.2011.608820).
Freshly read author preprint
[IRCAM](http://articles.ircam.fr/textes/Mandereau11b/index.pdf),
§§2.2.3,2.3,2.4.1, especially pp.6--7.

**[PROVED-LIT: read primary algebraic argument]** Definition 2.7 uses
`I(U)*U=delta_e`; convolution by such a unit preserves the Patterson
function by associativity and commutativity. Proposition 2.8 identifies
the units as a group. The homometric-pair spectral-unit theorem is
attributed there to Rosenblatt, with coefficient-field qualifications.
The footnote on p.7 explicitly identifies the real `Z_3` units with two
circles of circulant matrices whose first-column entries obey

```
a^2+b^2+c^2=1,       a+b+c=+1 or -1.
```

This is exactly the classical small-group mechanism behind an embedding
into the order-three subgroup of `Z_21`. The finite-order rational-unit
classification in Theorem 2.9 does not restrict arbitrary real units to
finite order. The source does not assert the proposed generic
three-coset counterexample to a later conjecture.

Rosenblatt 1984 DOI [10.1007/BF01212402](https://doi.org/10.1007/BF01212402)
is already verified in the repository's earlier work. This pass's live
Project Euclid fetch encountered a security check, so the original is
not newly re-read here. The fresh attribution above is through the
2011 primary paper, not an assertion that this pass read Rosenblatt's
whole proof.

### Il'inskaya 2016: positive measures and embedded order three

I. P. Il'inskaya, *Phase retrieval for probability measures on cyclic
groups*, Matematychni Studii 46(1) (2016), 89--95, DOI
[10.15330/ms.46.1.89-95](https://doi.org/10.15330/ms.46.1.89-95).
[Primary PDF](https://matstud.org.ua/texts/2016/46_1/89-95.pdf),
definitions and Theorems 1--3 read, plus proofs on pp.91--93.

**[PROVED-LIT: proof read]** Theorem 3(i) says the only probability
measures on `Z_3` determined modulo translation/reflection by Fourier
magnitude are the uniform measure and point masses. Its full-support
proof, p.92 equation (7), fixes the sum and squared norm; the third
autocorrelation equation follows from these. A nonuniform positive
triple lies on a nondegenerate plane/sphere circle with infinitely many
positive solutions. Theorem 1(ii), pp.91--92 equation (6), explicitly
embeds the obstruction in `Z_{3r}`: two-point measures on `{0,r}` have
infinitely many positive competitors supported on `{0,r,2r}`.

These results establish classical positivity and subgroup antecedents.
Their competitor cardinality can increase, and they do not by
themselves prove the proposed same-cardinality three-coset statement.

### Edidin--Suresh 2026: generic basis is a different hypothesis

Dan Edidin and Arun Suresh, *The generic crystallographic phase retrieval
problem*, ACHA 84 (2026), 101888, DOI
[10.1016/j.acha.2026.101888](https://doi.org/10.1016/j.acha.2026.101888).
Freshly read [arXiv:2307.06835v3](https://arxiv.org/html/2307.06835v3),
Theorem 1.1, Remarks 1.2/1.4, §1.1.1 and §6. This pass checked the
statement/comparison scopes, not every step of the generic-basis proof.

**[VERIFIED: theorem scope]** Theorem 1.1 assumes a generic basis and
gives generic real recovery for `M<=floor(N/2)`, modulo global sign.
Section 1.1.1 still cites Bendory--Edidin's journal Conjecture 4.7 with
the standard-basis condition `|S-S|>M`. It discusses arithmetic
progressions, without adding an exclusion of coset-union supports.
The theorem cannot establish recovery in every coordinate support.
ArXiv records v3 dated 30 April 2026. The HTML's displayed document-date
line differs from that metadata; do not use it to infer revision history.

### Amir--Bendory--Dym--Edidin: stability outlook

Tal Amir, Tamir Bendory, Nadav Dym and Dan Edidin, *The stability of
generalized phase retrieval problem over compact groups*, arXiv
[2505.04190v3](https://arxiv.org/html/2505.04190v3), 19 November 2025;
ACHA 82 (2026), 101838 as recorded in Edidin--Suresh's bibliography.
Freshly read main-result scope and §6, and compared the older v1 outlook.

**[VERIFIED: scope]** Section 6 explicitly separates the paper's generic
basis hypothesis from standard-basis sparse crystallography and leaves
the latter's stability open. It supplies no missing support assumption
for the 2020 conjecture. This review does not attack or invalidate its
generic-prior bi-Lipschitz theorem.

### Zhao 2026: close musical overlap remains unread in full

Qiuwan Zhao, *From Fourier phase to musical realization: paths between
homometric pitch-class distributions*, JMM 20(2) (2026), 136--153,
DOI [10.1080/17459737.2025.2563675](https://doi.org/10.1080/17459737.2025.2563675).
Publisher abstract freshly read; full article fetch failed, and the
ResearchGate record reports no available full text.

**[VERIFIED: abstract only; full content LIT-VERIFY]** The abstract
describes homometric paths of real-valued distributions through Fourier
phase changes, with visualization and composition tools. This is
direct overlap with any claim of new homometric paths. No conclusion
about its fixed-support or sparse genericity content is warranted.

## Terminology attack on the proposed example

**[OPEN until root proof/independent attack: our mathematical inference]**
`S` contains 0 and 1, hence its differences generate all of `Z_21`.
Thus it is primitive if that term means generating the ambient group.
It is support-periodic because `S+7=S`. Generic unequal strengths on
that support are not translation-periodic as a weighted signal. A
statement excluding signals with a shorter period would therefore
require a different argument from one excluding periodic supports.

The positivity strengthening should be justified by continuity of the
small rotation on a finite set of strictly positive coordinates, with
zeros outside `S` preserved. It must not be inferred merely from the
word crystallographic. A one-dimensional ambiguity circle inside the
ten-dimensional real magnitude torus has measure zero; it does not
contradict a measure-zero assertion about the full fibre.

## Logged searches and access gaps

Queries below were issued on 1 October 2026. Search-result absence is
not evidence that a result does not exist. No author was contacted.

### General/arXiv searches (exact query strings)

```
Bendory Edidin crystallographic phase retrieval conjecture counterexample subgroup support
crystallographic phase retrieval standard basis uniqueness 2026 4.7 4.8 4.11
"The generic crystallographic phase retrieval problem" arxiv
"crystallographic phase retrieval" "subgroup"
"crystallographic phase retrieval" "periodic support"
"Conjecture 4.11" "phase"
"crystallographic phase retrieval" "counterexample"
"phase retrieval" "union of cosets" spectral
"phase retrieval" "support" "spectral units" "generic"
"Toward a mathematical theory" erratum correction phase retrieval
"homometric distributions" "paths" Zhao
"spectral units" "continuous" "homometric"
"phase retrieval" "periodic" "subspace" "counterexample" Bendory Edidin
"crystallographic phase retrieval" "primitive" OR "aperiodic"
site:arxiv.org "crystallographic phase retrieval" coset
"Conjecture 4.7" "Bendory" counterexample
"Conjecture 4.11" "Bendory"
"crystallographic phase retrieval" "coset" OR "cosets"
"crystallographic phase retrieval" "stabilizer"
"homometry" "continuous" "spectral unit" "support"
"phase retrieval" "subgroups" "support" "cyclic" generic
"Phase retrieval for probability measures on cyclic"
"homometry" "cosets" "positive"
"phase retrieval" "cyclic groups" "support" "positive"
"Il'inskaya" "crystallographic" phase retrieval
"Conjecture 4.7" "phase retrieval" "periodic"
"phase retrieval" "support stabilizer" cyclic
"crystallographic phase retrieval" "nonperiodic"
"Toward a mathematical theory of the crystallographic phase retrieval problem" pdf 809
"20M132136X" pdf
"Conjecture 4.11" "CRYSTALLOGRAPHIC"
"20M132136X" correction erratum
```

ArXiv direct records and current HTML/PDF were accessible for the three
modern papers; no later 2002.10081 revision or matching correction was
located. The general searches found the 2016 positive-measure paper.
The query using the straight apostrophe in Il'inskaya is normalized here
from the typographic apostrophe submitted to the search tool.
One additional arXiv-domain-filtered query was:
`"phase retrieval" "periodic support" "convolution" "sparse"`;
it returned no results. This was a targeted search, not exhaustive.

### Required venue attempts

| Venue | Exact query/access attempt | Result/gap |
|---|---|---|
| Google Scholar | `https://scholar.google.com/scholar?q=%22crystallographic+phase+retrieval%22+%22cosets%22`; indexed `site:scholar.google.com "crystallographic phase retrieval" subgroup` | Direct endpoint inaccessible; no matching primary result from indexed fallback. |
| MathSciNet | `https://mathscinet.ams.org/mathscinet/search/publications.html?pg1=TI&s1=crystallographic%20phase%20retrieval`; indexed `site:mathscinet.ams.org "crystallographic phase retrieval"` | Direct endpoint inaccessible; indexed fallback did not establish a reviewed classification or correction. |
| zbMATH | `https://zbmath.org/?q=crystallographic+phase+retrieval`; indexed `site:zbmath.org "crystallographic phase retrieval"` | Direct endpoint inaccessible. A MaRDI metadata mirror was located but was not used as a primary proof. |
| OEIS | `https://oeis.org/search?q=homometric&fmt=json`; `site:oeis.org "homometric"`; `site:oeis.org "spectral units"` | Direct search inaccessible; no relevant sequence/priority certificate. |
| Journal of Mathematics and Music | `site:tandfonline.com "Journal of Mathematics and Music" "homometry" "spectral units"`; earlier `site:tandfonline.com/loi/tmam20 "spectral" "homometric"` | Found 2011 spectral-unit source and 2026 Zhao source; author preprint read, Zhao full-content gap retained. |
| Journal of Music Theory | `site:read.dukeupress.edu/journal-of-music-theory "homometric" "phase"`; `site:read.dukeupress.edu/journal-of-music-theory "homometry" "Fourier"`; `site:read.dukeupress.edu/journal-of-music-theory "Fourier" "phase"`; `Jason Yust 2015 "Fourier" "Journal of Music Theory"` | Found Yust2015 metadata/accepted-manuscript record on BU; it was not read as a fixed-support uniqueness theorem. |
| Music Theory Online | `site:mtosmt.org "spectral unit" phase`; `site:mtosmt.org "spectral units"`; `site:mtosmt.org "homometric" "paths"` | No matching fixed-support obstruction identified. A later domain-filtered `"homometric" "Fourier" "phase"` also returned no results. |

For JMT the same domain-filtered `"homometric" "Fourier" "phase"`
query returned no results. Related MTO bibliographic results from the
Yust search were not promoted into mathematical dependencies.
Live Rosenblatt/Project Euclid reached an additional security check;
SIAM PDF returned 403; Zhao full-article page failed. These access
failures are explicit unresolved priority gaps.

## Local provenance and handoff

The result directory holds local reading copies and text extraction for
Bendory--Edidin v2 and the 2011 IRCAM author preprint. They are reading
artifacts, not new mathematical outputs or permission to redistribute.
Exact source URLs, SHA-256 values and extraction commands are in its
README. The root should commit the original review note and provenance
record explicitly, and avoid blanket-staging third-party reading copies.

The safest public wording, after the independent proof attack, is a
counterexample to the precisely cited arXiv formulation, accompanied by
classical spectral-unit and positive-measure attribution. Whether that
application has appeared elsewhere remains **[OPEN]**. Human specialist
review and comparison with the journal full text are advisable before
external sharing. No message, submission, or external outreach occurred.
