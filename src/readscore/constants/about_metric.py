# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Descriptions of readability metrics."""

ARI = (
    "Uses character count and sentence length to estimate US grade level. "
    "Unlike syllable-based metrics, it handles technical jargon more reliably "
    "because character counting is exact where syllable counting is approximate. "
    "Returns grade level and a corresponding age range."
)

COLEMAN_LIAU = (
    "Uses letter count and sentence length to estimate US grade level. "
    "Like ARI, it avoids syllable counting — but counts letters only, not digits. "
    "This makes it diverge from ARI on numeral-heavy text. "
    "Works well for large-scale batch processing where deterministic results matter."
)

DALE_CHALL = (
    "Compares words against a list of 3,000 familiar English words, then weights "
    "sentence length. Most accurate for text aimed at grade 4 and above. "
    "Less reliable for technical text where common words have domain-specific meanings, "
    "or for text with many proper nouns not on the familiar-word list."
)

FLESCH = (
    "Scores text on a 0-100 scale using sentence length and syllables per word — "
    "higher scores mean easier text. The most widely cited readability formula; "
    "used in US government and legal requirements. Note: the scale runs backwards "
    "compared to every other metric in this library."
)

FLESCH_KINCAID = (
    "Uses the same inputs as Flesch Reading Ease — sentence length and syllables "
    "per word — but outputs a US grade level directly. Targets 75% comprehension; "
    "scores 2-4 grade levels lower than SMOG on the same text because SMOG targets "
    "100% comprehension."
)

GUNNING_FOG = (
    "Estimates years of formal education needed to understand text on first reading. "
    "Weights sentence length and the share of words with three or more syllables. "
    "Returns 'na' for very simple text (score below 6). "
    "Best for general prose; not calibrated for children's text."
)

LINSEAR_WRITE = (
    "Developed by John O'Hayre for the US Bureau of Land Management (1966), later "
    "adopted by the US Air Force. Classifies words as easy (1-2 syllables) or hard "
    "(3+ syllables), weights them, and maps the result to a US grade level. "
    "The grade-level conversion has limited validation and can be off by two grade levels."
)

SMOG = (
    "Counts polysyllabic words across a 30-sentence sample to estimate the grade "
    "level needed for full comprehension of health or educational materials. "
    "Targets 100% comprehension — scores 2-4 grade levels higher than Flesch-Kincaid "
    "on the same text. Requires at least 30 sentences by default."
)

SPACHE = (
    "Compares words against a list of familiar primary-grade words, then weights "
    "sentence length. Implements the 1953 original formula. "
    "Designed for grades 1-3 only — results above grade 3 indicate the text is "
    "outside the formula's calibrated range."
)

__all__ = (
    "ARI",
    "COLEMAN_LIAU",
    "DALE_CHALL",
    "FLESCH",
    "FLESCH_KINCAID",
    "GUNNING_FOG",
    "LINSEAR_WRITE",
    "SMOG",
    "SPACHE",
)
