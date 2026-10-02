# Punctured periodic supports: focused literature supplement

Date: 1 October 2026. Scope: primary-source search for the construction in
Theorem H of `notes/2026-10-01-weighted-subgroup.md`, and for any prior correction
to the standard-coordinate sparse uniqueness conjectures in Bendory–Edidin
(2020). This supplements the required venue audit in
`notes/2026-10-01-weighted-phase-literature.md`; it does not replace that audit.
Only this note was edited for this task. No author was contacted.

**[OPEN] Priority and the completeness of the search remain open.** No matching
punctured-coset generic cyclic construction or correction was located by the
queries and reading scopes below. That is a search outcome, not a claim that no
such result exists. Phase tori, spectral-unit parametrizations, support
constraints, and nontransverse intersections have substantial prior literature.
This note makes no novelty claim and does not promote the status of our theorem.

## 1. Precise comparison target

The internal construction uses the real, standard-coordinate, **length-N cyclic
DFT** and cyclic autocorrelation. Put N=qm, q≥7, m≥5, H=qZ_N, Q={0,1,3}, and
S=(Q+H)\{0}. The claims to compare are: prescribed exact support S; generic
strengths on S, including a relatively open set of positive strengths; trivial
translation stabilizer of S; difference-class surplus; and a local continuous
same-support ambiguity of dimension floor((m−1)/2)−1. Here a difference class
identifies d with −d and includes the class 0. These are the claims of the
internal note, whose mathematical verification and adversarial review are
tracked separately.

The mechanism first takes a spectral-unit orbit inside the periodic supersupport
Q+H, then imposes one coordinate equation y_0=0. It is useful to distinguish
this **signal-dependent intersection** from a convolution operator that preserves
the smaller support space for every vector. The smaller support can have trivial
translation stabilizer while the larger support still supplies a torus on which
the zero equation cuts out a positive-dimensional level set. A claim of only a
singular Jacobian or a tangent direction would be weaker than the claimed exact
continuous ambiguity: tangency can occur at an isolated intersection.

Three meanings of “aperiodic” must be kept separate: trivial translation
stabilizer in Z_N; failure to be an arithmetic progression; and the use of a
nonwrapping autocorrelation on a finite interval. The last describes different
measurement data. The internal S has the first two properties, but its data are
cyclic and may wrap around the entire length N.

## 2. Primary reading and what each source addresses

The following statements describe inspected formulations and reading scopes.
They are not claims that every proof in these sources has been independently
verified. Where a proof has not been read, its use as a mathematical dependency
remains **[LIT-VERIFY]**.

### Bendory–Edidin (2020): the actual conjecture and its version

