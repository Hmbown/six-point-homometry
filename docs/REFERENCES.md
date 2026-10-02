# References and attribution

The endpoint formulas, factor reversal, spectral units, cyclic projection
and general modular arrangement-counting methods are established prior
work. This repository's theorem labels describe its own written arguments;
they do not establish historical originality. Source titles and author
credits below are retained as published.

The reading scopes here summarize the recorded primary-source audits.
They do not imply that every result in a cited paper has been independently
verified. Restricted results on the real line, collision-free distances,
fixed supports and generic bases have different hypotheses.

## Classical six-point constructions

**Joseph Rosenblatt and Paul D. Seymour.** “The Structure of Homometric
Sets.” *SIAM Journal on Algebraic Discrete Methods* **3**(3) (1982),
343–350. [DOI](https://doi.org/10.1137/0603035).
Publisher metadata and abstract verified. The original full text was
inaccessible; its proof was not read. Rosenblatt's 1984 primary paper,
Theorem 2.4, p.322, attributes the torsion-free joint factorization to this
source. That restatement allows signed factors over a conjugation-closed
unique factorization domain. It is an antecedent of the integer algebraic
backbone; the abstract alone does not establish a six-point classification
or settle overlap with this repository's full line theorem.

**G. S. Yovanof and S. W. Golomb.** “The Polynomial Model in the Study of
Counterexamples to S. Piccard's Theorem.” *Ars Combinatoria* **48** (1998),
43–63. [Publisher scan](https://combinatorialpress.com/article/ars/Volume%20048/volume-48-paper-4.pdf).
Family N, p.47, gives the two-parameter endpoint formulas and signed
factor-reversal mechanism used here. Relevant formulas and arguments on
pp.43–44, 46–48 and 62–63 were read. The source's displayed product labels
are interchanged relative to its factors; the repository states the directly
checked product orientation. Its attribution to Yovanof's 1988 thesis and
earlier Bloom/Bloom–Golomb work is preserved as historical reporting; those
original sources were not fully read.

**Eric Postpischil and Peter Gilbert.** “There Are No New Homometric Golomb
Ruler Pairs with 12 Marks or Less.” *Experimental Mathematics* **3**(2)
(1994), 147–152.
[DOI](https://doi.org/10.1080/10586458.1994.10504286) ·
[primary scan](https://emis.de/ft/52010).
The full six-page source was read, including §3's classical family,
§§4–6's symbolic search and §7's planar projection model. Its completeness
scope is Golomb rulers, with distinct pairwise distances; it supplies no
all-modulus cyclic six-point fiber count.

**Paul Lemke, Steven S. Skiena and Warren D. Smith.** “Reconstructing Sets
From Interpoint Distances.” DIMACS Technical Report **2002-37** (2002);
published in *Discrete and Computational Geometry* (2003), 597–631.
[Official report record](https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2002/2002-37.html) ·
[official full report](https://archive.dimacs.rutgers.edu/pub/dimacs/TechnicalReports/TechReports/2002/2002-37.ps.gz).
Read §2.1 and the bibliography. Table 1 credits the repeated-distance pair
$\{0,1,2,6,8,11\}/\{0,1,6,7,9,11\}$ to Hosemann–Bagchi (1954).
That qualified attribution precedes Bloom's example; the original 1954
proof remains unread and is not a verified direct dependency.

## Cyclic homometry and smaller cardinalities

**Joseph Rosenblatt.** “Phase retrieval.” *Communications in Mathematical
Physics* **95**(3) (1984), 317–343.
[DOI](https://doi.org/10.1007/BF01212402).
The primary scan's §3, selected §4 examples and appendix proof were read.
This supplies the four-point classification and spectral-unit background,
under the source's coefficient-field hypotheses. Theorem 3.9 credits joint
work with Joel Berman; he is not a bibliographic coauthor. It does not
classify cyclic six-point sets.

**Fresh factorization reading, 1 October 2026:** the primary scan's
pp.319–330 were inspected as text and rendered pages. Theorem 3.6 and its
complete proof, pp.327–328, give joint factor reversal for every cyclic
group and every cardinality, over a conjugation-closed field, with signs
and translations. Factors can be signed or rational and need not be
binary or sparse. Theorem 4.1 and proof, pp.329–330, treat arbitrary
abelian groups with the necessary half-group enlargement. These are
classical all-cardinality algebraic characterizations; they do not
supply the finite six-point admissible-construction grammar or its counts.
Theorem 2.4, p.322, is explicitly a restatement of Rosenblatt–Seymour,
whose original proof remains unread. The cyclic factorization proof's
references to “Lemma 3.3” point to the zero-support projector lemma
numbered 3.2 in the scan. See the
[universal formulation](UNIVERSAL_THEOREM.md) for the distinction between
algebraic equivalence and binary constructive completeness.

**William Q. Erickson and Nicholas B. Jones.** “Homometric subsets of
$\mathbb Z_n$ with cardinality 5: classification and enumeration.”
[arXiv:2412.08997v4](https://arxiv.org/abs/2412.08997v4), 27 August 2026.
Read the stated classification/enumeration scopes, Theorems 4.1/4.4 with
proofs and §5. The source classifies five-point sets modulo cyclic shifts
and reflections into six pair types and one triple type, and counts them.
Its higher-cardinality questions provide context, not priority evidence for
this repository. Section references here use the version actually read.

**Franck Jedrzejewski and Tom Johnson.** “The Structure of Z-Related Sets.”
In *Mathematics and Computation in Music*, LNCS **7937** (2013), 128–137.
[DOI](https://doi.org/10.1007/978-3-642-39357-0_10) ·
[author preprint, arXiv:1304.6608v1](https://arxiv.org/abs/1304.6608v1).
The complete author version, §§1–5, was read. Its constructions and finite
family tables are antecedents, including six-point triples at modulus 16.
The reported family counts are not automatically Bloom pair-edge counts.
No novelty is claimed for the mere existence of six-point triples.

## Modular parameter counting

**Hidehiko Kamiya, Akimichi Takemura and Hiroaki Terao.** “Periodicity of
hyperplane arrangements with integral coefficients modulo positive
integers.” *Journal of Algebraic Combinatorics* **27** (2008), 317–330.
[DOI](https://doi.org/10.1007/s10801-007-0091-2) ·
[arXiv:math/0703904v2](https://arxiv.org/abs/math/0703904v2).
Read §§1.1, 2.1 and 2.3, including the Smith-factor kernel counts and
inclusion–exclusion/quasipolynomial proofs. These are prior methods for
counting admissible parameters modulo every integer. Identifying parameters
that produce the same unordered rigid-class pair is a separate obligation.
The support proof also gives an elementary exact-order overlap argument.

## Weighted phase retrieval

**John Mandereau, Daniele Ghisi, Emmanuel Amiot, Moreno Andreatta and
Carlos Agon.** “Discrete phase retrieval in musical structures.”
*Journal of Mathematics and Music* **5**(2) (2011), 99–116.
[DOI](https://doi.org/10.1080/17459737.2011.608820) ·
[author preprint](http://articles.ircam.fr/textes/Mandereau11b/index.pdf).
Read the circulant/Fourier and spectral-unit arguments in §§2.2–2.4,
including the explicit real $\mathbb Z_3$ spectral-unit circles on
preprint pp.6–7. This is a classical antecedent of continuous weighted
ambiguity. The paper attributes the homometric-pair spectral-unit theorem
to Rosenblatt. Its units need not produce binary indicators.

**I. P. Il'inskaya.** “Phase retrieval for probability measures on cyclic
groups.” *Matematychni Studii* **46**(1) (2016), 89–95.
[DOI](https://doi.org/10.15330/ms.46.1.89-95).
Theorems 1–3 and their primary publisher proofs, pp.91–93, were read.
Positive continuous ambiguity on $\mathbb Z_3$ and subgroup embeddings
are antecedents. No priority is claimed for those mechanisms.

**Tamir Bendory and Dan Edidin.** “Toward a mathematical theory of the
crystallographic phase retrieval problem.” *SIAM Journal on Mathematics
of Data Science* **2**(3) (2020), 809–839.
[DOI](https://doi.org/10.1137/20M132136X) ·
[arXiv:2002.10081v2](https://arxiv.org/abs/2002.10081v2), 2 July 2020.
The repository's counterexample comparison is to the literal arXiv v2
Conjectures 4.7 and 4.11, with genericity in each fixed coordinate support
and folded differences including zero. Relevant §§1.3, 4.1–4.3 and 5
were read. Full journal wording was not independently compared. No claim
is made about a correction, retraction, every subsequent theorem, the
distinct-support conjecture, or its separate measure-zero assertion.

## Historical-priority limits

The literature searches located no matching statement of the specific
general generating grammar or all-modulus Bloom fiber/count theorem in
the primary sources read. This is a bounded search result. Access gaps
remain in MathSciNet, zbMATH, Google Scholar and OEIS, and in historical
originals and some later full texts. Missing access and unsuccessful
searches do not establish originality. The proof package is intended for
mathematicians to inspect, reproduce and compare with prior work before
any first-solution claim or formal submission.
