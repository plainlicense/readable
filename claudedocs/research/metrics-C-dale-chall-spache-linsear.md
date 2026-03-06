<!--
SPDX-FileCopyrightText: 2026 PlainLicense

SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT
-->

# Research Report: Dale-Chall, Spache, and Linsear Write Readability Formulas

**Prepared for:** Readable Library Documentation
**Date:** 2026-03-05
**Scope:** Historical background, formula mechanics, word list analysis, validated use cases, known limitations, and implementation notes for three readability metrics.

---

## Table of Contents

1. [The Dale-Chall Readability Formula](#1-the-dale-chall-readability-formula)
2. [The Spache Readability Formula](#2-the-spache-readability-formula)
3. [The Linsear Write Formula](#3-the-linsear-write-formula)
4. [Cross-Metric Comparison](#4-cross-metric-comparison)
5. [Implementation Notes: Porter Stemming](#5-implementation-notes-porter-stemming)
6. [References](#6-references)

---

## 1. The Dale-Chall Readability Formula

### 1.1 Background and History

The Dale-Chall Readability Formula was developed by Edgar Dale, professor of education at Ohio State University, and Jeanne Chall, then Dale's research assistant who would later become director of the Harvard Reading Laboratory. Their foundational paper, "A Formula for Predicting Readability," appeared in the *Educational Research Bulletin* in 1948 (Dale & Chall, 1948).

Dale's interest in readability dated to the 1920s, when he was teaching in Winnetka, Illinois, and observed Carleton Washburne and Mabel Vogel working on readability formulas for grading instructional materials (Dale, 1982, cited in Garfield Library citation classic). By the late 1940s, Dale had developed a list of 769 words that 80% of fourth-grade students recognized, and Chall's systematic review of existing readability research gave them the statistical foundation for a formula.

Their explicit motivation was to improve on Rudolf Flesch's formula (Flesch, 1948), which used word length as a proxy for difficulty. Dale and Chall argued that using syllable counts or character counts is a crude proxy: a long word familiar to most readers should not be penalized; a short word unknown to readers should be flagged. Their answer was the word list approach.

#### The 1995 Revision

The word list was later revised by Dale. According to one primary source account, Dale compiled an updated list in 1984 using the same criterion (words recognized by 80% of fourth graders), but he died before the revision could be published. Jeanne Chall published the revised formula and expanded list posthumously in 1995 as *Readability Revisited: The New Dale-Chall Readability Formula* (Chall & Dale, 1995, Brookline Books).

The 1995 revision made several specific changes:

- **Word list expansion:** from 763-769 words to approximately 3,000 words
- **Inflection handling formalized:** The original list contained only base forms of verbs and nouns. The 1995 revision explicitly documented which inflections of listed words count as familiar (e.g., regular plurals, past tense, progressive forms, comparative/superlative endings: -s, -es, -ed, -ing, -er, -est) and which do not (e.g., derivational suffixes that create new words: -tion, -ation, -ment, -ly, -y)
- **Simplified instructions:** The 1995 book included worksheets combining the formula with assessments of cognitive complexity, reader characteristics, and reading purpose
- **New criterion passages:** The regression was recalibrated using updated text samples

Importantly, the 1995 revision kept the same formula coefficients as the 1948 original. The formula did not change; the word list and surrounding documentation did.

### 1.2 The Formula Explained

The formula measures two things: how many words in a text are unfamiliar to a typical 4th-grade American reader, and how long the sentences are on average.

**Formula (1948/1995):**

```
raw_score = 0.1579 × (difficult_words / total_words × 100) + 0.0496 × (total_words / total_sentences)

adjusted_score = raw_score + 3.6365  (if percent difficult words > 5%)
adjusted_score = raw_score            (otherwise)
```

The adjustment for texts with more than 5% difficult words reflects a non-linear reality: once unfamiliar words become frequent enough to disrupt reading fluency, comprehension difficulty does not increase at a steady rate.

**Score-to-grade mapping:**

| Score | Grade Level |
|-------|-------------|
| 4.9 and below | Grades 1-4 |
| 5.0 - 5.9 | Grades 5-6 |
| 6.0 - 6.9 | Grades 7-8 |
| 7.0 - 7.9 | Grades 9-10 |
| 8.0 - 8.9 | Grades 11-12 |
| 9.0 - 9.9 | College (13-15) |
| 10.0 and above | College graduate (16+) |

The formula was designed for text aimed at readers above 4th grade. Texts scored at 4.9 or below are appropriate for elementary readers; the formula does not differentiate within that band (grades 1 through 4 all map to the same score range).

**Why word familiarity instead of syllables or characters?**

The theoretical argument is that what makes a word cognitively difficult for a reader is unfamiliarity, not length per se. The word "catastrophic" has five syllables and would be penalized heavily by Flesch-Kincaid; a frequent reader who knows the word would not find it hard. Conversely, the word "waive" has one syllable and is familiar-sounding, but many fourth-graders do not know its legal meaning. Only word-list approaches distinguish these two cases. As Chall and Dale (1995, p. 84) wrote: "It is no accident that vocabulary is also a strong predictor of text difficulty."

### 1.3 The Word List: What Is and Is Not On It

The Dale-Chall word list is empirically grounded: each word was included because 80% or more of 4th-grade American students said they knew it during data collection. This grounding in actual reader knowledge makes the list philosophically sounder than frequency-based approaches alone. However, it introduces specific quirks:

**What is on the list (examples):** Basic common words like "a," "the," "no," "yes," everyday objects (apple, chair, dog), common verbs in base form (run, eat, see), numbers, colors, and names of common animals. More surprisingly, rural or agricultural words reflecting mid-20th-century American life also appear: "bushel," "haystack," "harness," "reap."

**What is not on the list:** Words that did not exist in 1948 or 1984, or were not sufficiently common among 4th graders at the time of testing. This means no "email," "internet," "smartphone," "streaming," "website," or "social media." Technical terminology from domains that have grown since the 1980s is largely absent.

**The polysemy problem (critical for software documentation):** The word list contains words, but not word senses. The word "cookie" on the Dale-Chall list refers to the baked good. A browser cookie is not the same referent. The word "enter" appears on the list because children know "enter the room," but a software instruction to "press Enter" may invoke a different cognitive process. As Ginny Redish (UX expert) and others have argued, the Dale-Chall formula cannot distinguish these cases; it would score both "cookie" uses identically, even though the technical usage requires prior domain knowledge (Redish, 2019).

**Inflection rules:** A word on the list with regular plural, past tense, or progressive forms is treated as familiar in those forms. But derivational changes that create new words are treated as difficult. For example:
- `complete` (on list) + `-tion` = "completion" (counted as difficult)
- `judge` (on list) + `-ment` = "judgment" (counted as difficult)
- `normal` (on list) + `-ly` = "normally" (counted as difficult)

This creates an interesting phenomenon: a text that uses abstract nouns (-tion, -ment words) will score higher difficulty even if the root words are all familiar.

**Proper nouns:** Both the 1948 and 1995 versions treat proper nouns (names of people and places) as familiar words. This is explicitly stated in the Dale-Chall computation guidelines: "The names of people and places (whether or not they appear on the word list) are considered familiar words" (Dale-Chall worksheet, Wright Online). Whether this is correct is debated; unfamiliar proper nouns can disrupt fluent reading (Brown, 2010).

### 1.4 Strengths

**Theoretically grounded word difficulty:** Of all the classical readability formulas, Dale-Chall has the strongest theoretical basis for its word difficulty component. It measures what readers actually know, not a proxy for what they might know.

**Best-validated for educational content:** Multiple research reviews find that Dale-Chall has the highest validity for educational materials when validated against actual comprehension (Assessing Readability of Patient Education Materials, PMC, 2011). One review states: "The New Dale-Chall Readability formula was developed specifically for evaluating health education materials and has the highest validity when tested for reader comprehension."

**Sensitive to vocabulary that syllable-count formulas miss:** It can distinguish "wave" from "waive" - a distinction no syllable-count formula makes (Redish, 2019).

**Works across a wide grade range:** Unlike Spache (limited to grades 1-4), Dale-Chall covers grades 4 through college graduate level, making it useful for a broader range of texts.

**Used in health communications research:** It is one of the most cited formulas in patient education materials research, where ensuring comprehension by patients with limited health literacy is a genuine public health concern.

### 1.5 Weaknesses and Biases

**The word list aging problem:** The 1995 list reflects word familiarity among American 4th graders in approximately 1984. A quantitative analysis cited in a *Chance* magazine article on readability formulas found that 31% of the Dale-Chall "easy" words have declined in popularity since the list was constructed (as measured by Google N-gram frequencies). Words reflecting mid-20th-century rural life (bushel, haystack) are likely less familiar to contemporary children; words reflecting contemporary digital life (email, app, wifi) are not on the list at all. The implication is that the list systematically underestimates the difficulty of texts containing agricultural or historical vocabulary, and overestimates the difficulty of texts using familiar contemporary terminology not yet on the list.

**Semantic drift:** Words on the list have acquired new meanings not intended by Dale and Chall. "Cookie," "virus," "stream," "feed," "cloud," "network," "enter," "execute," "crash" all appear in technical contexts where the familiar meaning is not the technical meaning. The formula treats these as familiar words even when the technical sense is what matters.

**Domain-specific vocabulary problem:** A cardiologist reading a medical journal does not find "myocardial" difficult; an expert petroleum engineer does not find "stratigraphic" difficult. Domain expertise overrides word familiarity in ways the word list cannot account for. Research on credentialing examinations (Badgett, 2010, cited in ALPINETESTING) explicitly found that occupational-specific terminology that experts recognize is falsely scored as "difficult" by Dale-Chall, artificially inflating difficulty estimates for domain-expert audiences.

**Lower bound limitation:** The formula is not designed for texts below grade 4. Its score range does not differentiate between kindergarten and 4th-grade texts. Use Spache for primary-grade material.

**U.S.-centric:** The word list reflects what American 4th-grade students knew in the 1980s. It has inherent cultural and geographic bias: words common in American English but not in British, Australian, or other English varieties may appear or be absent in ways that distort scores.

**Inter-formula disagreement:** A study comparing seven readability formulas applied to elementary social studies textbooks found no universal agreement in rank-ordering difficulty, with wide discrepancies leaving the same textbook rated several grade levels apart by different formulas (Chen, 1986, cited in Readability of Texts: State of the Art). This is partly because Dale-Chall weights vocabulary over sentence length, while other formulas do the reverse.

**Counterintuitive results for literary texts:** The Chance article cited a demonstration where Shakespeare's "All the World's a Stage" monologue scored more readable (lower grade level) than either the standard or simplified Wikipedia articles about Shakespeare. This is because Shakespeare used primarily monosyllabic, common words. Dale-Chall's inability to handle syntactic complexity (inverted word order, archaic constructions) produces misleading scores for literary texts.

### 1.6 Best Use Cases

- Educational materials for grades 4 and above, where matching text to reader level is the explicit goal
- Patient education materials, health pamphlets, consumer health information
- Government documents and public information materials intended for general adult audiences
- Children's and young adult literature assessment
- Legal notices and consumer disclosure documents intended to be comprehensible to the general public
- Any context where the audience is general adults (not domain experts) and vocabulary familiarity is the primary concern

### 1.7 What Dale-Chall Is NOT Good For

- Technical documentation aimed at domain experts (it will falsely flag expert vocabulary as "difficult")
- Software documentation and user interfaces (polysemy problems with technology terms)
- Texts containing significant contemporary vocabulary not on the 1984 list
- Primary-grade texts (grades 1-3): use Spache instead
- Literary or poetic texts where syntactic complexity, archaic constructions, or deliberate style choices affect comprehension in ways the formula cannot detect
- Non-English text (the formula is English-only by design)
- Very short texts (fewer than 100 words): sampling noise becomes significant

---

## 2. The Spache Readability Formula

### 2.1 Background and History

George Spache, an educational psychologist, introduced his formula in 1953 in "A New Readability Formula for Primary-Grade Reading Materials," published in *The Elementary School Journal* (Spache, 1953). The title is precisely accurate: this was a formula designed from the ground up for primary-grade materials, filling a gap that Spache explicitly identified.

In his original paper, Spache noted that the three most widely used readability formulas of the time -- Flesch, Lorge, and Dale-Chall -- could not meaningfully assess texts intended for readers below 4th grade. They were calibrated on older readers, used criterion measures from adult contexts, and their grade-level outputs became unreliable at the low end. Primary-grade texts needed a purpose-built tool.

Spache's empirical foundation was a corpus of 224 samples of 100 words each drawn from 152 books commonly used in grades 1-3. He found something noteworthy: for primary-grade materials, sentence length was slightly more closely related to reading difficulty than vocabulary load. This contrasts with studies of materials for older readers (including Dale and Chall's own findings), where vocabulary carries more weight. The difference makes intuitive sense: primary readers are still developing fluency, and sentence length directly constrains working memory demands during early decoding.

Clarence R. Stone published a constructive criticism of the formula in 1956 (Stone, 1956), and in 1978, Spache himself revised the formula, explicitly acknowledging that a readability formula must evolve as language and education change:

> "If a readability formula is to continue to reflect accurate estimates of the difficulty of today's books, it, too, must change. That is, a formula validated with one group of students and one type of texts is found to be invalid for the same types of students and texts as conditions change over a 25-year period." (Spache, 1978, cited in Why Readability Formulas Fail, IDEALS)

This is a remarkably candid admission from the formula's own creator, and it applies with equal force today.

### 2.2 The Formula Explained

The formula computes a grade level from average sentence length and the percentage of unfamiliar words, where familiarity is defined by the Spache word list.

**Original formula (Spache, 1953):**

```
Grade Level = 0.141 × ASL + 0.086 × PDW + 0.839
```

**Revised formula (Spache, 1978):**

```
Grade Level = 0.121 × ASL + 0.082 × PDW + 0.659
```

Where ASL = average sentence length (words per sentence), and PDW = percentage of unique difficult words (words not on the Spache list, counted only once per text regardless of repetition).

Note the key difference in counting methodology: **Spache counts each unique unfamiliar word once**, while Dale-Chall counts each occurrence of every unfamiliar word. This means Spache is less sensitive to repetition of unfamiliar vocabulary, which is arguably appropriate for primary-grade texts where controlled vocabulary repetition is a deliberate instructional strategy.

The 1978 revision reduced both the sentence length coefficient (0.141 to 0.121) and the vocabulary coefficient (0.086 to 0.082), and lowered the constant (0.839 to 0.659). The practical effect is that the revised formula generally produces slightly lower grade estimates than the original. This was recalibrated against updated text samples.

**Grade range:** The formula produces scores approximately between grades 1 and 4. A score of 4.0 or above indicates the text may exceed the formula's reliable range and should be assessed with Dale-Chall instead.

This library implements the original 1953 formula, which is the most widely cited version in formal contexts.

### 2.3 The Word List

The Spache word list contains approximately 925 words in its 1978 revised form. These are words familiar to primary-grade readers -- simpler and fewer in number than the Dale-Chall list, reflecting the more constrained vocabulary of young children.

The list consists predominantly of: common monosyllabic and disyllabic words, basic action verbs, common nouns for everyday objects and family members, basic function words, and common animals. Words like "said," "went," "little," "mother," "house," "dog," "happy," and "water" are representative.

**What is on the Spache list (sample):** a, able, about, across, act, add, afraid, after, again, air, all, almost, alone, already, also, always, among, angry, animal, another, answer, any, apple, arm, around, ask, asleep, at...

**What is not on the Spache list:** Most polysyllabic words, abstract concepts, technical or academic vocabulary, and words outside the core vocabulary of primary-grade reading instruction. Even many common words that a 3rd-grader might know are absent if they did not appear frequently enough in primary-grade reading materials of the 1950s-1970s.

**Variant form handling:** The Spache computation rules allow regular verb endings (-ing, -ed, -es) and regular plural and possessive endings as familiar forms of listed words. Adverbial, comparative, and superlative endings (-ly, -er, -est) are also recognized. Irregular forms are treated as difficult unless they independently appear on the list.

**First names:** Like Dale-Chall, Spache treats all first names as familiar words.

### 2.4 Strengths

**Purpose-built for its audience:** Spache is the only classical formula explicitly calibrated on primary-grade reading materials, using primary-grade texts as its corpus and primary-grade students as its validation population. This makes it more appropriate than any formula adapted from older-reader research.

**Corpus-validated calibration:** Spache's finding that sentence length matters more for primary readers than for older readers is empirically grounded in his 224-sample corpus. The formula's coefficients reflect this empirical reality.

**Sensitive to sentence length at the critical developmental stage:** For new readers learning to decode, sentence length directly loads working memory in ways that formula can detect. Short sentences are genuinely easier for beginning readers.

**Complementary to Dale-Chall:** The two formulas cover adjacent grade bands with compatible methodology. When applied together, they provide coverage from grade 1 through college. Fry's Readability Graph comparison studies showed the Spache formula correlates reasonably well with the Fry graph and the cloze procedure for primary-grade materials (ERIC, 1968 study).

### 2.5 Weaknesses and Biases

**The word list aging problem (acute for Spache):** The Spache word list reflects primary-grade vocabulary norms from the early 1950s. The 1978 revision helped, but the core list still predates digital life, contemporary children's media, and significant changes in children's vocabulary exposure. A 2019 analysis (*Chance* magazine article on readability formulas) found that 26% of the Spache "easy" words have declined in popularity since the list was constructed. Children today may not know "harness," "sled," or "rye" but would recognize "tablet," "video," and "app" - none of which are on the list.

**Hard upper ceiling:** The formula produces reliable estimates only up to approximately grade 4. A text at the 4th-grade level is at the outer edge of the formula's validated range. Above that, use Dale-Chall. This creates a practical problem: children develop rapidly during grades 1-4, and the formula's limited range means it cannot guide text selection across that entire span with fine-grained discrimination.

**Unique-word counting obscures vocabulary density:** Counting each unfamiliar word only once means a text could use "photosynthesis" twenty times and it counts as one difficult word. This can underestimate difficulty for texts with repeated specialized vocabulary. For primary-grade instructional text, this may be acceptable (controlled vocabulary is intentional); for other uses, it can mislead.

**Syntactic complexity not captured:** The formula does not capture syntactic complexity beyond sentence length. The famous counterexample: the children's book *Don't Forget the Bacon* (Hutchins, 1976) scores at grade level 2.7 using Spache, yet some 4th-graders find it genuinely difficult because the narrative structure requires distinguishing between a character rehearsing a list and correcting himself -- a comprehension task well beyond what sentence length or word familiarity predicts (Why Readability Formulas Fail, IDEALS).

**Cultural and dialectal bias:** The word list was constructed from mid-20th-century American English children's literature and primary-grade reading materials. It reflects the vocabulary exposure of American children in that era and cultural context. Children from non-English-speaking households, or children from regions where certain words are used differently, may have familiarity profiles that differ from what the list assumes. As Spache (1978) himself acknowledged: "The effects on validity of the formula for readers having different cultural backgrounds or dialects must be considerably greater" than the 25-year temporal drift he was already correcting for.

**Small word list increases noise:** With only ~925 words, the Spache list is a coarser instrument than Dale-Chall's 3,000-word list. Any given unfamiliar word in a short text has more impact on the final score, making the formula more volatile on short texts.

**Self-acknowledged assumption never validated:** Spache himself stated that the formula "should mean that a child with that level of reading ability could read the book with adequate comprehension and a reasonable number of oral reading errors. This assumption has seldom if ever been tested" (Spache, 1978, quoted in Why Readability Formulas Fail). This is a fundamental caveat about what the score actually predicts.

### 2.6 Best Use Cases

- Primary-grade reading materials (grades 1-3), especially children's books and early reader texts
- Children's picture books and leveled readers where vocabulary control is deliberate
- Early literacy instructional materials where matching text to developing reader level is critical
- Educational assessment of books being considered for classroom use in grades K-3
- Children's health information materials designed for early readers
- Any context where the target audience is beginning readers and vocabulary familiarity is paramount

### 2.7 What Spache Is NOT Good For

- Texts intended for readers above grade 4: the formula is not calibrated for this range
- Adult texts of any kind: the word list and calibration are entirely inappropriate
- Technical or specialized texts regardless of simplicity: domain vocabulary is absent from the word list
- Texts containing significant contemporary vocabulary (digital, media-related terms)
- Texts where the target reader is a non-native speaker of English: the list assumes native-language primary-school vocabulary exposure
- Assessment of picture books or texts where illustrations carry significant comprehension load (formula is text-only)

---

## 3. The Linsear Write Formula

### 3.1 Background and History

**Important attribution note:** Linsear Write is frequently attributed to the US Air Force, and many sources (including calculator websites) describe it as "developed for US Air Force technical manuals." This attribution appears to be incorrect or at least imprecise. The formula's actual primary source is:

> O'Hayre, J. (1966). *Gobbledygook Has Gotta Go*. Bureau of Land Management, US Department of the Interior, Washington, DC.

O'Hayre was a government employee working at the Bureau of Land Management's Western Information Office, not for the Air Force. The full text of the manual is publicly available at governmentattic.org and blm.az.gov. Wikipedia's own Linsear Write article uses the word "purportedly" when attributing it to the Air Force -- this hedging reflects genuine uncertainty about the secondary attribution.

The confusion may stem from the fact that other readability formulas (notably the Automated Readability Index and later the Flesch-Kincaid derivation) were developed by or for military services. The Linsear Write formula may have been adopted by Air Force technical writing programs at some point, but O'Hayre's Bureau of Land Management origin is the documented primary source.

**O'Hayre's motivating philosophy:** The manual's title, *Gobbledygook Has Gotta Go*, signals that O'Hayre was a plain-language advocate, not primarily a readability researcher. His concern was government writing that was bureaucratic, passive-voice-laden, and impenetrable. He described the formula as measuring "writeability" more than readability: the goal was to train writers to use active verbs and direct language, not merely to assess what readers could comprehend.

His description of the formula's purpose is illuminating: "Rather than counting every syllable or only words of three syllables or more, we concentrate on words which make up nearly three-fourths of plain English, the words most natural to the language, especially its native nouns and verbs, its one-syllable words." He argued that monosyllabic words are the backbone of plain English, and that writing in them forces the writer toward active, direct expression.

**The connection to George Klare:** Klare (1974) cited the Linsear Write formula in his seminal review "Assessing Readability" in *Reading Research Quarterly*, which is likely how it gained wider circulation in the academic readability literature.

**The O'Hayre formula vs. the grade-level formula:** There are two distinct versions of Linsear Write:

1. **O'Hayre's original (1966):** A writing feedback scale, not a grade-level predictor
2. **The grade-level conversion (authorship uncertain):** A formula that produces a U.S. grade level

Who converted the formula to a grade-level output is not documented in the sources reviewed. CheckReadability.com notes: "It's unclear who converted Linsear Write to a grade-level version or when this happened -- whether it was John O'Hayre or another linguist."

### 3.2 The Formula Explained

**O'Hayre's original formula (writing quality scale):**

1. Take a 100-word sample
2. Count all one-syllable words, excluding "the", "is", "are", "was", and "were"
3. Count all sentences, multiply by 3
4. Sum the one-syllable word count and the sentence score
5. Interpret: 70-80 = appropriate for average adult reader; 80 = ideal; above 85 = too simple; below 70 = too complex (unless writing for specialists)

Note that O'Hayre explicitly excluded the five listed function/auxiliary verbs because they frequently appear in passive constructions. By "emphasizing them out," the formula nudges writers away from passive voice. This is as much a style guide heuristic as a readability measure.

**The grade-level version (modern implementation):**

1. In a 100-word sample: for each easy word (1-2 syllables), add 1 point; for each hard word (3+ syllables), add 3 points
2. Divide the total points by the number of sentences in the sample
3. Adjust the provisional result (r):
   - If r > 20: Lw = r / 2
   - If r ≤ 20: Lw = (r - 2) / 2

The result is a U.S. grade level. A score of 10 corresponds to approximately 10th grade.

**Implementation note (this library):** The library applies the grade-level formula to the entire text rather than to a 100-word sample:

```python
num_easy_words = stats.num_words - stats.num_poly_syllable_words
num_hard_words = stats.num_poly_syllable_words
inter_score = (num_easy_words + (num_hard_words * 3)) / stats.num_sentences
if inter_score > 20:
    return inter_score / 2
return (inter_score - 2) / 2
```

The `_score()` implementation uses `num_poly_syllable_words` for hard words (3+ syllables) and all remaining words as easy words. The code comment acknowledges this is "an approximation based on the original library's implementation." This divergence from the 100-word sampling methodology is a practical choice that affects comparability with hand-calculated scores.

**Why syllable count instead of word lists?** O'Hayre's rationale was explicitly anti-syllable-counting for most words: he wanted to reward monosyllabic words, not penalize polysyllabic ones across the board. His insight was that a text full of one-syllable words plus active verbs is probably in plain English; a text with many three-plus-syllable words probably is not. He was not trying to replicate the word-familiarity approach of Dale or Spache; he was trying to change writing behavior.

### 3.3 Strengths

**Simple to compute:** The formula requires only syllable counting and sentence counting. No word lists needed. It can be applied to any domain without concern about whether the word list is appropriate.

**Domain-agnostic:** Unlike Dale-Chall and Spache, Linsear Write makes no assumptions about which words are "familiar." A text dense with three-syllable technical terms scores as difficult regardless of whether the intended audience knows those terms -- which may be the right behavior for audience-independent style checking.

**Useful as a writing feedback tool:** O'Hayre designed it to change writer behavior. Running a draft through Linsear Write and noticing a high proportion of hard words identifies specific revision targets -- words to simplify or replace.

**Computationally robust:** Because it uses no external word lists, it cannot be invalidated by language change in the way word-list formulas can. "Smartphone" is three syllables and counts as hard; "app" is one syllable and counts as easy -- which is arguably correct regardless of when the word entered common use.

**Good fit for technical writing assessment:** For technical documentation where the concern is sentence complexity and polysyllabic jargon density, Linsear Write provides a straightforward structural assessment without importing educational norms about what readers "should" know.

### 3.4 Weaknesses and Biases

**Small sample size problem:** The formula was designed around a 100-word sample. This sample size is prone to high variance. A single long sentence or a paragraph-dense with technical terms can swing the score significantly. The library mitigates this by operating on the full text, which averages across samples and reduces variance -- but this is a deviation from the formula's designed methodology.

**Syllable count as a crude proxy:** The fundamental limitation of syllable-counting approaches (shared with Flesch-Kincaid, SMOG, ARI) is that syllable count correlates with, but does not equal, word difficulty. "Cat" (one syllable) is easier than "gauge" (one syllable). "Photosynthesis" (five syllables) is harder than "beautiful" (three syllables) for most readers. The correlation is real but imperfect.

**No distinction between familiar and unfamiliar polysyllabic words:** The word "beautiful" and "perpendicular" both have four syllables and receive the same hard-word score, even though "beautiful" is known to most 2nd-graders. Linsear Write cannot make this distinction; Dale-Chall can.

**The grade-level conversion is not well-validated:** Testing has shown the grade-level version "can sometimes be off by two grade levels" compared to the original O'Hayre scale (CheckReadability.com). The conversion's authorship is unknown, and its validation against actual reading comprehension is not documented in the sources reviewed for this report. Academic reviews of health content readability assessment explicitly excluded Linsear Write from some systematic reviews due to limited supporting evidence (Accuracy of Readability Formulas in Health Content, PrimeScholars).

**Not designed for comprehension prediction:** O'Hayre was a plain-language advocate designing a writer's tool. He was explicit that he was shifting emphasis "from readability to writeability." Using the formula as a predictor of reader comprehension stretches it beyond its original purpose.

**Passive-voice heuristic baked in (original version):** The exclusion of "is," "are," "was," "were" in the original formula is a style prescription, not a neutral measurement. The grade-level version drops this exclusion entirely. This means the two versions measure subtly different things.

**Similar to Fry graph but less validated:** Wikipedia notes that Linsear Write is "similar to the Fry readability formula," and indeed both focus on syllables and sentence length. Fry's graph has substantially more validation research behind it. Where both are applicable, Fry may be preferable for its better-documented reliability.

### 3.5 Best Use Cases

- Technical writing assessment where the concern is polysyllabic jargon density
- Government and internal communications where plain-language goals align with O'Hayre's original intent
- Rapid, rough-and-ready readability assessment without word list dependencies
- Creative writing and journalism where domain-specific word lists would be inappropriate
- Comparative assessment within a consistent domain (comparing two technical documents against each other)
- Cases where no appropriate word list exists for the domain

### 3.6 What Linsear Write Is NOT Good For

- Definitive grade-level assessment: the formula lacks validation at the level of Dale-Chall or Flesch-Kincaid
- Primary-grade texts: it is not calibrated for children's reading
- Health and medical communications where validated formulas (SMOG, Dale-Chall) are preferred by professional guidelines
- Legal readability assessment, where validity is important and better-validated alternatives exist
- Short texts: the 100-word sample requirement means very short texts cannot be meaningfully assessed
- Distinguishing familiar from unfamiliar polysyllabic words: all three-plus-syllable words are treated identically

---

## 4. Cross-Metric Comparison

### 4.1 Dale-Chall vs. Spache: Same Approach, Different Populations

Dale-Chall and Spache share a fundamental methodology: both use a word list to identify unfamiliar words and combine that with average sentence length. Their key differences are:

| Feature | Dale-Chall | Spache |
|---------|-----------|--------|
| Target grade range | 4+ through college | 1-4 |
| Word list size | ~3,000 words | ~925 words |
| Difficult word counting | Every occurrence | Each unique word once |
| Sentence vs. vocab weight | Vocabulary weighted more | Sentence length weighted more (per calibration) |
| Word list currency | 1984, revised 1995 | 1953, revised 1978 |
| Proper nouns | Treated as familiar | Treated as familiar |

The appropriate choice between them is straightforward: **Spache for grades 1-4, Dale-Chall for grades 4 and above.** At grade 4, they should be applied together -- Spache to check the text is not too complex, Dale-Chall to confirm it is not too simple for the intended grade.

An ERIC study comparing the Spache formula with the Fry Readability Graph found "highly consistent correlations for all four methods" (Spache, Fry, cloze, oral reading) for primary-grade books, suggesting that for this range, multiple approaches converge.

A comparative study of readability formulas applied to science-based texts found that Spache and Dale-Chall do NOT correlate well with each other or with Flesch-Kincaid across grade levels (correlation coefficient r between Spache and Dale-Chall: -0.13 for online articles; 0.39 for trade books). This low correlation reflects their non-overlapping grade bands: the formulas are not redundant but complementary.

### 4.2 Word-List Metrics vs. Syllable-Counting Metrics: A Philosophical Difference

There are two fundamentally different theories of what makes a word "difficult":

**Theory 1 (word-list approach):** A word is difficult if readers are unfamiliar with it. Familiarity is an empirical fact that can be tested. Dale-Chall and Spache implement this theory.

**Theory 2 (structural proxy approach):** Word length (in syllables or characters) correlates with difficulty in general populations. Longer words tend to be rarer and more technical. Flesch, ARI, Coleman-Liau, and SMOG implement this theory.

Neither theory is always right. The word-list approach is more accurate for the specific population tested to build the list; the structural proxy approach is more durable over time and across domains. In practice:

- Word-list formulas are more valid for educational and general-audience contexts
- Syllable-count formulas are more robust to language change and domain shift
- Linsear Write occupies a middle ground: it is structural, but was designed for a specific context (government plain-language writing)

**When to choose Dale-Chall over Flesch or SMOG:**
- When the audience is known to be general adults or children (not domain experts)
- When the text is educational or informational, not technical
- When vocabulary familiarity is the primary concern (not just word length)
- When validated comprehension prediction is important (Dale-Chall has more validation research for educational content)

**When to choose Flesch, SMOG, or ARI over Dale-Chall:**
- When the audience is unknown or mixed (general population)
- When the text contains significant domain-specific vocabulary that experts would know but the word list would flag
- When language change makes the word list unreliable (contemporary technology topics)
- When healthcare communication follows established guidelines preferring SMOG (SMOG is recommended for health materials in many professional guidelines due to its 100% comprehension calibration)

### 4.3 Linsear Write's Niche

Linsear Write sits apart from Dale-Chall and Spache in that it does not use a word list and was not designed for educational grade-level prediction. It is best understood as a style tool rather than a readability predictor. Its niche is:

- Writing process feedback for technical or government writers
- Quick polysyllabic-density assessment
- Domain contexts where no appropriate word list exists

For serious readability assessment, it should be used alongside at least one other metric. It should not be the sole measure for high-stakes readability decisions.

---

## 5. Implementation Notes: Porter Stemming

### 5.1 What the Library Does

The Readable library uses Porter-stemmed versions of both the Dale-Chall and Spache word lists (stored in `readable/resources/data/` as `dale_chall_porterstem.txt` and `spache_easy_porterstem.txt`). When analyzing a text, each word is Porter-stemmed via NLTK's `PorterStemmer` before being checked against the word list:

```python
# From readable/resources/stemmer.py
return self._porter_stemmer.stem(word.lower())
```

This means that "running" → "run" → checked against the stemmed list; if "run" is in the stemmed Dale-Chall list, "running" is counted as familiar.

### 5.2 The Rationale

The word lists contain base forms of words (e.g., "run" but not "running," "eat" but not "eaten"). Without stemming, every inflected form not explicitly listed would be counted as "difficult," dramatically inflating difficulty scores. The original Dale-Chall and Spache computation guidelines handle this by explicitly enumerating which regular inflections are acceptable variants of listed words.

The library's stemming approach is a computational approximation of this enumeration. Rather than explicitly handling every inflectional suffix, it reduces words to approximate stems and checks the stemmed form.

### 5.3 Is This Validated?

No readability formula research reviewed for this report validates Porter stemming specifically as the correct approach to inflection handling for Dale-Chall or Spache. It is a practical engineering choice that is not documented in the original papers.

**Known limitations of Porter stemming in this context:**

1. **Over-stemming:** Porter stemming can be aggressive. Words like "operate," "operates," "operating," "operation," "operational," and "operative" all reduce to the same stem. If "operate" is on the word list (it is not, but hypothetically), "operation" would be counted as familiar even though it is a different word with different usage.

2. **Non-word stems:** Porter stemming sometimes produces stems that are not English words (e.g., "happi" for "happy"). If the word list contains "happi" as a stemmed entry, matching works; if it contains "happy," the match fails. The library's use of pre-stemmed word lists addresses this: the word lists are themselves Porter-stemmed, so stemmed forms in text are matched against stemmed forms in the list.

3. **Semantic mismatch on derivational morphology:** The original Dale-Chall rules treat derivational suffixes (-tion, -ment, -ly, -y) as creating new "difficult" words. Porter stemming may sometimes over-reduce, treating these derived forms as equivalent to their bases. For example, "completion" might stem to something close to "complet," and "complete" would also stem to "complet" -- if the stemmed list contains that form, "completion" would be counted as familiar when Dale-Chall's original rules would count it as difficult.

4. **Under-stemming:** Some inflected forms may not be correctly normalized, leading to words being counted as difficult when they should be familiar.

**Bottom line:** The Porter-stemmed word list approach is a reasonable engineering compromise that works acceptably for most texts. It is not a validated replication of the original manual computation procedure. For high-precision readability assessment against the original Dale-Chall or Spache methodology, the library's scores may diverge slightly from hand-calculated scores.

Developers who need high fidelity to the original computation procedures should consider implementing the explicit inflection rules from the original papers alongside a lookup against unstemmed base forms.

---

## 6. References

The following citations distinguish primary sources, peer-reviewed research, and secondary web sources.

### Primary Sources

- Dale, E., & Chall, J.S. (1948). A formula for predicting readability. *Educational Research Bulletin*, 27(1/2), 11-20, 37-54.

- Dale, E. (1982). Citation Classic commentary on the above. *Current Contents*, April 19, 1982. [Available via Garfield Library, University of Pennsylvania]

- Chall, J.S., & Dale, E. (1995). *Readability Revisited: The New Dale-Chall Readability Formula*. Brookline Books. ISBN: 1571290087.

- Spache, G. (1953). A new readability formula for primary-grade reading materials. *The Elementary School Journal*, 53(7), 410-413. doi:10.1086/458513

- Spache, G. (1978). Revision of the Spache Readability Formula. [Referenced in: Why Readability Formulas Fail, IDEALS, University of Illinois]

- O'Hayre, J. (1966). *Gobbledygook Has Gotta Go*. Bureau of Land Management, US Department of the Interior, Washington, DC. [Available at governmentattic.org and az.blm.gov]

### Peer-Reviewed Research and Academic Sources

- Brown, J. (2010). An improper assumption? The treatment of proper nouns in text difficulty measures. *Reading in a Foreign Language*, 22(2). [University of Hawaii]

- Chall, J.S., & Dale, E. (1995). Readability revisited, the new Dale-Chall readability formula. [As cited in Readability of Texts: State of the Art, *Theory and Practice in Language Studies*, 2012]

- Klare, G.R. (1974). Assessing readability. *Reading Research Quarterly*, 10(1), 62-102. doi:10.2307/747086

- Plavén-Sigray et al. (2017). The readability of scientific texts is decreasing over time. *eLife*, 6, e27725. [Available via eLife Sciences]

- Stone, C.R. (1956). Measuring difficulty of primary reading material: A constructive criticism of Spache's measure. *The Elementary School Journal*, 57(1), 36-41.

- Why Readability Formulas Fail. (ca. 1981). [IDEALS, University of Illinois at Urbana-Champaign. Available at ideals.illinois.edu]

- Why Readability Formulas Fail. (1980). [ERIC document ED205915]

- Assessing Readability of Patient Education Materials. (2011). *PubMed Central*, PMC3049622. [NIH/PMC]

- A large-scaled corpus for assessing text readability. (2023). *PubMed Central*, PMC10027808.

- Evaluating the Evaluators: Are readability metrics good measures of readability? (2025). arXiv:2508.19221.

- The Use of Readability Metrics in Legal Text: A Systematic Review. (2024). arXiv:2411.09497.

- The Accuracy of Readability Formulas in Health Content: A Systematic Review. *Prime Scholars*.

- A Comparison of Readability in Science-Based Texts. (2017). *Canadian Journal of Education*, 40(1). [ERIC EJ1136164]

- Badgett, C. (2010). [Credentialing examination readability research]. Cited in: READABILITY OF CREDENTIALING EXAMINATIONS MATERIALS. Alpine Testing Solutions.

- Chen, W.S. (1986). A comparison of seven computerized readability formulas as applied to elementary social studies textbooks. Unpublished doctoral dissertation, Columbia University. [Cited in Readability of Texts: State of the Art]

- The readability of federal land management plans. *Environmental Management*. doi:10.1007/BF01867589 [Springer; cites O'Hayre, 1966]

- Plain Language in the US Gains Momentum: 1940-2015. Schriver, K. *Karenschriverassociates.com*.

### Secondary Web Sources (Quality Reference Sites)

- Wikipedia: Dale-Chall readability formula. https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula

- Wikipedia: Spache readability formula. https://en.wikipedia.org/wiki/Spache_readability_formula

- Wikipedia: Linsear Write. https://en.wikipedia.org/wiki/Linsear_Write

- ReadabilityFormulas.com: The Dale-Chall 3000 Word List. https://readabilityformulas.com/word-lists/the-dale-chall-word-list-for-readability-formulas/

- ReadabilityFormulas.com: The Spache Readability Formula for Young Readers.

- ReadabilityFormulas.com: Learn about the Linsear Write Readability Formula.

- Redish, J.G. (2019). Readability Formulas: 7 Reasons to Avoid Them. *UX Matters*. https://www.uxmatters.com/mt/archives/2019/07/readability-formulas-7-reasons-to-avoid-them-and-what-to-do-instead.php

- Redish, J.G. / Effortmark (same article, UK publication). https://www.effortmark.co.uk/readability-formulas-seven-reasons-to-avoid-them-and-what-to-do-instead/

- Smeaton & Hamill (source of the *Chance* magazine article cited): The Past, Problems, and Potential of Readability Analysis. https://www.jhanley.biostat.mcgill.ca/bios601/Surveys/ReadabilityChanceMagazineArticle.pdf

- Gorby.app: Spache Readability Formula Calculator. https://gorby.app/readability/spache-readability-formula/

- Jim Wright Online: Dale-Chall and Spache Computation Worksheets. http://www.jimwrightonline.com/htmdocs/tools/okapi/

---

## Appendix: Key Points for Documentation Authors

**On "which version" of Dale-Chall:** The library implements the formula coefficients from the 1948 original paper (0.1579, 0.0496, 3.6365). The word list is the post-1995 expanded list of ~3,000 words. This is the standard modern implementation called "New Dale-Chall" or "NDC" in research literature.

**On "which version" of Spache:** The library implements the 1953 original formula coefficients (0.141 ASL + 0.086 PDW + 0.839), not the 1978 revised coefficients (0.121 ASL + 0.082 PDW + 0.659). If comparing scores against research that uses the revised formula, expect slight discrepancies.

**On Linsear Write attribution:** Do not describe Linsear Write as "developed by the US Air Force" -- this is not documented. The correct attribution is to John O'Hayre of the Bureau of Land Management (1966). The Air Force association appears to be a secondary adoption, not the origin.

**On Linsear Write implementation:** The library applies the formula to the full text rather than a 100-word sample. This is a practical deviation from the original methodology that reduces sampling variance but may produce scores that diverge from calculator tools that implement the strict 100-word sample.

**On grade-level output for Spache:** The library returns `round(score)` as the grade level, which collapses the decimal precision that the formula technically produces. Spache's decimal output (e.g., 2.7) is actually more informative for primary-grade discrimination; rounding to the nearest integer loses one grade level of precision in a range that only spans about three grade levels total.

**On the range limits:** Both Dale-Chall and Spache produce undefined or unreliable results outside their intended grade ranges. A Spache score of 4.5 should be interpreted with caution: the text may be at grade 4, or it may be outside the formula's reliable range and require Dale-Chall instead. A Dale-Chall score of 4.5 or below means the text is at or below 4th-grade level but does not discriminate further within that range.
