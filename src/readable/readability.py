# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Main API for the readable library."""

import warnings

from readable.metrics.ari import ARI
from readable.metrics.coleman_liau import ColemanLiau
from readable.metrics.dale_chall import DaleChall
from readable.metrics.flesch import Flesch
from readable.metrics.flesch_kincaid import FleschKincaid
from readable.metrics.gunning_fog import GunningFog
from readable.metrics.linsear_write import LinsearWrite
from readable.metrics.smog import Smog
from readable.metrics.spache import Spache
from readable.text.analyzer import TextAnalyzer
from readable.text.statistics import StatSummary
from readable.text.tokenizer import Tokenizer
from readable.types.results import (
    ARIResult,
    ColemanLiauResult,
    DaleChallResult,
    FleschKincaidResult,
    FleschResult,
    GunningFogResult,
    LinsearWriteResult,
    SmogResult,
    SpacheResult,
)


class Readability:
    """
    Main class for calculating various readability metrics for a given text.
    """

    def __init__(self, text: str, min_words: int = 100):
        """
        Initialize with text and analyze it.

        Args:
            text: The text to analyze.
            min_words: Minimum number of words required for most readability tests.
        """
        self._text = text
        self._analyzer = TextAnalyzer()
        self._stats = self._analyzer.analyze(text)
        self._min_words = min_words

        # We also need sentences for SMOG
        tokenizer = Tokenizer()
        self._sentences = tokenizer.tokenize_sentences(text)

        if self._min_words < 100:
            warnings.warn(
                "Documents with fewer than 100 words may affect the accuracy of readability tests.",
                stacklevel=2,
            )

    @property
    def stats(self) -> StatSummary:
        """Return the statistics object calculated during initialization."""
        return self._stats

    def ari(self) -> ARIResult:
        """Calculate Automated Readability Index (ARI)."""
        return ARI(self._stats, self._min_words).score

    def coleman_liau(self) -> ColemanLiauResult:
        """Calculate Coleman-Liau Index."""
        return ColemanLiau(self._stats, self._min_words).score

    def dale_chall(self) -> DaleChallResult:
        """Calculate Dale-Chall Readability Score."""
        return DaleChall(self._stats, self._min_words).score

    def flesch(self) -> FleschResult:
        """Calculate Flesch Reading Ease score."""
        return Flesch(self._stats, self._min_words).score

    def flesch_kincaid(self) -> FleschKincaidResult:
        """Calculate Flesch-Kincaid Grade Level."""
        return FleschKincaid(self._stats, self._min_words).score

    def gunning_fog(self) -> GunningFogResult:
        """Calculate Gunning Fog Index."""
        return GunningFog(self._stats, self._min_words).score

    def linsear_write(self) -> LinsearWriteResult:
        """Calculate Linsear Write Formula."""
        return LinsearWrite(self._stats, self._min_words).score

    def smog(self, *, all_sentences: bool = False, ignore_length: bool = False) -> SmogResult:
        """
        Calculate SMOG Index.

        Args:
            all_sentences: Whether to use all sentences or a 30-sentence sample.
            ignore_length: Whether to ignore the 30-sentence minimum length requirement.
        """
        return Smog(
            _stats=self._stats,
            _min_words=self._min_words,
            sentences=self._sentences,
            all_sentences=all_sentences,
            ignore_length=ignore_length,
        ).score

    def spache(self) -> SpacheResult:
        """Calculate Spache Readability Formula."""
        return Spache(self._stats, self._min_words).score

    def statistics(self) -> dict:
        """Return a dictionary of calculated statistics."""
        return {
            "num_letters": self._stats.num_letters,
            "num_words": self._stats.num_words,
            "num_sentences": self._stats.num_sentences,
            "num_polysyllabic_words": self._stats.num_poly_syllable_words,
            "avg_words_per_sentence": self._stats.avg_words_per_sentence,
            "avg_syllables_per_word": self._stats.avg_syllables_per_word,
        }


__all__ = ("Readability",)
