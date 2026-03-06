<!--
SPDX-FileCopyrightText: 2026 PlainLicense

SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT
-->

# Research Report: ARI, Coleman-Liau, and Gunning Fog Readability Metrics

**Prepared for**: Readable library documentation
**Date**: 2026-03-05
**Scope**: Automated Readability Index (ARI), Coleman-Liau Index (CLI), and Gunning Fog Index

---

## Table of Contents

1. [ARI (Automated Readability Index)](#ari-automated-readability-index)
   - Background and History
   - Formula Explained
   - Strengths
   - Weaknesses and Biases
   - Best Use Cases
   - Not Good For
2. [Coleman-Liau Index](#coleman-liau-index)
   - Background and History
   - Formula Explained
   - Strengths
   - Weaknesses and Biases
   - Best Use Cases
   - Not Good For
3. [Gunning Fog Index](#gunning-fog-index)
   - Background and History
   - Formula Explained
   - Strengths
   - Weaknesses and Biases
   - Best Use Cases
   - Not Good For
4. [Comparative Analysis](#comparative-analysis)
   - ARI vs. Coleman-Liau: Both Character-Based
   - Gunning Fog vs. Syllable-Based Metrics
   - Scoring the Same Text: What to Expect
   - When to Use Which
5. [References](#references)

---

## ARI (Automated Readability Index)

### Background and History

The Automated Readability Index was developed by E. A. Smith (EdD, Aerospace Medical Research Laboratories) and R. J. Senter (PhD, University of Cincinnati), and published in November 1967 in a report titled "Automated Readability Index" (AMRL-TR-66-220). The research was conducted at the Aerospace Medical Research Laboratories, Wright-Patterson Air Force Base, Ohio, as part of a project on human factors in training system design for the U.S. Air Force (Smith and Senter, 1967).

The stated problem that motivated the work was practical: Air Force technical manuals and training materials were frequently written at a reading level that exceeded the capabilities of the enlisted personnel expected to use them. The military needed a way to assess the readability of documents as they were being produced, without the computational overhead of existing formulas.

**The typewriter connection** is central to understanding why the formula was designed the way it was. Smith and Senter designed a hardware attachment called the "Readability Index Tabulator," built by Robert Roettele, that physically connected to an IBM Selectric (model 721) electric typewriter. The Tabulator consisted of three counters (Sodeco TCe F4E, TCe F5E, and TCe F6E) triggered by the typewriter's keyboard. As a typist typed, the machine automatically counted: (a) the number of keystrokes (characters), (b) the number of words (spaces), and (c) the number of sentences (as entered by the typist). This enabled real-time readability monitoring without any post-hoc manual analysis (Smith and Senter, 1967).

The insight was that characters (keystrokes) are trivially easy to count mechanically — each key press is one character — whereas syllables require linguistic analysis. Existing formulas like Flesch (1948) and the Gunning Fog Count (1952) required offline counting. ARI was built for the production environment, not the review environment.

In 1975, Kincaid, Fishburne, Rogers, and Chissom recalculated ARI (along with the Fog Count and Flesch formulas) specifically for Navy enlisted personnel, deriving updated coefficients from reading comprehension test results of 531 Navy enlisted personnel at Naval Air Station Memphis and Great Lakes Navy Training Center. This "recalculated ARI" (Kincaid et al., 1975) is what most modern implementations use, with the constant -21.43 (the original Smith/Senter constant was -21.34, a minor difference that has propagated inconsistently across implementations).

### Formula Explained

The Readable library implements:

```
ARI = 4.71 × (characters / words) + 0.5 × (words / sentences) - 21.43
```

Where `characters` counts letters and digits only (not whitespace or punctuation), `words` counts space-delimited tokens, and `sentences` counts sentence-terminating punctuation.

**What the components measure:**

- **Characters per word (× 4.71)**: This is the word complexity proxy. Longer words tend to be less common, more Latinate, and harder to decode. The coefficient 4.71 was derived through regression analysis to optimally predict reading comprehension. The weight is higher than the sentence length weight because word complexity was found to be the dominant predictor.

- **Words per sentence (× 0.5)**: Sentence complexity proxy. Longer sentences impose more working memory load. The lower weight (0.5 vs. 4.71) reflects that sentence length, while important, is a weaker predictor than word complexity in the original regression.

- **-21.43**: A normalizing constant that anchors the output to U.S. grade levels. Without this offset, the formula would produce raw scores far above typical grade levels.

**Output interpretation:**

| ARI Score | Grade Level | Typical Age |
|-----------|-------------|-------------|
| 1         | 1st Grade   | 6-7 years   |
| 2         | 2nd Grade   | 7-8 years   |
| 3         | 3rd Grade   | 8-9 years   |
| 4         | 4th Grade   | 9-10 years  |
| 5         | 5th Grade   | 10-11 years |
| 6         | 6th Grade   | 11-12 years |
| 7         | 7th Grade   | 12-13 years |
| 8         | 8th Grade   | 13-14 years |
| 9         | 9th Grade   | 14-15 years |
| 10        | 10th Grade  | 15-16 years |
| 11        | 11th Grade  | 16-17 years |
| 12        | 12th Grade  | 17-18 years |
| 13        | College/UG  | 18-24 years |
| 14+       | Graduate    | 22+ years   |

Non-integer scores are rounded up to the nearest whole number per the original specification.

### Strengths

**Machine computation accuracy**: The central advantage of ARI is that character counting is exact in a way that syllable counting cannot be. Syllable counting algorithms — whether implemented in software or performed by humans — introduce errors. The phonological structure of English is irregular enough that even trained humans disagree on syllable boundaries in many words (Coleman and Liau, 1975, explicitly cited this as motivation for their similar approach). Character counting is deterministic.

**Speed in production environments**: The original motivation — monitoring readability as text is being produced — remains valid in modern NLP pipelines. ARI can be computed in O(n) string operations with no dictionary lookups, phoneme tables, or heuristic rules. For large-scale document processing, this matters.

**Validated for technical and military documentation**: The original validation was against comprehension scores on Air Force technical manuals. The 1975 recalculation used actual reading comprehension test results from 531 Navy personnel on Navy training manuals (Kincaid et al., 1975). This makes ARI arguably better calibrated for technical documentation than formulas derived from basal readers or general prose.

**Strong inter-formula agreement**: Multiple studies find ARI correlates well with other readability metrics when applied to the text types it was validated on. The Kincaid (1975) study found ARI, Fog Count, and recalculated Flesch all provide approximately the same grade level scores on a large enough sample of military technical materials.

**Good for adult reading material**: Smith and Senter (1967) explicitly noted that word lists (used by Dale-Chall and Spache) are advantageous at 4th grade and below, but "somewhat inaccurate when applied to adult reading material." Character-based metrics like ARI avoid this limitation.

### Weaknesses and Biases

**Character counting conflates script length with cognitive difficulty**: The core proxy — longer words are harder — holds statistically across large corpora but breaks down in important specific cases:

- **Abbreviations and acronyms inflate apparent difficulty**: In technical documentation, words like "mm", "Hz", "dB", "kg", "API", "SQL" are very short by character count but may be conceptually opaque to a novice reader. ARI would score a document heavy in such abbreviations as deceptively easy. Conversely, expanding those abbreviations to "millimeters," "hertz," and "decibels" would raise the ARI score despite potentially aiding comprehension.

- **Common long words are penalized**: Words like "interesting," "beautiful," "wonderful," "important," and "information" have 9-11 characters each and push ARI scores upward, despite being part of ordinary everyday vocabulary for most adults. The formula cannot distinguish between a long common word and a long rare word.

- **Short but difficult words are invisible**: Technical jargon often uses short terms: "flux," "torque," "node," "shear," "fret," "null," "void," "heap," "stack." Domain-specific short words are treated as easy by ARI but may be entirely opaque to an out-of-domain reader.

**Sentence splitting artifacts**: The formula's sentence variable is sensitive to how sentence boundaries are detected. Bullet lists, headers, code examples, numbered steps, and other non-prose structures common in technical documentation create artificial "sentences" that do not correspond to cognitive processing units.

**Constant discrepancy between implementations**: The original Smith and Senter (1967) formula used -21.34; the widely cited version uses -21.43. This discrepancy, while small, has propagated across implementations without systematic documentation. The difference produces ARI scores that diverge by a small but non-trivial amount on short texts.

**No sensitivity to vocabulary frequency or familiarity**: Two texts can have identical ARI scores while differing dramatically in conceptual difficulty if one uses common long words and the other uses rare long words. ARI cannot detect this.

**Bias toward certain genres**: ARI tends to score poetry, dialogue, and conversational prose as lower than analytical prose, even when the latter is actually more accessible because of explicit logical connectives. Short declarative sentences with rare vocabulary will score low; long but well-structured sentences with common vocabulary will score high.

### Best Use Cases

- **Technical documentation and manuals**: ARI was validated specifically for this domain, making it the most defensible choice for military, engineering, aerospace, and industrial documentation.
- **Real-time readability monitoring in authoring tools**: The computational simplicity makes it suitable for editor plugins and live feedback.
- **Batch processing of large document corpora**: Where syllable-counting overhead matters at scale.
- **Adult-level material (grade 6 and above)**: More reliable than word-list approaches at higher grade levels.
- **Baseline comparison in multi-metric analysis**: As one metric among several, ARI provides a useful data point with clear interpretation.

### Not Good For

- **Children's texts (grade 5 and below)**: Word lists (Dale-Chall, Spache) are better calibrated for early reading material.
- **Documents heavily reliant on abbreviations, acronyms, or short technical codes**: The character proxy breaks down when short-form notation is prevalent.
- **Poetry and literary prose**: Sentence structure and rhythm matter in ways ARI cannot capture.
- **Non-prose formats**: Bullet lists, tables, code blocks, structured forms — the formula assumes running narrative.
- **Non-English text**: The formula's coefficients were derived from English corpora. Character length distributions differ substantially across languages, and applying ARI to non-English text is not appropriate.
- **Assessing conceptual complexity or domain expertise requirements**: A document written entirely in accessible prose about quantum field theory will score easier than a document about carpentry using longer trade terminology.

---

## Coleman-Liau Index

### Background and History

The Coleman-Liau Index was developed by Meri Coleman and T. L. Liau and published in 1975 in the *Journal of Applied Psychology* (Vol. 60, pp. 283-284). The full title of the paper was "A computer readability formula designed for machine scoring." The work was done in collaboration with the U.S. Office of Education, with the stated goal of assessing the readability of textbooks across the public school system (Coleman and Liau, 1975).

The historical context is specific and interesting: in 1975, the available methods for computer-assisted readability scoring required "keypunching the text into the computer" before analysis — a costly, time-consuming process. Coleman and Liau were designing around an alternative technology: optical scanning devices that could read printed text from physical documents without full character recognition. Their key insight was that a scanner need not recognize *which* characters appeared in a word, only *how many* characters it contained. This reduced the hardware requirement dramatically. The paper's abstract (which Wikipedia uses as its worked example) states: "Both predictors can be counted by an optical scanning device, and thus the formula makes it economically feasible for an organization such as the U.S. Office of Education to calibrate the readability of all textbooks for the public school system" (Coleman and Liau, 1975).

This is historically significant: Coleman-Liau predates reliable OCR (optical character recognition), and was explicitly designed for a generation of simpler scanning hardware that could detect character boundaries without identifying characters. The practical motivation has evaporated in the modern era — full OCR and NLP pipelines are now standard — but the statistical insight that letter count predicts readability at least as well as syllable count remains valid and is the formula's enduring contribution.

Coleman and Liau also made a theoretical argument alongside the practical one, quoting: "There is no need to estimate syllables since word length in letters is a better predictor of readability than word length in syllables." This claim has been disputed (opinion on accuracy relative to syllable-based indices varies, per Wikipedia's Coleman-Liau article), but it reflects the authors' empirical finding that, controlling for other factors, character length was a marginally better predictor in their regression analysis.

### Formula Explained

The Readable library implements:

```
CLI = 0.0588 × L - 0.296 × S - 15.8
```

Where:
- `L` = (letters / words) × 100 — the average number of letters per 100 words
- `S` = (sentences / words) × 100 — the average number of sentences per 100 words

Note that Coleman-Liau **does not count digits** as characters, unlike ARI — it is specifically letters only. This is a meaningful implementation difference. A text with many numerals will score differently under ARI (which counts digits) vs. CLI (which does not).

**What the components measure:**

- **L (letters per 100 words × 0.0588)**: Word length proxy. Larger L means longer words on average, which the formula treats as harder to read. The per-100-words normalization means the formula is scale-invariant: it doesn't matter if you analyze 200 or 2000 words, the score is computed on normalized rates.

- **S (sentences per 100 words × -0.296)**: Sentence length proxy, but inverted. More sentences per 100 words means shorter sentences, which means easier text, which is why the coefficient is negative. Fewer sentences per 100 words means longer sentences, which raises the score. This is mathematically equivalent to words-per-sentence but expressed as a rate.

- **-15.8**: Calibration constant anchoring output to U.S. grade levels.

**The formula can also be expressed as:**

```
CLI = 5.88 × (letters / words) + 29.6 × (sentences / words) - 15.8
```

This algebraically equivalent form (seen in some implementations) makes the sentence length term positive since the relationship to grade level is positive: more words per sentence = harder. The -15.8 calibrates the output range.

**Output interpretation**: Like ARI, CLI outputs a U.S. grade level. A score of 8 means an 8th-grader can be expected to comprehend the text. The recommended range for material targeting the general public is 8-10.

### Strengths

**Full independence from syllable counting**: Coleman-Liau's defining property is that it requires no phonological knowledge whatsoever. The formula needs only a count of letters (distinguishing letter characters from non-letter characters), spaces (word boundaries), and sentence-terminal punctuation. This makes it:
  - Completely deterministic — no heuristic syllable rules
  - Fast — O(n) string scan with minimal processing
  - Cross-platform consistent — two implementations agree exactly on every text

**Historical suitability for pre-OCR machine processing**: While this is no longer a practical concern, it explains the formula's architectural choices. The design requirement was minimum information per character: character vs. non-character (for letter count), character vs. space vs. sentence-terminal mark (for word/sentence count). No other information was needed. This is why the formula uses raw letter count rather than distinguishing letter types.

**Scale-invariant formulation**: By normalizing to per-100-words rates, Coleman-Liau is explicitly designed to work on text samples of varying length (though like all readability formulas, very short texts produce unstable scores). The original paper recommended samples of at least 300 words for reliable results.

**Education and curriculum validation**: The formula was developed with U.S. public school textbooks as the primary corpus. This makes it reasonably well calibrated for educational content at grade levels 4-12.

**Wide applicability**: Coleman-Liau has been applied in education, healthcare communication, legal readability analysis, and translation quality assessment. Its character-based approach is considered particularly consistent across content types.

### Weaknesses and Biases

**Shares the core character-proxy problem with ARI**: The same critiques apply here — abbreviations score as easy, common long words score as hard, short domain-specific jargon scores as easy regardless of cognitive difficulty. Coleman-Liau is slightly different from ARI because it excludes digits from the character count, but the structural limitation is the same.

**Letters-only creates novel edge cases**: By counting only letters and not digits, Coleman-Liau treats "H2O," "CO2," "2FA," "3D," and similar alphanumeric tokens differently from ARI. A document heavy in chemical formulae or identifier codes will produce different character-to-word ratios under the two formulas, without necessarily reflecting any real difference in reading difficulty.

**Tends to score higher than ARI on the same text**: In practice, the CLI often assigns scores approximately 1-2 grade levels higher than ARI on identical texts. This is an empirical observation across multiple comparative studies, not a systematic derivation — the formulas use different normalizations and different regression coefficients derived from different corpora.

**Insensitive to vocabulary familiarity**: Like ARI, Coleman-Liau cannot distinguish between a long familiar word ("interesting") and a long rare word ("exsanguination"). It cannot detect whether readers are likely to know the words being used.

**Does not penalize conceptual density**: Two texts with identical letter-per-word and sentence-per-word profiles but radically different information density (number of distinct concepts per sentence) will receive the same CLI score.

**Sentence detection is critical and underspecified**: The formula's S variable is highly sensitive to sentence boundary detection. Coleman and Liau (1975) were working with printed text scanned from physical books, where sentence boundaries are marked by visible terminal punctuation. In digital text, sentence boundary detection in the presence of abbreviations, ellipses, and structured content introduces errors that directly affect the CLI score.

**Validated primarily on textbooks, not technical prose**: The corpus used to derive CLI was U.S. public school textbooks across grade levels. This makes it well-suited for evaluating educational content in the same register, but less validated for technical documentation, legal text, or informal prose.

### Best Use Cases

- **Evaluating educational textbooks and curriculum materials**: This is the domain the formula was explicitly designed and validated for.
- **Medical and health literacy materials**: Widely used in healthcare communication research to assess patient-facing materials.
- **Legal readability analysis**: Applied in research examining the readability of judicial opinions and regulatory documents.
- **Batch processing of educational content at scale**: The formula's simplicity makes it efficient for large-scale curriculum audits.
- **Cross-metric comparison**: Useful as one data point alongside ARI, Flesch-Kincaid, and SMOG, particularly for establishing consensus when multiple formulas agree.

### Not Good For

- **Documents with heavy numeral content**: Digits are excluded from CLI's character count, creating a systematic bias compared to ARI in numeral-heavy texts.
- **Short texts under 300 words**: The formula becomes statistically unreliable on short samples, as a single complex sentence can shift the score significantly.
- **Children's texts (grade 3 and below)**: Word-list approaches remain better calibrated at early reading levels.
- **Texts with heavy abbreviation use**: Same limitation as ARI — abbreviations score as easy even when conceptually dense.
- **Non-English text**: Developed and validated on English corpora only.

---

## Gunning Fog Index

### Background and History

The Gunning Fog Index was developed by Robert Gunning (1908-1980), an American businessman who had worked in newspaper and textbook publishing. Gunning was not an academic linguist but a practitioner who had observed, in his publishing career, that business documents and news articles were routinely written at reading levels that exceeded most readers' abilities.

In 1944, Gunning left his editing job and founded Robert Gunning Associates, described by one contemporary account as a consulting business "not listed in the government's index of occupations" — readability consulting being an entirely new profession (Notorc, 2006). His firm worked with over 60 large-city daily newspapers and popular magazines over the following years, helping writers and editors reduce unnecessary complexity.

In 1952, Gunning published *The Technique of Clear Writing* (McGraw-Hill), which introduced the Fog Index. The book presented the formula as a practical tool for working journalists, business writers, and editors — not as a formal academic contribution. This origin in practice, rather than academia, distinguishes the Fog Index from ARI and Coleman-Liau, both of which were published in peer-reviewed or semi-academic contexts.

The Fog Index has been revised over its publication history. Gunning revised *The Technique of Clear Writing* in 1968 and again in 1973. The Gunning-Mueller Clear Writing Institute, Inc. (established in Santa Barbara, California) holds the copyright on the formula and the "Ten Principles of Clear Statement" that accompanied it. The University of Missouri published an adapted version of the formula with permission.

Kincaid et al. (1975) recalculated the Fog Count alongside ARI and Flesch as part of the same Navy study, producing a "Recalculated Fog Count" calibrated to Navy enlisted personnel reading Navy technical manuals. However, the original Gunning formula remains the more commonly cited version, and the two produce similar results on large samples (Kincaid et al., 1975).

The name "Fog Index" reflects Gunning's core metaphor: unnecessary complexity creates "fog" that obscures meaning. Gunning believed that much of the readability problem was a *writing* problem, not a reading problem — writers made texts unnecessarily difficult through long sentences and polysyllabic vocabulary when simpler alternatives existed.

### Formula Explained

The Readable library implements:

```
Gunning Fog = 0.4 × ((words / sentences) + 100 × (complex_words / words))
```

Where `complex_words` are words of three or more syllables, with the following exclusions:
- Proper nouns (capitalized names like "Baltimore," "Mrs. Madison")
- Familiar compound words (like "bookkeeper," "sunflower," "butterfly")
- Words made three syllables by the suffixes -ed or -es (like "created," "trespasses")

**What the components measure:**

- **words / sentences** (Average Sentence Length, ASL): The average number of words per sentence. Longer sentences increase cognitive load because readers must hold more information in working memory while parsing the grammatical structure.

- **100 × (complex_words / words)** (Percentage of Hard Words, PHW): The proportion of polysyllabic words in the text, expressed as a percentage. This is the formula's measure of vocabulary complexity. The 100 multiplier converts the proportion to a percentage, putting it on a compatible scale with ASL.

- **0.4**: The balancing coefficient. Through empirical analysis, Gunning found that multiplying the sum of ASL and PHW by 0.4 produced a score that corresponded approximately to the years of formal education a reader would need to understand the text on first reading.

**The "complex word" definition and its implementations:**

This is where Gunning Fog introduces the most implementation variance. The definition of "complex word" in practice varies:

- **Gunning's original (1952)**: Words with three or more syllables, excluding proper nouns, hyphenated words, and two-syllable verbs made into three syllables by -es or -ed endings. Some sources cite his original definition as excluding two-syllable verbs (not just two-syllable-made-three), creating ambiguity.

- **Kincaid et al. (1975) recalculated version**: Applied the same formula structure to Navy training materials, deriving new coefficients. The definition of "complex words" was maintained.

- **Modern NLP implementations**: Commonly omit the proper noun and compound word exclusions because they require part-of-speech tagging or capitalization heuristics that add complexity. An implementation that counts *all* three-syllable-or-more words without exclusions will produce systematically higher Fog scores than the original formula intended.

The Readable implementation should be checked against which exclusion rules it applies, as the score will differ materially depending on this choice.

**Output interpretation:**

| Fog Score | Education Level | Example Publications |
|-----------|-----------------|---------------------|
| 6         | 6th Grade       | Comics, simple prose |
| 7-8       | 7th-8th Grade   | Reader's Digest, True Confessions |
| 9         | 9th Grade       | Reader's Digest |
| 10        | 10th Grade      | Time magazine |
| 11        | 11th Grade      | Harper's, high school junior |
| 12        | 12th Grade      | Atlantic Monthly, high school senior |
| 13-16     | College         | College-level academic texts |
| 17+       | Post-graduate   | Graduate academic, professional journals |

Gunning's empirical benchmarks: Bible, Shakespeare, and Mark Twain score approximately 6. Time and the Wall Street Journal average approximately 11. A score above 12 is considered too complex for most readers. Scores above 17 indicate graduate-level material. The formula's output range is nominally 0-20+, but scores above 20 are considered "barely readable" by most users.

### Strengths

**Practical simplicity and intuitive interpretation**: Unlike ARI (which requires character counting) or Coleman-Liau (which requires computing per-100-word rates), the original Fog Index formula was designed to be computed manually with a pencil and notepad on a 100-word sample. This practicality made it accessible to journalists and business writers without computational tools.

**Dual predictor captures both length and vocabulary**: By combining sentence length (ASL) and vocabulary complexity (PHW), Gunning Fog captures two genuinely different aspects of readability that do not always co-vary. A text can have short sentences with complex vocabulary, or long sentences with simple vocabulary. Fog penalizes both, and the 0.4 coefficient was chosen empirically to weight them approximately equally in predicting comprehension difficulty.

**Validated in business and journalism contexts**: Gunning's extensive consulting experience with 60+ newspapers and magazines provides the ecological validity that academic studies often lack. The formula was tested against real readers of real publications.

**Good for adult prose and business writing**: Gunning's consulting work focused specifically on business communications, news articles, and professional documents — the same domain where the formula remains most commonly applied. For this type of content, Fog provides a useful signal.

**Strong correlation with Flesch-Kincaid in many studies**: Multiple comparative studies find Gunning Fog correlates highly with Flesch-Kincaid Grade Level when applied to the same text (Kincaid et al., 1975, found correlations of .80 or higher across the three formulas they studied). This suggests Fog is measuring a real and similar underlying dimension.

**Financial reporting research**: A substantial body of empirical finance research uses Gunning Fog as a proxy for deliberate obfuscation in corporate annual reports and 10-K filings. The index has been found to be associated with earnings management — companies with worse financial performance tend to produce more opaque reports (Li, 2008; and subsequent studies). This is a sophisticated use case where the "complexity = difficulty" heuristic has proven empirically productive.

### Weaknesses and Biases

**The polysyllabic word heuristic is crude**: The formula treats any word of three or more syllables as "complex," regardless of how common or familiar that word is. This creates systematic false positives:

- Common everyday words like "beautiful," "interesting," "important," "however," "another," "remember," "together," "yesterday," "already," and "understand" all have three syllables and will be counted as complex words.
- The word "spontaneous" (four syllables) is not considered a difficult word by most adult readers, yet it counts the same as "prestidigitation."
- Words familiar to a specialist audience — "antibody," "algorithm," "education," "university" — are flagged as complex even when they are core vocabulary for the target readers.

This is documented in the Gunning Fog Wikipedia article and explicitly noted in the original Gunning formula documentation (Gunning, 1952).

**Implementation variance on "complex word" exclusions**: As noted above, the exclusion rules for proper nouns, compound words, and inflected forms are applied inconsistently across implementations. A text with many proper nouns (a news article, a historical document) will score significantly differently depending on whether the implementation excludes capitalized words. This creates a reproducibility problem — two Fog scores computed by different tools on the same text may not be comparable.

**Short words can be difficult, long words can be easy**: This is the fundamental limitation of syllable-counting approaches. Domain-specific short words ("flux," "torque," "null," "shear," "node," "quark") are invisible to Fog. Common long words ("interesting," "government," "education") inflate the score.

**Sentence structure is ignored**: The formula counts words per sentence but ignores grammatical complexity. A long sentence with a simple subject-verb-object structure may be easy to parse, while a short sentence with embedded relative clauses, multiple negations, or passive constructions may be genuinely difficult. Fog cannot distinguish these.

**Compound sentence counting variant**: Some sources note that Gunning's original specification treated sentences connected by semicolons, colons, or commas (when linking complete thoughts) as compound sentences to be counted as two sentences. This variant, if applied, reduces Average Sentence Length and therefore lowers the Fog score. Most modern implementations count by punctuation marks (periods, question marks, exclamation marks) only, ignoring this compound-sentence rule.

**Context and reader familiarity ignored**: A document can use simple vocabulary and short sentences while discussing a highly specialized topic that requires significant domain knowledge. A pharmaceutical leaflet written at an 8th-grade Fog score is not actually readable by an 8th-grader if they don't know what the underlying medical condition is.

**Gaming the formula is straightforward and counterproductive**: Writers who know the formula can produce low Fog scores by artificially chopping sentences into fragments, which Gunning himself warned against: "Don't write to make a good fog index score. That will make you write short, choppy sentences. Like these." (Gunning-Mueller Clear Writing Institute, as cited by MU Extension, 1973/2006).

**Bias toward penalizing technical and scientific vocabulary**: Because technical and scientific terminology is disproportionately polysyllabic (derived from Greek and Latin roots), Fog systematically rates technical documents as harder than equivalently complex non-technical documents. A medical text using "myocardial infarction" scores harder than one using "heart attack," even though both convey similar information to readers in the target audience.

### Best Use Cases

- **Business writing and corporate communications**: This is the domain Gunning validated the formula on. Reports, memos, policies, and executive communications are appropriate targets.
- **News articles and journalism**: Gunning's consulting practice with 60+ newspapers makes this a well-validated context.
- **Legal and regulatory documents**: Fog is commonly used to assess regulatory readability for the public.
- **Financial reporting opacity research**: Gunning Fog has an established empirical track record as a proxy for deliberate obfuscation in financial disclosures.
- **Writing feedback for adult audiences**: As a quick check on whether business or professional prose is unnecessarily complex.
- **Approximate cross-document comparison**: When ranking documents by relative complexity within a consistent genre, Fog provides a useful ordinal measure.

### Not Good For

- **Scientific and medical documentation**: The polysyllabic-word proxy systematically misclassifies domain vocabulary as "complex" even when familiar to the target audience. SMOG is generally preferred for healthcare materials.
- **Children's texts**: Dale-Chall and Spache are calibrated for early reading material; Fog is not.
- **Texts with many proper nouns**: News articles about named entities, historical texts, and documents with extensive proper noun lists will score differently depending on whether the implementation applies proper noun exclusions.
- **Poetry and non-prose text**: The formula assumes running narrative prose.
- **Non-English text**: The syllable-based definition of "complex word" is specific to English phonology.
- **Texts where the 3-syllable threshold is actively misleading**: Documents in domains where polysyllabic vocabulary is both common and necessary (medicine, law, engineering) will score artificially high without this reflecting reader difficulty for the intended audience.

---

## Comparative Analysis

### ARI vs. Coleman-Liau: Both Character-Based

ARI and Coleman-Liau are the two character-based readability metrics in the Readable library. They share the fundamental insight that letter count is a tractable machine-computable proxy for word complexity, and both were developed specifically for mechanical/computational scoring. Despite these similarities, they differ in important ways:

**Different character definitions:**
- ARI counts letters *and digits*. A number like "2024" contributes 4 characters.
- Coleman-Liau counts letters *only*. The same "2024" contributes 0 characters.

This means on documents heavy in numerical data (financial reports, scientific papers with measurements, technical specifications), ARI and CLI will diverge systematically. Texts with many numbers will appear relatively harder under ARI and relatively easier under CLI.

**Different normalization:**
- ARI computes the ratio directly: (characters / words).
- CLI normalizes to per-100-words rates before formula application: (letters / words) × 100.

The CLI normalization was designed to allow mechanical counting on fixed-length text samples, which was relevant to the optical scanner use case. In modern implementations, both approaches produce identical ordinal rankings (they're mathematically equivalent transformations), but they reach that equivalence through different paths.

**Different calibration corpora:**
- ARI was calibrated on U.S. Air Force technical manuals and then recalibrated on Navy technical training materials (Kincaid et al., 1975).
- CLI was calibrated on U.S. public school textbooks across grade levels.

This means ARI is likely better calibrated for technical documentation, while CLI is likely better calibrated for educational content.

**Empirical score differences**: In practice, CLI often returns scores approximately 1-2 grade levels higher than ARI on the same text. This is a consistent empirical pattern observed across comparative studies (e.g., EFL assessment studies, health content studies). The difference reflects the different corpora and regression coefficients, not a meaningful methodological superiority of either formula.

**When to use ARI over CLI:**
- Technical documentation (manuals, specifications, engineering documents)
- Documents with significant numerical content where digit-counting behavior is preferred
- When ARI's validated alignment with military and technical writing contexts is relevant

**When to use CLI over ARI:**
- Educational textbooks and curriculum materials
- When consistency with prior health literacy research is needed
- When digit-exclusion behavior is preferred
- When comparing against studies that used CLI as the standard

### Gunning Fog vs. Syllable-Based Metrics

The most obvious comparison is between Gunning Fog and other syllable-based metrics like Flesch-Kincaid Grade Level (FKGL) and SMOG.

**Fog vs. Flesch-Kincaid Grade Level:**
Both use syllable counting and average sentence length. The key difference is what each formula does with syllable information:
- FKGL uses the *average* syllables per word across the text.
- Fog counts only words that *exceed a threshold* (3+ syllables), treating all other words as equally easy regardless of syllable count.

This threshold approach means Fog is particularly sensitive to the proportion of polysyllabic words, while FKGL responds more smoothly to the overall syllable density. A text with many 2-syllable words will score lower on Fog than on FKGL; a text with occasional very long words surrounded by monosyllables will score higher on Fog.

Kincaid et al. (1975) found ARI, Fog, and Flesch intercorrelations of .80 or higher across their study passages, suggesting all three are measuring similar underlying constructs. However, they diverge on specific text types.

**Fog vs. SMOG:**
SMOG (Simple Measure of Gobbledygook, McLaughlin, 1969) was explicitly designed as "a more accurate and more easily calculated substitute for the Gunning fog index." SMOG uses the square root of polysyllabic word count, multiplied by a ratio correction, and is calibrated to require 100% comprehension rather than first-reading comprehension.

For healthcare and medical writing, SMOG is generally preferred over Fog because:
- SMOG is considered better calibrated for health literacy research
- SMOG's 100% comprehension calibration is more appropriate when patient safety depends on full understanding
- SMOG is simpler to apply manually (no sentence length calculation)

For business writing and general prose, Fog remains more widely cited, partly for historical reasons and partly because its dual-variable structure (sentence length + complex word percentage) is more intuitive to writers who want to know *which* aspect of their writing to improve.

### Scoring the Same Text: What to Expect

When all three metrics are applied to the same passage, you should expect:
- ARI and CLI to generally agree within 1-3 grade levels but sometimes diverge based on digit content and different calibration.
- CLI to typically score 1-2 grade levels higher than ARI on most text.
- Fog to correlate broadly with the other two but diverge on texts with many polysyllabic words (Fog will score higher) or texts with many long sentences of common vocabulary (Fog may score lower if those long words are everyday vocabulary).
- On highly technical text with domain abbreviations: ARI and CLI may score it as easier than it actually is; Fog may score it as harder because technical vocabulary is polysyllabic.
- On healthcare materials: SMOG is the benchmark; Fog will generally agree in direction but calibrate to a different comprehension threshold.

Multiple studies applying all three to health websites, medical documents, and general web content find that the formulas produce varying absolute scores but generally agree on relative ranking of documents from harder to easier (e.g., the LWW comparative study of 102 websites found mean Fog of 14.04, CL of 11.74, and ARI of 11.52 on the same content — different absolute values but similar relative picture).

### When to Use Which

| Scenario | Best Choice | Rationale |
|----------|-------------|-----------|
| Technical/military documentation | ARI | Validated on this domain; character-based is appropriate for technical prose |
| Educational textbooks | Coleman-Liau | Original calibration corpus; designed for this purpose |
| Business writing and journalism | Gunning Fog | Historical validation; intuitive for writers |
| Healthcare / patient education | SMOG (not in this trio) | But if required, Fog for relative comparison |
| Legal documents | Coleman-Liau | Established use in readability of judicial opinions |
| Financial disclosures | Gunning Fog | Established empirical use in opacity research |
| Large-scale automated processing | ARI or CLI | Faster than syllable-based methods |
| Multi-metric consensus | All three | Disagreement between metrics is itself informative |

---

## References

**Primary Sources**

Smith, E. A., and Senter, R. J. (1967). *Automated Readability Index*. Technical Report AMRL-TR-66-220. Aerospace Medical Research Laboratories, Aerospace Medical Division, Air Force Systems Command, Wright-Patterson AFB, Ohio. Published November 1967. Available from Defense Technical Information Center: https://apps.dtic.mil/sti/tr/pdf/AD0667273.pdf

Coleman, Meri, and Liau, T. L. (1975). A computer readability formula designed for machine scoring. *Journal of Applied Psychology*, Vol. 60, pp. 283-284.

Gunning, Robert (1952). *The Technique of Clear Writing*. New York: McGraw-Hill. (Revised editions 1968, 1973.)

Kincaid, J. Peter; Fishburne, Robert P. Jr.; Rogers, Richard L.; and Chissom, Brad S. (1975). *Derivation of New Readability Formulas (Automated Readability Index, Fog Count and Flesch Reading Ease Formula) for Navy Enlisted Personnel*. Research Branch Report 8-75. Chief of Naval Technical Training, Naval Air Station Memphis, Millington, Tennessee. Available from ERIC: https://eric.ed.gov/?id=ED108134 and from DTIC: https://apps.dtic.mil/sti/tr/pdf/ADA006655.pdf

**Validation and Comparative Studies**

Bogert, Judith (1985). In Defense of the Fog Index. *Business Communication Quarterly*, 48(2), 9-12. doi:10.1177/108056998504800203

Bruce, Bertram C.; Rubin, Ann D.; and Starr, Kathleen S. (1981). Why readability formulas fail. *IEEE Transactions on Professional Communication*, PC-24, 50-52.

Hosseinzadeh, Shayan, et al. (2021). Dupuytren's Contracture: The Readability of Online Information. *Journal of Patient Experience*, Volume 8, 1-6.

McLaughlin, G. Harry (1969). SMOG grading: a new readability formula. *Journal of Reading*, Vol. 12, No. 8, 639-646. [Relevant as the formula explicitly designed to supersede Gunning Fog.]

Redish, Janice C. (2000). Readability formulas have even more limitations than Klare discusses. *ACM Journal of Computer Documentation*, 24(3), August 2000, 132-137. Available: https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf

Redish, Janice C., and Selzer, J. (1985). The place of readability formulas in technical communication. *Technical Communication*, 32(4), 46-52.

**Healthcare and Domain Applications**

Antunes, Helder, and Teixeira Lopes, Carla (2019). Analyzing the Adequacy of Readability Indicators to a Non-English Language. *Experimental IR Meets Multilinguality, Multimodality, and Interaction — 10th International Conference of the CLEF Association*. Lugano, Switzerland. hdl:10216/133321.

Paasche-Orlow, Michael K., and Wolf, Michael S. (2007). Evidence does not support clinical screening of literacy. *Journal of General Internal Medicine*, 22(9), 1361-1363. [Background on health literacy context.]

Various authors (2009). The Accuracy of Readability Formulas in Health Content: A Systematic Review. Available: https://www.primescholars.com/articles/the-accuracy-of-readability-formulas-in-health-content-a-systematic-review.pdf [Multiple formulas evaluated against human comprehension ratings; Gunning Fog and FKGL evaluated on diabetes health content.]

**Financial Applications**

Li, Feng (2008). Annual report readability, current earnings, and earnings persistence. *Journal of Accounting and Economics*, 45(2-3), 221-247. [Establishes Gunning Fog as a proxy for deliberate obfuscation in 10-K filings.]

Nature study (2025): Lost in the fog: growing complexity in financial reporting. *Nature*. doi:10.1038/s41599-025-06094-y [Applies Gunning Fog to financial report readability trend analysis.]

**Broader Readability Context**

DuBay, W. H. (2004). *The Principles of Readability*. Impact Information, Costa Mesa, California.

Flesch, Rudolf (1948). A new readability yardstick. *Journal of Applied Psychology*, 32(3), 221-233.

Klare, George R. (1974-76). Assessing readability. *Reading Research Quarterly*, 10(1), 62-102; and second look at validity, *Journal of Reading Behavior*, 8, 129-152. [Foundational critiques of readability formula limitations.]

---

## Notes on Uncertainty and Contested Claims

1. **The exact Senter-Smith constant**: The original 1967 paper uses -21.34 in some references and -21.43 in others. Wikipedia and most modern implementations cite -21.43. The DTIC document itself is partially illegible in the digitized PDF. This discrepancy has not been definitively resolved in the literature reviewed for this report. It is a small but real implementation ambiguity.

2. **Coleman-Liau's claim that "word length in letters is a better predictor than word length in syllables"**: This was Coleman and Liau's empirical finding, but Wikipedia notes "opinion varies on its accuracy as compared to the syllable/word and complex words indices." No definitive meta-analysis settling this claim was found. The claim is plausible but not established as a consensus finding.

3. **Gunning Fog's "complex word" exclusions in modern implementations**: The proper noun exclusion requires either knowing that a word is capitalized (easy to implement but imprecise — capitals also appear at sentence starts) or full named-entity recognition (expensive). Many NLP implementations skip proper noun exclusions. This means Fog scores computed by different tools on proper-noun-heavy text may be incomparable. The compound word exclusion is even more difficult to implement consistently and is often omitted. Readable's implementation should document which exclusions it applies.

4. **The "recalculated" vs. "original" ARI question**: Kincaid et al. (1975) derived updated formulas specifically for Navy personnel reading Navy training materials. These "recalculated" formulas have slightly different coefficients from the original Smith-Senter formula. The Readable implementation should clarify which formula version it uses, as this affects whether claims about military documentation validation are accurate.

5. **Coleman-Liau's counting of punctuation**: Some implementations count punctuation as characters; others count only alphanumeric characters. Coleman and Liau's (1975) paper specified "letters or digits" per the Wikipedia-cited worked example, but other sources describe the formula as counting all non-space characters. This ambiguity exists in the literature and affects scores on punctuation-heavy text.