Tamir Bendory and Dan Edidin, *Toward a mathematical theory of the
crystallographic phase retrieval problem*, arXiv:2002.10081v2, 2 July 2020;
SIAM Journal on Mathematics of Data Science 2(3), 2020,
DOI [10.1137/20M132136X](https://doi.org/10.1137/20M132136X).
Primary text: [arXiv v2](https://arxiv.org/html/2002.10081v2);
[version record](https://arxiv.org/abs/2002.10081).

Read §4.1.2, §4.2, and §4.3.4, supplementing the earlier audit of §§1,4,5.
PDF Conjecture 4.11 concerns generic signals on a fixed support with more
difference classes than support entries, predicting only intrinsic same-support
symmetries in the fibre. The inspected formulation adds no exclusion for
periodic supersupports or punctures. §4.2 discusses arithmetic-progression
supports and the link between periodized and nonperiodic data when support is
concentrated in half the cycle. Its terminology footnote explains the earlier
use of “periodic” for arithmetic progressions. These are useful distinctions,
not a stated repair covering the comparison target.

The arXiv record still lists v2 as latest. The
[SIAM article page](https://epubs.siam.org/doi/10.1137/20M132136X) was inspected
for correction/erratum notices; none was located. Full journal text remained an
access gap, so journal wording was not independently compared here.

### Edidin–Suresh (2026 version): generic bases are a different quantifier

Dan Edidin and Arun Suresh, *The generic crystallographic phase retrieval
problem*, [arXiv:2307.06835v3](https://arxiv.org/html/2307.06835v3), 30 April
2026; Applied and Computational Harmonic Analysis 84 (2026), 101888,
DOI [10.1016/j.acha.2026.101888](https://doi.org/10.1016/j.acha.2026.101888).

Read Theorem 1.1 and §1.1.1. The main result varies the sparsity basis
generically; the standard-coordinate support spaces in the comparison target
are special, fixed spaces. §1.1.1 continues to describe Bendory–Edidin
Conjecture 4.7 as the standard-basis difference-surplus target, and discusses
arithmetic-progression failures. No punctured-supersupport exclusion or
correction was located in that section. The publisher indexed text was
available, but direct full-article access failed; the inspected full source was
the preprint. Its full proof was not independently checked for this supplement.

### Barnett–Epstein–Greengard–Magland (2020): the closest geometric framework

Alexander H. Barnett, Charles L. Epstein, Leslie Greengard, and Jeremy Magland,
*Geometry of the Phase Retrieval Problem*, Inverse Problems 36 (2020), 094003,
DOI [10.1088/1361-6420/aba5ed](https://doi.org/10.1088/1361-6420/aba5ed).
Primary text: [arXiv:1808.10747v2](https://arxiv.org/html/1808.10747v2),
1 April 2020.

Read §1.1, magnitude-torus definitions, §§2.2–2.3, and §§3.1–3.2.2.
The authors treat phase retrieval as an intersection of a Fourier magnitude
torus with support constraints. They calculate tangent directions through
convolution and translate outside-support zeros into linear equations on the
tangent vector. They study nontransversality, poor conditioning, factor-based
true ambiguities, and approximate ambiguities. Much of the small-support
analysis uses a rectangular support box in a larger periodic grid.

This supplies a clear precedent for the torus-and-zero-constraints method.
However, a nonzero tangent intersection alone does not establish an exact
continuous fibre, and the inspected sections did not state the punctured-coset
generic, positive, fixed-support cyclic counterexample above. A support-box
result is also not automatically an assertion for an arbitrary sparse cyclic
support. This is a scoped reading outcome, not an exhaustive absence claim.

Their 2022 Cambridge book, *Geometry of the Phase Retrieval Problem: Graveyard
of Algorithms*, DOI [10.1017/9781009003919](https://doi.org/10.1017/9781009003919),
is a further priority-search lead. Only the
[chapter 2 summary](https://doi.org/10.1017/9781009003919.005),
“Geometry Near an Intersection,” was accessible and inspected; full chapter and
book were not read.

### Jaganathan–Oymak–Hassibi (2013/2015): oversampled finite-line data

Kishore Jaganathan, Samet Oymak, and Babak Hassibi, *Sparse Phase Retrieval:
Uniqueness Guarantees and Recovery Algorithms*,
[arXiv:1311.2745v4](https://arxiv.org/html/1311.2745), 1 July 2015;
[version record](https://arxiv.org/abs/1311.2745) shows the original 2013 version.

Read §I equations (1)–(3), §II's support definitions, and Theorem II.1.
The uniqueness setting zero-pads a length-n signal and takes a DFT of dimension
at least 2n. Its autocorrelation is a finite nonwrapping sum, with endpoints
depending on lag. “Aperiodic” means the support is not uniformly spaced, i.e.
not an arithmetic progression. The theorem's almost-all uniqueness statement
uses those data. It therefore does not contradict ambiguity for length-N
signals measured at just the N cyclic DFT frequencies. The full appendix proof
was not read for this supplement.

This comparison does not identify a defect in that theorem: adding the missing
Fourier measurements separates cyclic autocorrelation terms that have been
aliased together. The difference is in the measurement operator, even if both
supports are called aperiodic.

### Jaganathan (2016 thesis): the same measurement distinction

Kishore Jaganathan, *Convex programming-based phase retrieval: Theory and
applications*, Caltech PhD thesis, 2016.
Primary [thesis PDF](https://thesis.caltech.edu/9814/1/Kishore_Jaganathan_2016_Thesis.pdf).

Read §2.2 and §3's setup, equations (3.1)–(3.2), the support definition, and
Theorem 3.2.1 (printed pp.16–18, PDF pp.27–29). The sparse formulation sets
M=2N, uses zero padding, and writes nonwrapping autocorrelation. “Aperiodic”
again means nonuniform support spacing. The thesis does not turn the earlier
result into a length-N cyclic measurement theorem in these inspected sections.
Its full uniqueness proof in Appendix 8.1 was not read.

### Novikov–Xu (2026): discrete does not imply finite cyclic

Roman G. Novikov and Tianli Xu, *On Phase Retrieval for Continuous and Discrete
Fourier Transforms*, [arXiv:2604.25662v1](https://arxiv.org/html/2604.25662v1),
28 April 2026.

Read §§1–3, Theorems 1–2, examples, and Remark 7. In the discrete setup the
signal is finitely supported on Z^d and Fourier magnitude is given over the
frequency torus; it is not just a finite N-point cyclic sample. The authors
construct ambiguities through differential/difference operators and convolution
factor flips, including Pauli-related examples. The inspected statements do
not assert the comparison target's generic positive fixed-support cyclic fibre
or a correction to the 2020 conjecture. The detailed proof section was not
independently checked. This paper is a relevant contemporary ambiguity source,
but its discrete measurement setting must not be conflated with ours.

### Older periodic-image work: unresolved access gap

R. P. Millane, *Phase problems for periodic images: effects of support and
symmetry*, Journal of the Optical Society of America A 10(5) (1993),
1037–1045, DOI [10.1364/JOSAA.10.001037](https://doi.org/10.1364/JOSAA.10.001037).
The [primary publisher abstract](https://opg.optica.org/josaa/abstract.cfm?uri=josaa-10-5-1037)
discusses underdetermined periodic two-dimensional images and the effects of
support and symmetry. Full text was not accessible. Whether it contains a
comparable zero-constrained periodic orbit is **[LIT-VERIFY]**. Its date and
scope make this a material gap before any priority claim.

The earlier audit also identified primary spectral-unit and homometric
distribution papers (Mandereau et al. 2011 and Il'inskaya 2016). Their recorded
readings already establish classical weighted phase families and subgroup
embedding precedents. This supplement did not reread those papers. The
unread full text of Zhao's 2026 Journal of Mathematics and Music paper remains
another gap recorded in that audit; its abstract is not enough to settle
priority for punctured supports.

## 3. Correction search and its limits

Besides the two arXiv version records and SIAM page above, the primary
[Bendory publication list](https://www.tau.ac.il/~bendory/publications.html)
was inspected for the original article and correction notices. No such notice
was located. Exact title/identifier/conjecture queries below found no matching
correction. A notice can be absent from these sources while a later paper,
unindexed manuscript, lecture, or inaccessible journal version contains the
observation. No author correspondence or comprehensive citation-graph audit
was performed. The required venue audit's Google Scholar, MathSciNet, zbMATH,
and journal access limitations remain limitations here.

The literal fixed-support cyclic conjecture in the inspected arXiv v2 is the
comparison target. Distinct-support incidence claims and generic-basis claims
have different quantifiers; a same-support family by itself does not refute
them. The older oversampled theorem has a different operator. These scope
distinctions should accompany any eventual mathematical counterexample report.

## 4. Exact query log

All queries were issued to the web search tool on 1 October 2026. Quoted phrases
below preserve the submitted query strings. Irrelevant results (e.g. optical
instrument corrections, coding-theory punctures, and unweighted point-set
homometry) were not used as mathematical evidence. Searches were batched; no
broad support enumeration or computation was part of this task.

```text
"phase retrieval" "punctured" "support"
"phase retrieval" "aperiodic" "generic" "counterexample"
"crystallographic phase retrieval" "counterexample" "2026"
"crystallographic phase retrieval" "correction" OR "erratum"
"crystallographic" "phase retrieval" "aperiodic"
"phase retrieval" "cosets" "zeros"
"spectral units" "support" "zeros"
"phase retrieval" "punctured" "cyclic"
"Bendory" "Edidin" "conjecture" "counterexample"
"phase retrieval" "periodic support" "zero"
"phase retrieval" "support" "torus" "generic" "2020"
"phase retrieval" "sparse" "supersupport"
"The numerics of phase retrieval" arxiv
"crystallographic phase retrieval" "Conjecture 4.7"
"crystallographic phase retrieval" "zero" "orbit"
"periodic autocorrelation" "support" "counterexample" generic
"A geometric analysis of phase retrieval" support torus
"crystallographic phase retrieval" "Conjecture" "periodic"
"Bendory" "Edidin" "punctured"
"phase retrieval" "support" "nonperiodic" "counterexample"
Barnett Epstein Greengard Magland "phase retrieval" geometry torus
"phase retrieval" "torus" "support" "nontransversal"
"crystallographic" "support" "puncture"
"Bendory" "Edidin" "20M132136X" erratum
"phase retrieval" "circulant" "support" "generic"
"phase retrieval" "punctured coset"
"phase retrieval" "aperiodic" "Bendory" "Edidin"
"2002.10081" "counterexample"
"2002.10081" "correction"
"crystallographic phase retrieval" "non-periodic" "generic"
"crystallographic phase retrieval" "coset" "punctured"
"Phase problems for periodic images" "effects of support and symmetry"
"phase retrieval" "coset" "continuous"
"phase retrieval" "support" "puncturing"
"generic" "aperiodic" "crystallographic"
"spectral units" "zero coordinates"
"homometric distributions" "zeros"
"homometric" "aperiodic" "weighted"
"crystallographic phase retrieval" "erratum" OR "corrigendum"
"2002.10081" "periodic" "counterexample"
"phase retrieval" "spectral units" "punctured"
"phase retrieval" "torus" "zero constraints"
"Bendory" "Edidin" "4.11" correction
"crystallographic phase retrieval" "support stabilizer"
"sparse phase retrieval" "aperiodic support" "cyclic"
"homometric" "punctured"
```

The parent additionally searched “crystallographic phase retrieval counterexample
conjecture”, “phase retrieval aperiodic support subgroup”, and “Bendory Edidin
4.11”, and supplied the Jaganathan paper/thesis as leads. Those primary sources
were read here in the scopes specified above.

## 5. Remaining focused checks before any priority statement

1. Obtain Millane's full 1993 paper, the Cambridge book's relevant chapters,
   Zhao's full 2026 article, and the SIAM published text; compare their actual
   support/zero constraints and data operators.
2. Follow references and citations to periodic-image uniqueness and classical
   spectral-unit works for signal-dependent zero constraints, rather than
   treating “aperiodic” as a uniform keyword.
3. Obtain a human expert reading of the cyclic fixed-support counterexample and
   its comparison with the literal conjecture. Mathematical review and priority
   review are separate tasks.

The specific construction was not matched in this bounded search. The general
phase-torus intersection method is established prior work; the exact generic
punctured-support specialization and any earlier conjecture correction remain
**[OPEN]** for priority purposes.
