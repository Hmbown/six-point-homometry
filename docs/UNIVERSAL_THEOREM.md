# A universal formulation of homometry

Date: 1 October 2026.

This note isolates the established mathematical core shared by the cyclic
set problem and ideal diffraction. It then states exactly what the
six-point generating theorem adds. The general equivalence is classical;
this exposition claims no historical originality. Its full elementary proof
received a separate adversarial read, with no correctness blocker found.
The accepted scope and limits are in [the review](UNIVERSAL_REVIEW.md).

## 1. The pure statement

Let \(G\) be any finite abelian group, written additively, and let
\(f,g:G\to\mathbb C\). Define convolution, involution and autocorrelation by

\[
(f*h)(t)=\sum_{x\in G}f(x)h(t-x),\qquad
f^*(t)=\overline{f(-t)},\qquad
C_f=f*f^*.
\]

For a character \(\chi:G\to S^1\), use the unnormalized transform

\[
\widehat f(\chi)=\sum_{x\in G}f(x)\overline{\chi(x)}.
\]

**Universal equivalence — established harmonic analysis.** The following
conditions are equivalent:

1. \(C_f=C_g\).
2. \(|\widehat f(\chi)|=|\widehat g(\chi)|\) for every character \(\chi\).
3. \(g=u*f\) for some \(u:G\to\mathbb C\) with \(u*u^*=\delta_0\).
4. Every translation-invariant pair functional agrees on \(f\) and \(g\):
   for every kernel \(K:G\to\mathbb C\),
   \[
   Q_K(f):=\sum_{x,y\in G}K(x-y)f(x)\overline{f(y)}
   =Q_K(g).
   \]

A function \(u\) in condition 3 is a **spectral unit**. Its Fourier
coefficients have modulus one. If \(f\) and \(g\) are real, \(u\) can be
chosen real.

In ordinary language: **two arrangements have the same autocorrelation
exactly when every pair measurement depending only on displacement agrees.
All such ambiguities are changes of Fourier phase.**

This statement holds for every group size and every support size. It
includes products of cyclic groups, with arbitrary complex weights, and
does not impose a six-point restriction.

## 2. Full proof, including zeros and real signals

Character orthogonality makes the Fourier transform invertible, with

\[
f(x)=|G|^{-1}\sum_{\chi\in\widehat G}
\widehat f(\chi)\chi(x).
\]

A change of variables in the convolution sum gives
\(\widehat{f*h}=\widehat f\,\widehat h\).
Changing \(x\) to \(-x\) also gives
\(\widehat{f^*}=\overline{\widehat f}\). Thus

\[
\widehat{C_f}(\chi)=|\widehat f(\chi)|^2.
\]

Invertibility proves \(1\Longleftrightarrow2\).

Assume condition 2. Define
\[
v(\chi)=
\begin{cases}
\widehat g(\chi)/\widehat f(\chi),&\widehat f(\chi)\ne0,\\
1,&\widehat f(\chi)=0.
\end{cases}
\]
The zero case also has \(\widehat g(\chi)=0\).
Every \(v(\chi)\) has modulus one. Let \(u\) be the inverse transform of
\(v\). Then
\(\widehat{u*u^*}=|v|^2=1=\widehat{\delta_0}\), so
\(u*u^*=\delta_0\), and
\(\widehat{u*f}=v\widehat f=\widehat g\).
This proves \(2\Longrightarrow3\).
Conversely, condition 3 implies
\(C_g=(u*u^*)*C_f=C_f\), proving \(3\Longrightarrow1\).
No division by a zero Fourier coefficient occurred.

For real \(f,g\), their transforms satisfy
\(\widehat f(\overline\chi)=\overline{\widehat f(\chi)}\), and similarly
for \(g\). The chosen ratios and the value 1 on zero bins have this same
symmetry. On a self-conjugate character the nonzero ratio is \(+1\) or
\(-1\). Consequently inverse Fourier transformation gives real \(u\).

Finally, grouping the pairs by their displacement yields
\[
Q_K(f)=\sum_{t\in G}K(t)C_f(t).
\]
Condition 1 implies 4. Conversely, choose each point-indicator kernel
\(K=1_{\{t\}}\); condition 4 recovers \(C_f(t)=C_g(t)\) for every \(t\).
This proves \(4\Longrightarrow1\) and completes the equivalence.

**[PROVED], in-house exposition of established identities.** The
spectral-unit part is presented in Mandereau et al. (2011),
§§2.2–2.4, with attribution to Rosenblatt. Bendory–Edidin (2020),
§5, states the phase-orbit formulation. The pair-functional statement
is the elementary linear consequence written above. None of these
statements is asserted to be a new discovery.

### Classical factorization is already universal in the cyclic case

Rosenblatt's *Phase retrieval* (1984), Theorem 3.6, pp.327–328,
already gives the following stronger algebraic description. For a
conjugation-closed field \(K\subseteq\mathbb C\) and any cyclic group
\(\mathbb Z_n\), homometric \(D,E\in K[\mathbb Z_n]\) have factors
\(P,Q\in K[\mathbb Z_n]\) such that
\[
D=\varepsilon_1\delta_{t_1}*P*Q,\qquad
E=\varepsilon_2\delta_{t_2}*P*Q^*,\qquad
\varepsilon_1,\varepsilon_2\in\{1,-1\}.
\]
Conversely these formulas preserve autocorrelation. The section's
hypotheses and the complete proof were read in the primary scan.
Choosing \(K=\mathbb Q\) includes binary sets, but the factors need
not be nonnegative, binary, sparse or unique. An unrestricted
all-modulus factor-flip characterization is therefore prior art.

