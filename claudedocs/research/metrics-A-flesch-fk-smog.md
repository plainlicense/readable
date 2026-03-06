<!--
SPDX-FileCopyrightText: 2026 PlainLicense

SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT
-->

# Research Report: Flesch Reading Ease, Flesch-Kincaid Grade Level, and SMOG Index

**Prepared for:** Readable library documentation project
**Date:** 2026-03-05
**Status:** Research draft — not the final user-facing documentation
**Scope:** History, formula mechanics, strengths, weaknesses, use cases, and comparative analysis

---

## Table of Contents

1. [Flesch Reading Ease](#1-flesch-reading-ease)
2. [Flesch-Kincaid Grade Level](#2-flesch-kincaid-grade-level)
3. [SMOG Index](#3-smog-index)
4. [Comparative Analysis](#4-comparative-analysis)
5. [References](#5-references)

---

## 1. Flesch Reading Ease

### 1.1 Background and History

Rudolf Flesch (1911–1986) was an Austrian-born lawyer who fled Nazi persecution in 1938 and built his second career in the United States as a writing consultant, readability researcher, and Plain English advocate. After arriving as a refugee with a Viennese law degree that was not recognized in the US, he worked in a book manufacturing shipping department before earning scholarships to Columbia University. He received a BA in library science (1940), an MA in adult education (1942), and a PhD in educational research (1943), where his dissertation was titled "Marks of a Readable Style."

Flesch's 1943 dissertation introduced his first readability formula, which included affixes (prefixes and suffixes per 100 words) and "personal references" (personal pronouns and named individuals). Publishers discovered the formula could increase readership by 40–60 percent (DuBay, 2004). This brought Flesch considerable attention as a communications consultant.

In 1948, Flesch published a substantially revised formula in the *Journal of Applied Psychology* under the title "A New Readability Yardstick" (Flesch, 1948). He dropped affixes and personal references and reduced the formula to two variables: sentence length (average words per sentence) and word length (average syllables per word). This simplification was partly a practical concession — syllable counting was faster than counting affixes — and partly an empirical one: his data showed that the two-variable formula correlated above .90 with his earlier model while being far easier to apply (DuBay, 2004).

The 1948 formula was normed against 350 passages from the McCall-Crabbs Standard Test Lessons in Reading (McCall & Crabbs, 1925, 1950, 1961). These passages were originally written in the 1920s for schoolchildren in grades 3 through 12. The implications of this norming choice are discussed in the weaknesses section.

Flesch worked extensively with the Associated Press in the 1940s. His consulting helped reduce the average reading level of AP front-page news stories by roughly five grade levels, with measurable gains in readership (DuBay, 2004). The US Department of Defense subsequently adopted the Flesch Reading Ease formula as a standard, and it remains embedded in widely-used software — including Microsoft Word, which has offered a built-in Flesch score since the early 1990s. Pennsylvania was the first US state to use Flesch-derived metrics for legal requirements on insurance policy readability.

### 1.2 The Formula Explained

The Flesch Reading Ease Score (FRES) is:

```
FRES = 206.835 - (1.015 × ASL) - (84.6 × ASW)
```

where:
- **ASL** = average sentence length (total words ÷ total sentences)
- **ASW** = average number of syllables per word (total syllables ÷ total words)

**The constants explained:**

- **206.835** is the maximum intercept — the baseline score before any penalties for word and sentence length. It was derived empirically from regression analysis against the McCall-Crabbs comprehension data.
- **1.015** penalizes each additional word per sentence (on average). Its relative smallness reflects that sentence length, while important, carries less weight than word length in this formula.
- **84.6** penalizes each additional syllable per word (on average). This coefficient is 83 times larger than the sentence-length coefficient, which means the formula is heavily weighted toward word complexity — a deliberate design choice reflecting Flesch's view that vocabulary difficulty was the dominant driver of reading difficulty.

**What the output means:**

The formula is designed to produce a score from 0 to 100, where higher scores indicate easier reading. In practice, scores can go below 0 or above 100 for extreme texts — this is a known artifact of the linear regression design, not an error in implementation. A sentence from Moby Dick scored −146.77 by Amazon's implementation; a Proust sentence in translation scored −515.1 (Wikipedia, Flesch-Kincaid readability tests). Conversely, children's texts with very short monosyllabic words can exceed 100.

| Score | Reading Level | Typical Audience |
|-------|--------------|-----------------|
| 90–100 | Very easy | 5th grade; average 11-year-old |
| 80–90 | Easy | 6th grade |
| 70–80 | Fairly easy | 7th grade |
| 60–70 | Standard | 8th–9th grade |
| 50–60 | Fairly difficult | 10th–12th grade |
| 30–50 | Difficult | College level |
| 0–30 | Very confusing | College graduate |

These bands were calibrated against McCall-Crabbs data and should be treated as approximate. The formula was originally calibrated so that a score of 60–70 corresponded to "plain English" appropriate for general adult audiences, though what counted as "general adult" was measured against a specific American population in the 1940s.

**Why syllables and sentence length?**

Flesch's theoretical rationale was straightforward: longer words require more decoding effort because readers encounter them less frequently, and longer sentences impose greater working memory demands. Both are proxies — syllable count stands in for vocabulary familiarity and word frequency; sentence length stands in for syntactic complexity. The proxies are imperfect, as discussed in Section 1.4, but they are computationally tractable and correlate reasonably with comprehension outcomes in many (though not all) study populations.

### 1.3 Strengths

**Validated correlation with comprehension:** In Klare's (1976) comprehensive review, 39 of 65 studies showed a positive correlation between Flesch-derived formula estimates and reader performance. The formula correlates approximately 0.91 with comprehension as measured by standardized reading tests when applied to materials similar to those it was normed on (DuBay, 2004; Lumen Learning, Technical Writing).

**Established and widely adopted:** The formula has been in continuous use since 1948 across government agencies, the US military, insurance regulation, educational publishing, journalism, and plain language advocacy. This institutional footprint means the score is interpretable by many practitioners who have experience with its typical ranges. Microsoft Word's inclusion of the score from the early 1990s onward gave it ubiquity no other formula matches.

**Sensitive to both variables simultaneously:** Because the formula includes both sentence length and syllable count with explicit weights, it captures the combined effect of complex vocabulary and long sentences. A text with short simple sentences but polysyllabic technical words will score differently from a text with long compound sentences containing only monosyllabic words. This two-dimensional sensitivity is an advantage over formulas that focus on a single variable.

**Works well for general-purpose prose:** Flesch RE performs reasonably for newspaper articles, magazine writing, business correspondence, government documents, and general-audience books — text types similar to its norming corpus. For these domains, it is a reliable quick screening tool.

**Reversible design:** Because the formula's direction is intuitive (higher = easier), it is easier for writers to use as a feedback tool than formulas producing grade levels (where the direction of the goal varies by context).

**Appropriate for automated pipelines:** The formula requires only three counts (words, sentences, syllables), all of which are computationally tractable without large lookup tables or external word lists.

### 1.4 Weaknesses and Biases

**Syllable count is an imperfect proxy for word difficulty.** The central assumption is that words with more syllables are harder to understand. This fails in two symmetrical ways:

1. *Short but unfamiliar words score as "easy."* Medical jargon (e.g., "gout," "stat," "prion," "sepsis") and technical terms (e.g., "flux," "torque," "byte") are monosyllabic and score very low on the syllable penalty, but they may be completely opaque to lay readers. A text using a sentence like "The patient presented with acute MI" would score as relatively easy despite being incomprehensible to many general readers.

2. *Long but familiar words score as "hard."* Words like "understanding," "communication," "information," and "neighborhood" are polysyllabic but extremely common and well understood by most adult readers. They incur a heavy penalty that may not reflect actual comprehension difficulty.

This limitation is particularly acute in technical, scientific, and medical writing, where specialized vocabulary with short, unfamiliar terms coexists with common long words. (Paasche-Orlow et al., 2003, cited in PMC3049622; UXMatters, 2019)

**Cannot detect semantic difficulty.** The formula is "blind to meaning" (Redish, 2000). A nonsense sentence constructed from short words scores as very easy. A technically accurate paragraph about a familiar topic that uses precise but long scientific words may score as difficult even if the content is clear to the target audience. As Flesch himself acknowledged, the formula "will not indicate whether the ideas expressed are nonsense" (Lockman, 1957, cited in Bethel University thesis).

**Normed on outdated, limited passages.** The McCall-Crabbs Standard Test Lessons (1920s–1960s) were the basis for formula calibration. Multiple problems have been identified with this choice: the passages were intended only as reading practice exercises, not as comprehension measures; William A. McCall himself later stated that whatever data was used to assign grade placements had not been extensive nor evaluated for reliability; and he was apparently unaware the passages were being used for formula validation (Cunningham, Hiebert, & Mesmer, 2018; Stevens, 1980). The 350 passages are narrow in topic, historical in vocabulary, and specific to a US schooling context from the early 20th century. (Cunningham et al., 2018; PMC10027808)

**English-only.** The formula's constants were derived from English text. Other languages have different morphological structures — German compounds, Finnish agglutination, Chinese monosyllabic characters — that make syllable count a meaningless or misleading measure of word complexity. Even for non-American English dialects, the grade-level bands require recalibration.

**Can be gamed.** Because the formula only measures averages, writers can improve scores mechanically by shortening sentences (even into fragments) and replacing polysyllabic words with shorter synonyms — without necessarily improving actual comprehension. Armbruster et al. (1985), Davison and Kantor (1982), and Charrow and Charrow (1979) have all demonstrated that such manipulations change formula scores without improving measured comprehension. In some cases, breaking complex information into shorter sentences increases cognitive load by removing connective tissue (Redish, 2000).

**Ignores everything else.** Layout, typography, heading structure, images, prior knowledge, reading purpose, and the reader's motivation are all ignored. A score of 60 for a beautifully designed user manual and a score of 60 for dense bureaucratic prose with no paragraph breaks are equivalent to the formula, but they would test very differently with actual readers. (Klare, 1976; Redish, 2000)

**Sample sensitivity.** The score depends on which sample is analyzed. Different excerpts from the same document can produce substantially different scores. For short texts (under 100 words), the score is particularly unreliable.

**Score bands are arbitrary.** The 10-point grade bands were not independently validated against reader performance. They are best understood as rough order-of-magnitude descriptors, not precise reading level assignments.

### 1.5 Best Use Cases

- **General-purpose prose screening:** Quickly checking whether business correspondence, government documents, web content, or journalism is broadly accessible to adult readers.
- **Revision feedback loop:** During writing and editing, where relative score changes (not absolute values) are informative. If a score improves from 45 to 62, that directional change is meaningful even if the absolute values are imprecise.
- **Regulatory compliance:** Insurance policies, legal documents, and certain US government communications have statutory requirements tied to Flesch scores. If compliance is the goal, Flesch is the appropriate tool.
- **Comparative analysis of similar documents:** When comparing readability across a corpus of documents in the same domain, relative rankings are more reliable than absolute scores.
- **Plain language advocacy:** As a tool to encourage writers to notice sentence length and word choice, even if they don't treat the score as gospel.

### 1.6 What It Is NOT Good For

- **Medical and health education materials:** Flesch RE consistently underestimates the reading difficulty of health content because short medical terms (jargon) are not penalized. Healthcare researchers and the National Cancer Institute generally prefer SMOG for this domain.
- **Technical documentation:** Same problem as healthcare — specialized short terms score as "easy" when they are anything but.
- **Legal text:** Legal writing has a specific structure (definitions, conditional clauses, enumerated items) that the formula cannot evaluate meaningfully. A well-structured legal document may score as "difficult" while being genuinely accessible to its intended audience; conversely, poorly organized legal prose may score as "standard" while being incomprehensible.
- **Poetry and creative prose:** The formula penalizes literary devices (long sentences, rich vocabulary) that are central to artistic effectiveness. Literary prose that scores poorly by Flesch may be perfectly accessible to its intended readers.
- **Short texts:** Fewer than ~100 words produces unstable scores.
- **Non-English text:** Do not apply to texts in any language other than English.
- **Evaluating text simplification:** A 2021 ACL paper demonstrated that FK (which shares Flesch's variables) is not a valid metric for evaluating whether text simplification is successful, because it can be satisfied by manipulations that do not improve actual comprehension (ACL Anthology, 2021).

---

## 2. Flesch-Kincaid Grade Level

### 2.1 Background and History

The Flesch-Kincaid Grade Level formula was developed in 1975 under a US Navy contract (contract number N61339-74-D-0082) by a team led by J. Peter Kincaid of Georgia Southern College, with co-authors Lieutenant Robert P. Fishburne Jr. (MSC, USNR), Richard L. Rogers, and Brad S. Chissom — all affiliated with either Georgia Southern College or the Naval Air Station Memphis.

The work was published as "Research Branch Report 8-75" in February 1975, formally titled "Derivation of New Readability Formulas (Automated Readability Index, Fog Count and Flesch Reading Ease Formula) for Navy Enlisted Personnel" (Kincaid et al., 1975). The report is publicly available through the Defense Technical Information Center (DTIC document ADA006655) and has been archived at the University of Central Florida's STARS repository.

**Why the Navy commissioned the work:** The US military was a large consumer of technical manuals, rate training materials (for enlisted specialties), and operational documents. The existing Flesch Reading Ease score produced a 0–100 number that required a separate lookup table to interpret in terms of reading level — a friction point in operational use. The Navy wanted a formula that directly produced a US school grade level, which would be immediately interpretable by trainers, curriculum designers, and educators without a conversion table.

**The norming data:** The formula was derived from reading comprehension tests of 531 Navy enlisted personnel enrolled in four technical training schools at two bases: Naval Air Station Memphis and Great Lakes Navy Training Center. Personnel were tested using the reading comprehension section of the Gates-McGinitie Reading Test, plus comprehension of 18 passages from Rate Training Manuals. Regression analysis produced the grade-level formula calibrated to this specific population reading this specific type of material.

The formula uses the same two inputs as Flesch Reading Ease (ASL and ASW) but applies different weights derived from this Navy-specific dataset. The Army adopted it as a readability standard for technical publications in 1978, and it subsequently became a US Military Standard. Many US states now require insurance policies and other legal documents to comply with Flesch-Kincaid grade level limits (typically grade 9 or lower), and Pennsylvania was the first to implement such a requirement.

### 2.2 The Formula Explained

```
FK Grade Level = 0.39 × ASL + 11.8 × ASW - 15.59
```

where:
- **ASL** = average sentence length (total words ÷ total sentences)
- **ASW** = average syllables per word (total syllables ÷ total words)

**The constants explained:**

- **0.39** is the sentence-length coefficient. Compared to Flesch RE (where ASL coefficient is 1.015), this is a smaller penalty per word per sentence — but because the grade formula is additive rather than subtractive, longer sentences push the grade level up.
- **11.8** is the syllable coefficient. This is a large positive weight: each additional syllable per word raises the grade level by 11.8 grade units (after accounting for the baseline). Words averaging 1.5 syllables each produce a higher grade level than words averaging 1.3 syllables each.
- **-15.59** is the intercept correction to scale the output to US grade levels. Without this correction, the raw score would not align with the 1–12+ grade level system.

**The output** is a number corresponding to a US school grade level. A score of 8.0 means the text is expected to be comprehensible to an 8th-grade reader. There is no upper bound: extremely complex text with very long sentences and polysyllabic words can produce grade levels in the hundreds if constructed pathologically (the formula has no ceiling). The practical range for real text is approximately -3 to 18+.

**Relationship to Flesch RE:** Both formulas use ASL and ASW as inputs, but the weighting factors differ substantially, and the direction of the scale is opposite (higher Flesch RE = easier; higher FK Grade = harder). The two formulas are not directly convertible to each other. The relative weight of sentence length vs. syllable count also differs: FK Grade weights sentence length slightly more relative to syllables compared to Flesch RE.

### 2.3 Strengths

**Immediately interpretable output.** A grade level is more actionable for most practitioners than a 0–100 score. Teachers, curriculum designers, publishers, and plain language writers understand what "grade 8" means without a lookup table. This interpretability was the primary motivation for the formula's creation.

**Widely validated.** As a direct transformation of the same inputs as Flesch RE, FK Grade Level inherits most of Flesch's empirical validation record. It correlates approximately 0.91 with comprehension as measured by standardized tests in appropriate populations (DuBay, 2004; Lumen Learning). It is "the most commonly used formula" for English-language readability in educational and healthcare contexts (PMC3049622).

**Institutional acceptance.** US Military Standard, IRS, Social Security Administration, many state insurance codes, and countless institutional readability policies specify FK Grade Level. Where compliance with a standard is required, FK is frequently the specified metric.

**Widely available in software.** Microsoft Word, Google Docs, and many writing assistance tools include FK Grade Level. This makes it accessible without specialized software for any practitioner.

**Good for general-audience calibration.** For general-purpose prose — news, government documents, web content — FK Grade Level is a reliable screening tool for checking whether text is broadly within range for a target audience.

### 2.4 Weaknesses and Biases

FK Grade Level shares all of Flesch RE's structural weaknesses (syllable count as a proxy for word difficulty, inability to detect semantic difficulty, gameable by mechanical sentence-shortening, English-only, ignores layout and context). In addition, it has some specific problems:

**Narrow norming population.** The formula was derived from 531 Navy enlisted personnel — a specific demographic (predominantly young, American, male, military-affiliated, reading Navy technical materials in 1975). This is not a representative sample of the general population, and the 18 test passages were from Rate Training Manuals, not from the wide range of documents the formula is now applied to. The generalizability of a formula normed on such a narrow corpus is, as one review put it, "suspect" (PMC10027808).

**Systematically underestimates reading difficulty of medical and technical content.** Multiple studies have found that FK Grade Level scores are 2–3 grade levels below SMOG scores for the same health education materials. The Centers for Medicare & Medicaid Services has explicitly warned that "Flesch-Kincaid scores tend to underestimate actual reading grade level because they are often several grade levels below results obtained using other measurements" (PMC5764592). For a 148-document study, SMOG produced a mean of 9.6 while FK produced a mean of 6.5 (PMC5764592). This isn't necessarily a flaw in the formula per se — it's a consequence of different comprehension targets (see Section 4) — but practitioners need to understand the discrepancy.

**Short medical jargon is invisible to the formula.** A text containing "The echocardiogram revealed aortic stenosis with a low ejection fraction" would score relatively well because several key medical terms are short (stenosis = 3 syllables; ejection = 3 syllables). However, the formula treats those terms identically to common 3-syllable words like "beautiful" or "tomorrow." The formula cannot distinguish familiar polysyllabic words from specialized ones.

**No upper bound.** The grade level formula has no ceiling. Single extremely long sentences can produce absurdly high grade levels; pathological input (very long words) can produce grade levels in the hundreds. This is not a failure of implementation — it is a mathematical property of the formula — but it creates challenges for automated quality checks.

**Sentence structure is invisible.** Two sentences of the same length — one with parallel structure and clear logic, one with tangled subordinate clauses — score identically. The formula cannot detect syntactic complexity beyond raw word count per sentence.

**Historical shift in baseline.** The formula was calibrated to 1975 US educational standards and test norms. Average reading levels in the US have shifted since then, and grade-level expectations vary by context, region, and educational system. A grade 8 score does not mean a contemporary 8th grader will understand the text — it means the text has the average statistical properties of text that was comprehensible to people tested at an 8th-grade level under 1975 Navy norming conditions.

### 2.5 Best Use Cases

- **Educational publishing:** Matching books and instructional materials to grade-level expectations. Publishers and librarians are accustomed to grade levels as a sorting mechanism.
- **Government and regulatory compliance:** When a statute or policy requires a specific FK grade level (most commonly grade 9 for insurance policies), the formula is the specified measurement.
- **Technical documentation for defined audiences:** When you know your audience's approximate education level (e.g., "high school graduate" = grade 12), FK provides a usable benchmark.
- **Broad screening in content pipelines:** Automated detection of grossly inappropriate reading levels in document sets, where precision is less important than identifying obvious outliers.
- **Tracking editorial progress:** As a directional metric during revision, particularly when targeting a general audience.

### 2.6 What It Is NOT Good For

- **Health and patient education materials:** Healthcare researchers and organizations (National Cancer Institute, CMS) consistently recommend SMOG over FK for medical materials, because FK underestimates difficulty by 2–3 grade levels in this domain.
- **Technical documentation for mixed audiences:** Cannot detect unfamiliar technical jargon; may rate impenetrable technical prose as "accessible."
- **Legal and regulatory documents:** Same limitations as Flesch RE. Compliance monitoring may be required, but the score does not reliably reflect comprehension.
- **Short texts:** Unstable for fewer than ~150 words.
- **Cross-formula comparison without calibration:** FK grades cannot be directly compared to SMOG grades, Dale-Chall grades, or Gunning Fog grades because each formula uses different assumptions about what "comprehension" means (see Section 4).
- **Any non-English text.**

---

## 3. SMOG Index

### 3.1 Background and History

G. Harry McLaughlin was an Associate Professor of Communications in the School of Journalism at Syracuse University. He held a PhD in psycholinguistics from University College London and had previously taught at The City University in London and York University (McLaughlin, 1969). The SMOG formula was published in 1969 in the *Journal of Reading* (now published by the International Literacy Association, formerly the International Reading Association) in an article titled "SMOG Grading — A New Readability Formula."

The name "SMOG" was chosen deliberately on multiple levels. It is an acronym for Simple Measure of Gobbledygook — directly targeting the kind of dense, pretentious, or bureaucratic language the formula was designed to identify. McLaughlin also chose it as a homage to Robert Gunning's FOG Index (Gunning Fog), which the formula was designed to improve upon. There may be a personal element as well: McLaughlin was British, and London's catastrophic "Great Smog" of 1952 was still in living memory. The use of weather metaphors (fog, smog) to describe unclear writing had a pointed self-awareness.

When McLaughlin first circulated an earlier version of the paper, a statistician who reviewed it assumed it was a joke. The formula was, in McLaughlin's own words, "laughably simple" — he meant this as a compliment, arguing that a formula's value should not depend on its complexity (readable.com/readability/smog-index).

**The mathematical insight behind SMOG:** McLaughlin recognized that in any fixed number of sentences, the count of polysyllabic words simultaneously captures both sentence length and word complexity, because:
- For any average number of syllables per word, a longer sentence contains more words and thus more chances for a polysyllabic word to appear.
- For any given sentence length, more polysyllabic words per sentence reflects harder vocabulary.

Therefore, counting polysyllabic words in a fixed sample of 30 sentences effectively multiplies word complexity by sentence length without requiring separate calculations. This insight allowed McLaughlin to eliminate multiplication from the manual calculation entirely, which he considered a significant practical improvement over Flesch's method. He calculated that SMOG grading on a 600-word sample (about 30 sentences) took approximately 9 minutes — comparable to the time required to run the Dale-Chall formula on a 100-word sample (McLaughlin, 1969).

**Norming:** McLaughlin validated his formula against 390 passages from the 1961 edition of the McCall-Crabbs Standard Test Lessons in Reading. (This is the same criterion corpus used by Flesch, which carries the same caveats about the quality of that norming data — see Section 1.4.)

**Subsequent refinement:** McLaughlin's original formula used `SMOG Grade = 3 + √(polysyllable count)` with the assumption of exactly 30 sentences. The modern refined version is:

```
SMOG Grade = 1.0430 × √(polysyllabic words × (30 / sentence count)) + 3.1291
```

The refined constant 3.1291 (replacing the original +3) and the scaling factor 1.0430 improve accuracy for texts of varying lengths and increase precision by less than 0.2 grade levels compared to the original. For texts of exactly 30 sentences, the two versions produce nearly identical results.

### 3.2 The Formula Explained

**Original (simplified) form:**
```
SMOG Grade = 3 + √(count of polysyllabic words in exactly 30 sentences)
```

**Modern form for variable text lengths:**
```
SMOG Grade = 1.0430 × √(polysyllabic words × (30 / sentence count)) + 3.1291
```

where "polysyllabic words" = words with three or more syllables.

**How to apply the original method:**
1. Count 10 consecutive sentences near the beginning, 10 in the middle, and 10 near the end (30 total).
2. Count every word with three or more syllables in those 30 sentences; count repetitions.
3. Take the square root of that count (or the nearest perfect square for manual estimation).
4. Add 3.

**What the output means:**
The result is a US school grade level. A SMOG grade of 10 means a reader needs approximately a 10th-grade education to understand the text with full comprehension (100% comprehension, not 75% as in Flesch/FK — see Section 3.3 and Section 4 for the importance of this distinction).

**The 30-sentence requirement:** The formula was specifically designed and validated for 30-sentence samples. This minimum exists because the count of polysyllabic words in fewer sentences introduces high variance — a single unusual sentence can skew the result substantially. The 30-sentence requirement is a statistical stability constraint, not an arbitrary rule. Shorter texts can be handled using the scaling version of the formula or adaptation methods (extrapolating polysyllabic words per sentence to a hypothetical 30-sentence total), but these produce less reliable results.

**Why polysyllabic words specifically?** McLaughlin identified an empirical law: the total number of syllables per 100 words can be estimated as (polysyllabic words × 3 + 112). This means polysyllabic word count is a reliable proxy for total syllable density, and it requires only a binary count (3+ syllables vs. not) rather than counting every syllable in every word. The 3-syllable cutoff was chosen empirically as the most predictive threshold.

### 3.3 Strengths

**Targets 100% comprehension.** This is the most important and often misunderstood distinction between SMOG and the Flesch family of formulas. McLaughlin designed SMOG to predict the education level required for complete understanding of a text, not just partial comprehension. Flesch and FK formulas were calibrated to approximately 75% comprehension (answering 75% of comprehension questions correctly). The 100% standard is more appropriate for any domain where misunderstanding has consequences — healthcare instructions, safety warnings, legal disclosures, technical operating procedures. A text at SMOG grade 8 should be fully comprehensible to someone at an 8th-grade reading level; a text at FK grade 8 may be only partially comprehensible to the same reader. (PMC3049622; gorby.app/readability/smog)

**Healthcare gold standard.** SMOG has the strongest validation record of any readability formula in the healthcare domain:
- The National Cancer Institute recommends SMOG for cancer pamphlets and patient education materials (PMC3049622).
- A 2010 study in the *Journal of the Royal College of Physicians of Edinburgh* established SMOG as the preferred measure for healthcare materials.
- Harvard T.H. Chan School of Public Health's Center for Health Communication uses SMOG as its primary readability tool.
- Multiple systematic reviews have confirmed SMOG's superiority over FK for detecting actual comprehension barriers in health materials.

**Simpler to calculate manually than its competitors.** The manual procedure requires only a binary classification of each word (3+ syllables or not) — easier than counting every syllable in every word. For a text of ~30 sentences, an experienced user can apply SMOG in about 9 minutes without specialized software (McLaughlin, 1969).

**Validated accuracy.** SMOG scores are reported to fall within approximately 1.5 grade levels of actual reader comprehension levels when measured against standardized reading tests (readabilityformulas.com/the-smog-readability-formula). The formula showed strong correlations with the McCall-Crabbs test and the Thorndike-McCall Reading Test in McLaughlin's original validation.

**Captures the interaction of word and sentence complexity.** By counting polysyllabic words within fixed sentence samples, SMOG implicitly captures both dimensions simultaneously — a text with long sentences full of polysyllabic words will score higher than a text with short sentences and the same per-word polysyllabic rate.

### 3.4 Weaknesses and Biases

**30-sentence minimum is a hard constraint.** SMOG was designed for and validated against 30-sentence samples. For short texts — web pages, product descriptions, form instructions, error messages, legal disclaimers — the formula either cannot be applied or produces unreliable results. Many real-world document types fall below this threshold. The adaptation for shorter texts (extrapolating to a hypothetical 30-sentence total) is a pragmatic workaround, not a validated method for texts significantly shorter than 30 sentences. Some tools refuse to calculate SMOG for texts under 30 sentences; others apply the scaling formula silently.

**Does not explicitly weight sentence length.** Unlike Flesch and FK, SMOG has no separate sentence-length term. While sentence length is implicitly captured (longer sentences in a fixed sample contain more chances for polysyllabic words), two texts with the same polysyllabic word count but different sentence lengths would score identically. A text with five very long, complex sentences containing 12 polysyllabic words would score the same as a text with 30 short sentences containing the same 12 polysyllabic words. Sentence structure and syntactic complexity are largely invisible to SMOG.

**Same syllable proxy problems as Flesch.** SMOG does improve on Flesch's approach by using a threshold (3+ syllables rather than counting every syllable), but it retains the fundamental limitation that polysyllabic word count is a proxy for vocabulary difficulty, not a direct measure of it. Medical monosyllabic jargon ("stat," "prion," "cyst") is invisible to SMOG just as it is to Flesch and FK.

**Systematically higher scores than Flesch/FK.** Because SMOG is calibrated to 100% comprehension rather than 75%, its grade levels are typically 2–4 grade levels higher than FK for identical texts in the healthcare domain (Walsh & Volsko; Freda; PMC5764592). This is appropriate given the design intent, but it creates confusion when practitioners compare SMOG scores to FK scores without understanding why they differ. A practitioner who learns that "aim for below grade 8" might conflate FK grade 8 (achievable more easily) with SMOG grade 8 (requiring substantially simpler vocabulary).

**Normed on the same McCall-Crabbs passages.** SMOG shares the norming weaknesses of Flesch RE (see Section 1.4). The McCall-Crabbs lessons are old, limited in scope, and their grade-level assignments were not based on rigorous empirical criteria.

**Less widely implemented in general-purpose tools.** FK and Flesch RE are built into Microsoft Word and many content management systems. SMOG, partly due to its 30-sentence requirement, is less universally available in off-the-shelf tools. Practitioners who want SMOG scores often need to use specialized or healthcare-specific readability software. Additionally, some automated SMOG implementations have been found to apply the formula incorrectly — a 2022 systematic study found that only some online calculators produced SMOG scores in acceptable agreement with manually calculated reference standards (PMC9856555).

**English only; US grade system.** The 3-syllable threshold and grade-level calibration are specific to English and the US educational system.

### 3.5 Best Use Cases

- **Patient and health education materials:** The primary validated application. Any text intended for patients, caregivers, or the general public on health topics should be assessed with SMOG rather than FK, because SMOG better captures the actual reading difficulty that leads to non-compliance or misunderstanding.
- **Safety warnings and critical instructions:** Anywhere where partial comprehension is not acceptable — operating procedures, medication instructions, safety data sheets, emergency information.
- **Public health communication:** Government health agencies, NGOs, and health communicators routinely use SMOG as a screening tool.
- **Long-form documents:** SMOG is most reliable on texts of 30+ sentences. It is well-suited to documents like brochures, pamphlets, educational booklets, training manuals, and similar formats.
- **Research that requires comparability across health studies:** Because SMOG is the most consistently used formula in health literacy research, using it allows comparison with published benchmarks.

### 3.6 What It Is NOT Good For

- **Short texts:** Fewer than 30 sentences significantly reduces reliability. For web pages, headlines, short product descriptions, or brief error messages, SMOG either cannot be calculated or produces poor results.
- **When sentence structure is the primary concern:** Because SMOG does not explicitly measure sentence length, it cannot distinguish a text that is difficult because of complex nested clauses from one that is difficult because of polysyllabic vocabulary.
- **Direct comparison with Flesch or FK scores:** The different comprehension targets (100% vs. 75%) mean SMOG scores will always be higher than FK scores for the same text. Mixing these scores in a single analysis without clearly documenting which formula produced which result is a source of confusion in the literature.
- **General-audience web content at scale:** Where texts are typically short and the 30-sentence requirement cannot be met.
- **Non-English text.**

---

## 4. Comparative Analysis

### 4.1 Flesch RE vs. Flesch-Kincaid: Same Inputs, Different Outputs

Flesch Reading Ease and Flesch-Kincaid Grade Level share identical input variables (ASL and ASW) but apply different regression coefficients derived from different calibration exercises:

| Feature | Flesch RE | FK Grade Level |
|---------|-----------|----------------|
| Formula origin | Flesch (1948) | Kincaid et al. (1975) |
| Output | 0–100 score (higher = easier) | Grade level (higher = harder) |
| ASL weight | 1.015 | 0.39 |
| ASW weight | 84.6 (subtractive) | 11.8 (additive) |
| Sentence length emphasis | Moderate | Relatively greater than Flesch RE |
| Norming corpus | 350 McCall-Crabbs passages | 18 Navy Rate Training Manual passages; ~531 Navy personnel |
| Comprehension target | ~75% | ~75% |

Because both formulas use the same inputs, they correlate inversely and closely — a text that scores very high on Flesch RE will score low on FK Grade Level — but they are **not directly convertible** because the weights differ. A 10-point change in Flesch RE does not correspond to a fixed change in FK Grade Level; the relationship depends on the specific mix of sentence length and word length in the text.

**When to use Flesch RE vs. FK Grade Level:**
- Use Flesch RE when a 0–100 score is more natural for the audience or when "higher = better" is easier to communicate (e.g., to writers who are improving their drafts).
- Use FK Grade Level when a grade-level output is expected by stakeholders (e.g., compliance checks against grade-level requirements, educational publishing, instructional design).
- For both use cases, be aware that the metrics are less reliable for technical and medical content than for general prose.

### 4.2 SMOG vs. Flesch/FK: Different Philosophies

The fundamental difference between SMOG and the Flesch family is not just formula mechanics — it is the comprehension standard each targets:

| Feature | Flesch RE / FK | SMOG |
|---------|---------------|------|
| Comprehension target | ~75% correct on comprehension questions | ~100% comprehension |
| Primary input | Average syllables per word + average sentence length | Count of polysyllabic words (3+) in 30 sentences |
| Sentence length | Explicit variable | Implicit (captured through fixed-sentence sampling) |
| Typical grade level vs. FK | — | 2–4 grade levels higher for same text (in healthcare) |
| Healthcare validation | Moderate | Strong (National Cancer Institute, CMS, RCPE) |
| Software availability | Very high (Word, many tools) | Moderate (specialized tools) |
| Minimum text length | ~100 words for stability | 30 sentences (hard practical minimum) |

**Which to choose:** The decision hinges on what "readable" means for your use case.

- If you're writing general-purpose content for broad audiences (news, blogs, business writing) and want a quick check that it's not impenetrably complex, Flesch RE or FK Grade Level is appropriate. The 75% comprehension benchmark is reasonable for general reading where full understanding is not critical.

- If you're writing content where misunderstanding has real consequences — health instructions, safety warnings, legal rights explanations, financial disclosures — use SMOG. The 100% comprehension design intent is directly relevant, and SMOG has the strongest validation record in those domains.

- If your text is less than 30 sentences and falls into a high-stakes domain, you face a genuine dilemma: SMOG is the better formula but may not apply reliably. In this situation, use multiple formulas and apply human judgment.

### 4.3 The Grade Level Discrepancy Problem

A recurring issue in the literature is that researchers studying the same documents with different formulas arrive at very different grade levels. A 148-document study (PMC5764592) found SMOG producing a mean of 9.6 compared to FK's 6.5 — a 3.1 grade level gap for identical documents. Studies by Walsh & Volsko and Freda found 2–3 grade level gaps consistently. The laryngology patient education materials study (Laryngoscope, cited above) found SMOG consistently 2–4 grade levels above FKGL.

This discrepancy is **not evidence that one formula is "wrong."** It reflects the different comprehension standards. Practitioners should:

1. Always specify which formula they used when reporting results.
2. Never compare Flesch/FK scores with SMOG scores as if they were measuring the same thing.
3. Be aware that institutional benchmarks (e.g., "aim for grade 6 or lower for patient materials") were almost always established using SMOG. If you apply FK Grade Level to the same materials and get a grade 6, that does not mean you've met the same standard.

### 4.4 The Problem All Three Share

All three formulas inherit a set of structural limitations that no refinement of their coefficients can solve:

**Surface features only.** All three measure what linguists call "surface-level" features — word length and sentence length as counted, not as experienced. They cannot measure:
- Semantic difficulty (word familiarity, abstractness, domain specificity)
- Discourse coherence (whether ideas connect logically)
- Text organization (whether headings, lists, and structure aid comprehension)
- Vocabulary familiarity (whether polysyllabic words are common or rare)
- Prior knowledge requirements (does the reader need domain expertise?)
- Syntactic complexity beyond raw sentence length

**Norming limitations.** All three were validated against McCall-Crabbs passages from the 1920s–1960s, or in the case of FK, against a very narrow Navy-specific corpus from 1975. None are well-calibrated for contemporary text types: social media, web content, email, technical documentation, or interactive interfaces.

**Proxy reliability.** As Klare's (1976) review showed, even when positive correlations with comprehension are found, the effect sizes are often modest, and negative results may be underreported. The formulas are useful screens, not precise measurements.

These limitations do not make the formulas useless. They make them what they actually are: imperfect but computationally tractable proxy measures useful for detecting gross readability problems, establishing approximate compliance with readability standards, and guiding revision. They should never be the sole determinant of whether content is "readable" — usability testing with actual readers is always more informative (Redish, 2000; UXMatters, 2019).

---

## 5. References

All references below are to primary sources, validated academic publications, or directly relevant institutional materials. Secondary summaries from commercial readability websites were used only for contextual detail and are not cited as authority.

**Primary sources:**

Flesch, R. (1948). A new readability yardstick. *Journal of Applied Psychology, 32*(3), 221–233. https://doi.org/10.1037/h0057532. PMID: 18867058.

Kincaid, J. P., Fishburne, R. P. Jr., Rogers, R. L., & Chissom, B. S. (1975). *Derivation of new readability formulas (Automated Readability Index, Fog Count and Flesch Reading Ease Formula) for Navy enlisted personnel* (Research Branch Report 8-75). Chief of Naval Technical Training, Naval Air Station Memphis. Available via DTIC: ADA006655. Also archived at UCF STARS: https://stars.library.ucf.edu/istlibrary/56/

McLaughlin, G. H. (1969). SMOG grading — A new readability formula. *Journal of Reading, 12*(8), 639–646. [Full text available via Ohio State University: https://ogg.osu.edu/media/documents/health_lit/WRRSMOG_Readability_Formula_G._Harry_McLaughlin__1969_.pdf]

**Simplification and critique of Flesch:**

Farr, J. N., Jenkins, J. J., & Paterson, D. G. (1951). Simplification of Flesch Reading Ease Formula. *Journal of Applied Psychology, 35*(5), 333–337. https://doi.org/10.1037/h0062427

**Key review and critique literature:**

Klare, G. R. (1976). A second look at the validity of readability formulas. *Journal of Reading Behavior, 8*, 129–152.

Redish, J. C. (2000). Readability formulas have even more limitations than Klare discusses. *ACM Journal of Computer Documentation, 24*(3), 132–137. https://doi.org/10.1145/344599.344637 [Full text: https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf]

DuBay, W. H. (2004). *The principles of readability*. Impact Information. [ERIC: ED490073. Full text: https://files.eric.ed.gov/fulltext/ED490073.pdf]

**On McCall-Crabbs norming problems:**

Cunningham, J. W., Hiebert, E. H., & Mesmer, H. A. (2018). *Investigating the validity of two widely used quantitative text tools*. TextProject. [Full text: https://textproject.org/wp-content/uploads/2022/07/Cunningham-Hiebert-Mesmer-2018.pdf]

Stevens, K. C. (1980). An examination of the McCall-Crabbs standard test lessons in reading. *Journal of Reading*, cited in DuBay (2004).

**Healthcare validation and comparison studies:**

Paasche-Orlow, M. K., Taylor, H. A., & Brancati, F. L. (2003). Readability standards for informed consent forms as compared with actual readability. *New England Journal of Medicine, 348*(8), 721–726. (Foundational healthcare readability study; widely cited for FK limitations.)

PMC3049622 — Shoemaker, S. J., Wolf, M. S., & Brach, C. (2011). Assessing readability of patient education materials: Current role in oncology practice. *Journal of Clinical Oncology*. [Available: https://pmc.ncbi.nlm.nih.gov/articles/PMC3049622/]

PMC5764592 — Study showing SMOG mean 9.6 vs FK mean 6.5 for 148 patient education documents. "Computerized versus hand-scored health literacy tools." [Available: https://pmc.ncbi.nlm.nih.gov/articles/PMC5764592/]

PMC9856555 — Comparison of automated SMOG and FK calculators against manually calculated reference standards. "Comparison of Readability Scores for Written Health Information." [Available: https://pmc.ncbi.nlm.nih.gov/articles/PMC9856555/]

PMC10027808 — CommonLit CLEAR corpus study; critique of norming limitations of traditional readability formulas. "A large-scaled corpus for assessing text readability." [Available: https://pmc.ncbi.nlm.nih.gov/articles/PMC10027808/]

**On gaming and formula limitations:**

Armbruster, B. B., Osborn, J. H., & Davison, A. L. (1985). Readability formulas may be dangerous to your textbooks. *Educational Leadership, 42*(7), 18–20.

Davison, A., & Kantor, R. N. (1982). On the failure of readability formulas to define readable texts: A case from adaptations. *Reading Research Quarterly, 17*(2), 187–209.

ACL Anthology (2021). Flesch-Kincaid is not a text simplification evaluation metric. In *Proceedings of the 1st Workshop on Natural Language Generation, Evaluation, and Metrics (GEM 2021)*. https://aclanthology.org/2021.gem-1.1.pdf

Crossley, S. A., Allen, D. B., & McNamara, D. S. (2011). Text simplification and comprehension: The effects of text elaborations and cohesion on comprehension and reading time. *Applied Linguistics*, 33(2), 228–250. (One of several Crossley et al. works on surface features vs. comprehension.)

**Institutional sources:**

Harvard T.H. Chan School of Public Health, Center for Health Communication. SMOG Readability Formula. https://hsph.harvard.edu/research/health-communication/resources/smog/

Wikipedia. Flesch-Kincaid readability tests. https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests [Used for formula summary data, not as primary source for historical or research claims.]

---

## Appendix: Uncertainty and Contested Claims

The following items in this report involve uncertainty or contested findings in the literature:

1. **The 0.91 correlation figure** (FK/Flesch with comprehension tests) cited in DuBay (2004) and repeated in educational writing sources. Klare's (1976) broader review found a more qualified picture — only 39/65 studies showed positive correlations, and positive results may be over-represented due to publication bias. The 0.91 figure likely applies to restricted conditions (similar text type and population to the norming data) and should not be taken as a general claim.

2. **The "100% vs. 75% comprehension" distinction for SMOG vs. Flesch.** This characterization is widely repeated in the health literacy literature and by the NCI. However, the original papers do not state their comprehension targets in these exact percentage terms. McLaughlin's design intent (full comprehension for his grade assignment) is clear; Flesch's 75% figure comes from how the McCall-Crabbs criterion was applied (reading at grade level = answering roughly 75% of questions correctly). The contrast is real but the specific percentages are interpretive reconstructions from methodology, not direct statements in the original papers.

3. **Whether SMOG is genuinely superior to Flesch/FK for health materials or simply systematically higher.** Some critics argue that SMOG produces higher scores not because it better measures comprehension difficulty, but because its 100% comprehension calibration produces grade levels that are intrinsically higher — and if you recalibrated Flesch/FK to the same comprehension target, the difference would narrow. This is a legitimate methodological debate. For practical purposes, SMOG remains the standard in health literacy research and the NCI recommendation holds.

4. **The "40–60% readership increase" from Flesch's AP work.** This figure appears in DuBay (2004) and other secondary sources but the original data from the Associated Press study are not readily accessible for verification. The direction of the effect is plausible given the magnitude of the reading level reduction reported; the specific percentage should be treated as approximate.

---

*Research compiled for internal use by the Readable library project. For questions about this report, see the project's claudedocs directory.*
