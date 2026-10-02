# Six-point manuscript: corrected classical attributions

30 September 2026. Focused primary-source reading for the mathematical
exposition revision. No novelty claim. This note does not upgrade an unread
historical proof to **[PROVED-LIT]**. It separates a source's own formula from
its report of an earlier author's result.

## 1. The exact two-parameter formula and signed factor

**VERIFIED, primary formula and factor-flip argument:** G. S. Yovanof and
S. W. Golomb, *The Polynomial Model in the Study of Counterexamples to
S. Piccard's Theorem*, **Ars Combinatoria 48 (1998), 43–63**.
[Publisher scan](https://combinatorialpress.com/article/ars/Volume%20048/volume-48-paper-4.pdf).

Read the rendered scan, printed pp.43–44, 46–48, 62–63. Page43 defines
“spanning” by distinct pairwise distances; p.44 defines the normalized
reciprocal and explains factor reversal. Page47, **Family N**, displays

\[
\begin{aligned}
r&=1+x^a+x^{b+2a}+x^{2b-a}+x^{2b+a}+x^{3b-a},\\
s&=1+x^a+x^{b-2a}+x^{2b-2a}+x^{2b}+x^{3b-a},\\
\phi_1&=1+x^a+x^b,\\
\phi_2&=1+x^{b-2a}-x^{b-a}+x^{2b-a}.
\end{aligned}
\]

Thus manuscript B has **a=p, b=q, X=s, Y=r**. The endpoint formula and
signed factor are established antecedents. Page47 attributes the unified
six-mark spanning-ruler family to Yovanof's thesis, listed on p.63 as
*Homometric Structures*, USC, August1988; that thesis was **not read**.
Pages46–47 report earlier families from Bloom–Golomb1977 and the
span17 example from Bloom1977. Those originals remain **[LIT-VERIFY]**.
Neither this reading nor that historical report verifies completeness with
repeated distances or weighted atoms.

### Product-label correction in the scan

The Family N display labels r=phi1 phi2 and s=phi1 phi2*, but its endpoint
labels are reversed relative to its printed factors. Direct multiplication
gives the manuscript's orientation:

\[
 X=FQ,\qquad Y=FQ^\dagger,\qquad
 Q^\dagger=x^{2q-p}Q(x^{-1}),
\]

where F=1+x^p+x^q and Q=1+x^{q-2p}-x^{q-p}+x^{2q-p}.
At p=1,q=6 the exact products are

```text
FQ     = 1+x+x^4+x^10+x^12+x^17
FQrev  = 1+x+x^8+x^11+x^13+x^17.
```

This is a transcription/algebra check of the source's formula, not a new
classification claim. Cite **Family N, p.47**, while stating the identity
with the manuscript's correct product orientation. Do not reproduce the
scan's swapped product labels.

## 2. The repeated-distance six-point example predates Bloom's example

**VERIFIED as a secondary historical attribution in a primary survey:**
Paul Lemke, Steven S. Skiena and Warren D. Smith, *Reconstructing Sets From
Interpoint Distances*, **DIMACS Technical Report2002-37 (2002)**.
[Official record](https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2002/2002-37.html);
[official full text, compressed PostScript](https://archive.dimacs.rutgers.edu/pub/dimacs/TechnicalReports/TechReports/2002/2002-37.ps.gz).
Published version: in *Discrete and Computational Geometry* (Springer,2003),
597–631. The [public published excerpt](https://dodona.be/en/exercises/1441444585/media/Lemke2003.pdf)
has only two pages; it is not the complete paper.

Read the official report's §2.1, printed pp.4–6 (PDF pp.6–8), and references,
printed p.30 (PDF p.32). **Table1, printed p.5**, gives

\[
\{0,1,2,6,8,11\},\quad\{0,1,6,7,9,11\}
\]

and credits **[hose54]**. Its reference identifies R. Hosemann and S. N.
Bagchi, *On homometric structures*, **Acta Crystallographica7 (1954),237–241**.
The exact substitution p=1,q=4 in manuscript B yields these endpoints.
Lemma2.1's prose also cites their1962 book; do not confuse the book citation
with Table1's1954 attribution.

The [IUCr issue record](https://journals.iucr.org/q/issues/1954/03/00/)
independently verifies authors, title, pages and
[doi:10.1107/S0365110X54000709](https://doi.org/10.1107/S0365110X54000709).
The original PDF returned401; the publisher's
[access page](https://journals.iucr.org/paper?buy=yes&cnor=a01120)
requires subscription/purchase. Original mathematical content remains
**[LIT-VERIFY]**. Cite **Lemke–Skiena–Smith, Table1**, for the qualified
historical attribution, rather than presenting the unread1954 article as
a verified direct source.

## 3. Classical block translation and reflection precursors

### Callender–Hall conference handout

**VERIFIED, primary handout read in full (4pages):** Clifton Callender and
Rachel Hall, *Crystallography and the structure of Z-related sets*, Society
for Music Theory annual meeting, Nashville,TN, **7November2008**.
[Author-hosted primary PDF](https://myweb.fsu.edu/ccallender/z-relationhandout.pdf).

Page2, **Case3**, sets P={0,6}, R1=I0(R1), R2=I6(R2), and
S_x=P union T_x(R1 union R2), with S_x homometric to S_-x.
Page3, **Cases4a/4b**, explicitly credit Bullough. They keep the regular
m-fold division P fixed and translate an n-point refinement Q by
12k/(mn). Case4b permits choosing each Q-point in the corresponding
P-coset. These are direct block-translation antecedents; the handout uses
continuous pitch-class space except Case2. As in the manuscript, genuine
set endpoints require collision control and T/I inequivalence.

**Bullough historical credit is verified through that handout, not through
the original proof.** The
[IUCr issue record](https://journals.iucr.org/q/issues/1961/03/00/) and
[article page](https://journals.iucr.org/paper?S0365110X61000838)
verify R. K. Bullough, *On homometric sets. I. Some general theorems*,
**Acta Crystallographica14 (1961),257–268**,
[doi:10.1107/S0365110X61000838](https://doi.org/10.1107/S0365110X61000838).
The original PDF returned401. Its proof remains **[LIT-VERIFY]**.

### Goyette thesis

**VERIFIED, focused primary sections:** Jeremiah Goyette, *The Z-Relation
in Theory and Practice*, PhD thesis, University of Rochester,2012.
[Institutional record](https://urresearch.rochester.edu/institutionalPublicationPublicView.action?institutionalItemId=24384&versionNumber=1);
[primary thesis PDF](https://urresearch.rochester.edu/fileDownloadForInstitutionalItem.action?itemFileId=76476&itemId=24908).
The PDF title matches the record; printed page p is PDF page p+17.

Read printed pp.118–123,125–128,131–135,137 and bibliography pp.218–219.
Section3.1 credits Callender–Hall/Patterson/Bullough and gives
**Formula3.1/3.2, p.120**, the cyclic-collection block construction

\[
 \Phi\uplus(x+\Psi)\sim\Phi\uplus(-x+\Psi).
\]

Section3.2 gives **Formula3.5, p.127**,

\[
 \Phi\uplus(x+\Psi)\sim\Phi\uplus(x-\Psi),
\]

its block-reflection formulation. Section3.3, pp.132–135, discusses
partial pitch-class transposition by multiples of the cycle interval.
These are antecedents, not arbitrary-n six-note completeness proofs.
Crucially p.122, footnote2, explicitly says **“I cannot prove this claim”**
about the proposed remainder-set criteria. Their empirical criterion list
must not be used as an unqualified published proof. The manuscript's exact
group-ring conditions and self-contained soundness arguments remain the
mathematical justification for its stated endpoints.

## 4. Suggested manuscript wording and checked bibliography additions

Recommended B heading: **“B: the classical six-point family”**. Retain the
existing B identifier in the executable grammar and certificates. A name
change in prose should not alter the recorded construction.

Suggested introduction paragraph:

```latex
The generators themselves have substantial classical antecedents.
The exact two-parameter six-point formula and its signed factorization
appear as Family N in Yovanof--Golomb \cite[p.~47]{yg}.
The repeated-distance example at $(p,q)=(1,4)$ is attributed to
Hosemann and Bagchi (1954) in Lemke--Skiena--Smith
\cite[Table~1]{lss}.
Block translations against a cyclic collection appear in the
Callender--Hall handout \cite[Cases~3--4]{ch}, which credits Bullough
for Cases~4a/4b; Goyette gives both translation and reflection
formulations \cite[Formulas~3.2 and~3.5]{goyette}.
Here each generator has an explicit algebraic acceptance condition;
the completeness claim concerns their combination with the stated
finite certificates. Historical priority is not established.
```

Use direct citations only to read sources. The following bibliography
entries can be added to the same manuscript without promoting unread
originals to proof dependencies:

```latex
\bibitem{yg}
G.~S. Yovanof and S.~W. Golomb,
\emph{The Polynomial Model in the Study of Counterexamples to
S. Piccard's Theorem}, Ars Combinatoria \textbf{48} (1998), 43--63.
Family N, p.~47; endpoint product labels are interchanged relative
to the displayed factors.

\bibitem{lss}
P. Lemke, S.~S. Skiena and W.~D. Smith,
\emph{Reconstructing Sets From Interpoint Distances},
DIMACS Technical Report 2002-37 (2002).
Published in \emph{Discrete and Computational Geometry},
Springer (2003), 597--631.
The primary report was read; Table~1 supplies the qualified
Hosemann--Bagchi historical attribution.

\bibitem{ch}
C. Callender and R. Hall,
\emph{Crystallography and the structure of Z-related sets},
Society for Music Theory annual meeting, Nashville, Tennessee,
7 November 2008, conference handout.
Cases~3--4; the Bullough attribution is read through this handout.

\bibitem{goyette}
J. Goyette,
\emph{The Z-Relation in Theory and Practice},
Ph.D. thesis, University of Rochester (2012).
Chapter~3, especially Formulas~3.2 and~3.5; the proposed criteria
are explicitly empirical (p.~122, footnote~2).
```

Not proposed as direct proof citations: Hosemann–Bagchi1954,
Bullough1961, Yovanof1988 thesis, Bloom1977, Bloom–Golomb1977,
Soderberg1995. Their unread mathematical content stays **[LIT-VERIFY]**.
The note records historical credit through read sources and verifies
publisher metadata where available. It does not resolve earliest priority.

## 5. Focused search, reading and exact-check log

No duplicate broad novelty search was conducted. Required-venue passes
remain logged in `notes/2026-09-30-six-literature.md` and the two
`notes/2026-09-30-six-literature-second*.md` notes. This pass addresses
missing attribution only.

Exact queries:

```text
Hosemann Bagchi 1954 Acta Crystallographica 7 237 241 homometric structures
Goyette Z-relation in theory and practice 2012 thesis pdf
"Goyette" "The Z-Relation" Rochester thesis pdf
"On homometric structures" "pdf" Hosemann Bagchi
"On homometric sets. I" pdf Bullough
"Hosemann" "Bagchi" "0, 1, 2, 6"
Lemke Skiena Smith Reconstructing sets interpoint distances Table 1 Hosemann Bagchi pdf
"On homometric structures" "1954" "237" pdf
"On homometric sets. I. Some general theorems" pdf Bullough
```

Fetched primary Yovanof–Golomb, Callender–Hall, Goyette and official
DIMACS source URLs above. Local temporary reading copies are under
`/tmp/babbitt2-formal-credit/`; they are not added to the project.
Yovanof–Golomb is image-only: rendered printed pages43,44,46,47,48,62,63
were visually read. Other PDFs were text-extracted; the official DIMACS
PostScript was decompressed and rendered to PDF. No account, purchase or
outreach was attempted. IUCr source PDFs for1954/1961 returned401 and
remain inaccessible; access failure is not evidence that their formulas
are absent.

SHA256 of the read source bytes:

```text
yovanof-golomb.pdf 621e0f63509d545c88530f85a6788d7098d55033f42b4c53ca6965d15ad87f5a
callender-hall.pdf 0a74798fc2a932d3188973bf4fe84c48cea478d27e4e8a08898c1fc3064c6e2e
goyette.pdf cadb9a541e8ce46ee788db0a24dae57effa575150c5bd3297422f3424d9985e6
lss.ps 93e0075010c6109730023e7bf2921961853b1842d224d74cf7f3b64c4eaa2ecf
```

Only inexpensive exact comparisons were computed: dictionary convolution
of F,Q and the normalized reciprocal at p=1,q=6, and direct substitution
of p=1,q=4 into the endpoint lists. They reproduce the products and the
Table1 endpoints above. The comparison ran with `.venv/bin/python`;
no census, solver or experiment was launched by this attribution pass.

No other project file, manuscript, ledger, reference implementation or
concurrent review output was changed by this pass.