Rosenblatt–Seymour (1982) is credited for the earlier torsion-free
factorization through Rosenblatt (1984), Theorem 2.4. The original 1982
publisher metadata and abstract were verified; its full proof was
inaccessible and was not read. The cyclic theorem above has its own
complete proof in the 1984 source. Neither attribution establishes
whether G's specific six-point structural grammar is historically new.

## 3. Where the difficult constructive theorem begins

Let
\[
\mathcal U(G)=\{u:G\to\mathbb C:u*u^*=\delta_0\}.
\]
For a binary arrangement \(1_A\), the set of all binary arrangements with
the same autocorrelation is exactly
\[
\{1_B:C_{1_B}=C_{1_A}\}
=
\{u*1_A:u\in\mathcal U(G)\}\cap\{0,1\}^{G}.
\]

Every binary member of this intersection automatically has \(|A|\)
occupied sites, since \(C_{1_A}(0)=|A|\). The displayed formula is exact,
but arbitrary phase choices usually produce nonbinary weights. It does
not supply a short list of admissible constructions, a practical
enumerator, or a unique normal form.

Our [six-point theorem G](../notes/2026-09-30-six-generation.md) claims
a finite explicit grammar that connects every such binary fibre for
\(G=\mathbb Z_n\) and \(|A|=6\), modulo translation and reflection,
for every \(n\). Every intermediate arrangement remains a six-point set.
Its contribution is therefore **constructive completeness within a
discrete constraint**, rather than the general lost-phase identity.

The proof uses integral signed-matching groups to handle arbitrary
moduli. That encoding extends to other cardinalities, but encoding
every possible matching alone is not a compressed structural solution.

**[OPEN research target, not a new conjecture or theorem].** Seek a
uniform, explicit structural description of the binary intersection
above for arbitrary cardinality and modulus. The target must specify
admissibility tests and prove completeness. Existence of a short
finite grammar, minimality, and an efficient algorithm are separate
questions; none follows from the universal equivalence or from G.

## 4. What “an algorithm of a crystal” can mean

Within a finite periodic grid model, \(f\) represents fixed scalar
scattering weights. With all character bins and a known common scale,
its ideal intensity data are \(|\widehat f|^2\), and their inverse transform
is the weighted displacement correlation. Thus the universal equivalence
describes exactly the information preserved by this measurement model.
A multidimensional finite grid uses a product of cyclic groups.

The quadratic functional result also applies to a chosen scalar
translation-invariant pair-interaction model. It concerns the energy of
the specified configurations. It does not establish stability under
deformations or equality of dynamics, vibrational spectra, electronic
states, or quantum many-body interactions.

A physical crystal can have continuous atomic positions, several species,
frequency-dependent scattering factors, disorder and incomplete
measurements. Those require their own models and hypotheses. The finite
theorem gives a clean model of structural ambiguity. Predicting which
crystal forms additionally requires interactions and formation dynamics.

## 5. How the supplied outside review changes the argument

The user supplied a report of separately implemented checks. The report
states agreement for six-point censuses and construction connectivity
at \(12\le n\le44\), the 135 incidence-minor bound, and direct Bloom
pair counts at \(6\le n\le120\). Its raw implementations and run logs
have not been inspected here; these are recorded as **reported checks**.

The reviewer used an independently formulated dyad-exchange menu. Its
exact correspondence to G's periodic-weight conditions was not separately
checked by the reported computation. The equivalence in Theorem D requires
the specified equal-sum parallelogram shape; it must not be presumed for
an arbitrary exchange menu.

The report did not verify the real-line solver encodings, the high-rank
reduction, or the entire low-rank DAG cover. Its bounded agreement does
not establish arbitrary-modulus completeness. Those branches remain the
main targets for an independent specialist.

There is already an exact standard-library checker for the 315-stratum
DAG cover, separate from its terminal-mechanism checker. A package-registry
block alone does not block those structural replays. The line branch
still has solver dependencies. A fresh replay should omit the DAG checker's
optional resume flag and use a new output directory; resumed records do not
recompute skipped predicates.

Referee-facing exposition should give each reduction a readable lemma,
state each checker's exact obligation, and distinguish soundness,
exhaustive coverage and specialization. G permits guarded operations and
thirteen fixed templates; it claims neither minimality nor a nonredundant
classification. These boundaries belong in the main theorem discussion.

## Sources

- J. Mandereau, D. Ghisi, E. Amiot, M. Andreatta and C. Agon,
  *Discrete phase retrieval in musical structures*, Journal of Mathematics
  and Music 5(2) (2011), 99–116,
  [DOI](https://doi.org/10.1080/17459737.2011.608820).
  Author preprint §§2.2–2.4 and their Fourier/spectral-unit arguments read.
- T. Bendory and D. Edidin,
  *Toward a mathematical theory of the crystallographic phase retrieval
  problem*, SIAM Journal on Mathematics of Data Science 2(3) (2020),
  809–839, [author version](https://arxiv.org/html/2002.10081v2).
  Relevant finite phase-orbit discussion is §5; model limits are §2.
- J. Rosenblatt, *Phase retrieval*, Communications in Mathematical
  Physics 95(3) (1984), 317–343,
  [primary scan](https://projecteuclid.org/journalArticle/Download?urlId=cmp%2F1103941578).
  Theorem 3.6 and proof, pp.327–328, read with the §3 field hypotheses;
  Theorem 2.4 is a primary restatement attributed to Rosenblatt–Seymour.
- Historical factorization antecedents, including the exact scope of
  Rosenblatt–Seymour, are recorded separately in
  [References and attribution](REFERENCES.md). The universal identities
  above do not establish historical priority for the six-point grammar.
