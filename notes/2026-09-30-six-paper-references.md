# Primary references for the six-note review manuscript

30 September 2026. Scoped bibliography and claim-support check for Theorem G.
The root agent handles the session tests, plan, ledgers and checkpoint. This note
adds no novelty claim and does not independently validate every proof in the cited
papers. **VERIFIED** below means the bibliographic record and the specified primary
sections were read in this pass; the source version and access limitations matter.

## 1. Rosenblatt 1984 — classification and spectral units

**Joseph Rosenblatt.** “Phase retrieval.” *Communications in Mathematical
Physics* **95**(3) (September 1984), 317–343.
DOI: [10.1007/BF01212402](https://doi.org/10.1007/BF01212402).
[Publisher record](https://link.springer.com/article/10.1007/BF01212402);
[original scan endpoint](https://projecteuclid.org/journalArticle/Download?urlId=cmp%2F1103941578).

**VERIFIED:** publisher record and publisher-deposited Crossref metadata; cached
original scan, MD5 `f55208635bbdfb62e7bed924d727e4dd`, matching the provenance
in `notes/lit_core.md`. Read §3, especially Theorem 3.1 and Proposition 3.3 with
their proofs (pp. 324–326), Theorem 3.9 (p. 329), Example 4.3(a) (p. 331), and
the appendix proof (pp. 336–341). Checked the title, Proposition 3.3, Theorem 3.9
and Example 4.3(a) against rendered scan pages.

**[PROVED-LIT] supports:** the two-type four-point circle/cyclic classification;
spectral-unit equivalence for finite abelian groups over the stated field;
an explicit uniform spectral unit for the parametric four-point family.
Theorem 3.9 is credited in the paper to joint work with **Joel Berman**; Berman
is not a bibliographic coauthor. It does not classify six-point cyclic sets.

**Access:** fresh Project Euclid and Springer PDF attempts returned HTML/bot
pages. The original was freshly read from its provenance-checked local copy.

## 2. Erickson–Jones v4 — five-point frontier

**William Q. Erickson and Nicholas B. Jones.** “Homometric subsets of
\(\mathbb Z_n\) with cardinality 5: classification and enumeration.”
[arXiv:2412.08997v4](https://arxiv.org/abs/2412.08997v4), 27 August 2026
(first submission 12 December 2024).
Repository DOI: [10.48550/arXiv.2412.08997](https://doi.org/10.48550/arXiv.2412.08997).

**VERIFIED:** current arXiv record, [primary HTML](https://arxiv.org/html/2412.08997v4)
and [v4 PDF](https://arxiv.org/pdf/2412.08997v4). Read the abstract and §1,
Theorem 4.1 and its discretization proof, Theorem 4.4 and proof, and §5,
especially Problem 5.2 (PDF pp. 21–22, 25–27). The full §3 classification proof
was not re-audited in this pass.

**[PROVED-LIT] supports:** the seven five-point types, comprising six pair
families and one triple family, modulo shifts/reflections, and their generating
function. **[OPEN, as posed by these authors]** §5 still asks for the extension
to weights at least six. That establishes their stated scope, not our priority.

**Metadata only:** Crossref now records *Discrete Mathematics* **350**(1),
January **2027**, article 115400,
[10.1016/j.disc.2026.115400](https://doi.org/10.1016/j.disc.2026.115400).
Publisher full text was inaccessible. Cite the version actually read, v4, when
using its section numbers; do not silently substitute the unread journal version.

## 3. Postpischil–Gilbert 1994 — classical line family and symbolic search

**Eric Postpischil and Peter Gilbert.** “There Are No New Homometric Golomb
Ruler Pairs with 12 Marks or Less.” *Experimental Mathematics* **3**(2)
(1994), 147–152.
DOI: [10.1080/10586458.1994.10504286](https://doi.org/10.1080/10586458.1994.10504286).
[Primary journal scan on EMIS](https://emis.de/ft/52010).

**VERIFIED:** entire six-page primary scan, particularly §2 definitions,
§3 family/result, §§4–6 symbolic matching algorithm and search, §7 planar
projection construction; publisher-deposited metadata confirms author order,
title, volume, issue, pages and DOI. The scan records receipt 10 June 1993 and
acceptance in revised form 15 September 1994. Use year 1994; Crossref's coarse
January field should not be treated as a precise publication day.

**[PROVED-LIT, computer-assisted] supports:** the classical two-parameter
six-mark family and its completeness among the paper's Golomb-ruler pairs with
at most twelve marks, including nonexistence for seven through twelve; symbolic
linear constraints and a geometric projection explanation. **Golomb-ruler scope
requires distinct distances.** This does not establish completeness for repeated
distances, multisets, or cyclic six-point homometry.

**Access:** EMIS download succeeded directly; its browser-text fetch failed.
The publisher page returned HTTP 403; no missing proof is being filled by a snippet.

## 4. Jedrzejewski–Johnson 2013 — constructions and finite enumeration

**Franck Jedrzejewski and Tom Johnson.** “The Structure of Z-Related Sets.”
In Jason Yust, Jonathan Wild and John Ashley Burgoyne (eds.), *Mathematics
and Computation in Music*, MCM 2013, Lecture Notes in Computer Science
**7937**, Springer, Berlin/Heidelberg (2013), 128–137.
DOI: [10.1007/978-3-642-39357-0_10](https://doi.org/10.1007/978-3-642-39357-0_10).
[Publisher record](https://link.springer.com/chapter/10.1007/978-3-642-39357-0_10);
[author preprint](https://arxiv.org/abs/1304.6608v1), 23 April 2013.

**VERIFIED:** publisher bibliographic record and complete nine-page
[arXiv PDF](https://arxiv.org/pdf/1304.6608v1), §§1–5. This pass read the author
version, not the subscription chapter.

**[PROVED-LIT] supports:** the construction discussion in §2, including
complementation, unit multiplication and periodic replication. **[COMPUTED,
source-reported]** §3 gives finite enumeration tables. Its §2 explicitly leaves
classification from cardinality five onward open in 2013. It supplies neither
arbitrary-n six-point completeness nor priority evidence for Theorem G.

The manuscript need not rely on the broad group-action assertion in §4; this
pass did not independently validate it. Avoid importing the paper's “first
quadruple” assertion, already contradicted in this repository's literature audit.

## 5. Mandereau et al. 2011a — homometry, quotient transport, complement

**John Mandereau, Daniele Ghisi, Emmanuel Amiot, Moreno Andreatta and
Carlos Agon.** “Z-relation and homometry in musical distributions.”
*Journal of Mathematics and Music* **5**(2) (2011), 83–98.
DOI: [10.1080/17459737.2011.608819](https://doi.org/10.1080/17459737.2011.608819).
[Publisher record](https://www.tandfonline.com/doi/full/10.1080/17459737.2011.608819);
[IRCAM author preprint](http://articles.ircam.fr/textes/Mandereau11a/index.pdf).

**VERIFIED:** publisher record and deposited metadata; author preprint §§3–4
(preprint pp. 7–11), §6 (pp. 12–14), §7.1 (pp. 14–15), with proofs. Publisher
record gives online publication **15 September 2011**; deposited issue date is
July 2011. Final typeset theorem numbering was not checked.

**[PROVED-LIT] supports:** the interval-content/Patterson-function connection;
quotient transport of homometry (Theorem 6.1, Corollary 6.2); an integer
six-point example reduced modulo n (Example 6.3); generalized complementation
(Lemma 7.1, Theorem 7.2). Quotients can merge points, and nontriviality need
not survive (Example 6.4). The paper does **not** supply the spectral-unit
characterization; cite Rosenblatt for that result.

**Access:** the direct HTTP IRCAM download succeeded; the web tool's HTTPS
fetch timed out. Read version is the author preprint, not final journal layout.

## 6. Mandereau et al. 2011b — phase-retrieval interpretation

**John Mandereau, Daniele Ghisi, Emmanuel Amiot, Moreno Andreatta and
Carlos Agon.** “Discrete phase retrieval in musical structures.”
*Journal of Mathematics and Music* **5**(2) (2011), 99–116.
DOI: [10.1080/17459737.2011.608820](https://doi.org/10.1080/17459737.2011.608820).
[Publisher endpoint](https://www.tandfonline.com/doi/full/10.1080/17459737.2011.608820);
[IRCAM author preprint](http://articles.ircam.fr/textes/Mandereau11b/index.pdf).

**VERIFIED:** deposited publisher metadata and author preprint §§2.2–2.4
(pp. 4–8), §2.5 (pp. 8–9), §5 (pp. 18–19). The preprint has a **25 July 2011**
template timestamp; this is not a publication date. Deposited issue date is
July 2011; exact online day was not independently checked here.

**[PROVED-LIT] supports:** circulant/Fourier formulations; the spectral-unit
interpretation, explicitly attributed to Rosenblatt in §2.3; the caveat that a
spectral unit need not produce a binary set; existence of nontrivial Z-pairs
exactly for n=8,10 or n≥12 (Theorem 2.10). §5 records a then-open constructive
characterization problem. It does not classify all cyclic six-point pairs.

**Access:** author preprint downloaded directly from IRCAM; publisher full text
failed. Do not cite Theorem 2.11's general linear-group assertion as an additional
axiom on this reading; no independent proof audit was performed here.

## Recommended manuscript use

Use Rosenblatt for four-point classification and spectral units, Erickson–Jones
v4 for the five-point classification and its stated higher-cardinality frontier,
and Postpischil–Gilbert to credit the classical line family and symbolic interval
matching. Use 2011a for quotient shadows and complementation, 2011b for the
phase-retrieval language and its binary-output limitation. Jedrzejewski–Johnson
provides useful construction/enumeration context. These six entries can form a
compact bibliography; none proves that the present theorem is historically new.

The primary comparisons still missing from the broader novelty audit remain
those named in `2026-09-30-six-literature-second.md`: Patterson and Bullough full
text, Soderberg, Zhao's full chapters/articles, remaining Goyette sections, and
integer-classification literature. No source outside the six entries above was
promoted to a verified mathematical dependency by this pass.

## Retrieval and reading audit

Primary online queries included Rosenblatt/Phase retrieval/1984/PDF;
Postpischil/Gilbert/homometric/1994 and exact title/DOI; the two 2011 titles with
IRCAM/PDF; Jedrzejewski/Johnson/2013/title/DOI. Metadata was refreshed from
`https://api.crossref.org/works/<DOI>` for all six journal/chapter records,
including the registered Erickson–Jones journal DOI. Some simultaneous requests
returned HTTP 429; sequential retries succeeded. arXiv metadata supplied the
version dates. Publisher records and author/journal originals supplied the
mathematical scope. Search snippets were used only to locate these originals.

Temporary downloads/extractions were kept outside the repository in
`/var/folders/gc/lw1tgpk97z51d30mcvbhyb400000gn/T/six-paper-primary-ftsnnno5/`.
The PDF skill was used: `pdftotext -layout`, with `pdftoppm` page rendering for
the Rosenblatt scan. Original local scan path:
`/private/tmp/claude-501/-Volumes-VIXinSSD-babbitt2/a1bb2e1f-a833-49d8-9ba3-3146db00dab4/scratchpad/lit/ros.pdf`.
No protected reference, data file or existing ledger was changed.

Download SHA-256 values (provenance only, not completeness certificates):

| Source | SHA-256 |
|---|---|
| EJ v4 PDF | `bedc040f270b1a3afbeb533c3fe2afe4a3a065d351b46910a7089aa444eabf04` |
| Postpischil–Gilbert scan | `e9d7cb927f3bcd41a07eeb59252fb8df6bafdc930fe7eafc17679cb977a7637b` |
| Jedrzejewski–Johnson v1 PDF | `e11b726ed8ba7ed80621ae77041689dd2ba78a8cbd099bd178123b803b518ab8` |
| MGAAA 2011a preprint | `9a30209237924cee55d5358e8d300996c746d1bcd8a21c81af7ddd1d0d529204` |
| MGAAA 2011b preprint | `f81b4d6f3e438202a2e4932a14e48c001f07655802aacd868cfb265336d53c98` |

## Final manuscript bibliography and scope verdict

30 September 2026, final read-only check of
`notes/2026-09-30-six-paper.tex`.
**VERDICT: ACCEPTED for bibliographic accuracy and the cited scopes; no required
reference correction remains.** This is not an independent whole-proof or
historical-priority verdict.

Checked source SHA-256:
`54f44fe0b0b9a51c16414b6503e8e87b1ba7baf13acab539566b45cd2b1cc02e`.
The live source hash exactly matched the root agent's proposed final hash.

All six final entries have the verified authors, titles, years, pages and
applicable DOIs/version details. The Postpischil–Gilbert initials and title are
now corrected. The JJ entry gives the published chapter metadata while stating
the author version was read. The EJ entry remains tied to the v4 text. The two
2011 articles are distinguished, with 2011a cited for transport.

The introduction's four-point/Berman attribution and five-point/triple wording
match the originals. Its collective construction/enumeration citations are
supported by JJ's §§2–3 and the 2011b background. The classical line-family
citation retains the Golomb-ruler limitation in the bibliography. The
homomorphic-transport paragraph cites 2011a and separately explains admissibility
and degeneration; it does not assume nontriviality always survives a quotient.
No cited claim promotes an unread journal version or an unrestricted six-point
completeness theorem from these references. No new search was performed for
this final check, and the existing novelty limitation remains unchanged.
