# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""SMOG Index implementation."""

import math
import warnings

from dataclasses import dataclass, field

from readable.constants.about_metric import SMOG as _SMOG_ABOUT
from readable.types._interfaces import BaseMeasure
from readable.types.results import SmogResult


@dataclass(frozen=True, slots=True)
class Smog(BaseMeasure):
    """SMOG Index."""

    sentences: list[str] = field(default_factory=list)
    all_sentences: bool = False
    ignore_length: bool = False

    def __post_init__(self):
        """Post-initialization checks or setup."""
        if len(self.sentences) < 30:
            if not self.ignore_length:
                raise ValueError(
                    f"SMOG requires at least 30 sentences. {len(self.sentences)} found."
                )
            warnings.warn(f"SMOG requires 30 sentences. {len(self.sentences)} found.", stacklevel=2)

    @property
    def score(self) -> SmogResult:
        """Calculate and return the score."""
        score = self._score()
        return SmogResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal method to compute the score."""
        if self.all_sentences:
            num_complex_words = self._stats.num_poly_syllable_words
            num_sentences = self._stats.num_sentences
        else:
            # Re-calculate stats for the 30-sentence sample
            sample_stats = self._smog_text_stats()
            num_complex_words = sample_stats["num_poly_syllable_words"]
            num_sentences = 30

        return 1.0430 * math.sqrt(30 * num_complex_words / num_sentences) + 3.1291

    def _smog_text_stats(self) -> dict:
        """Calculate statistics for the SMOG 30-sentence sample."""
        # This is a bit tricky because we don't want to import TextAnalyzer here
        # to avoid circular dependencies.
        # For now, let's use a simple heuristic or expect the Readability class to handle it.
        # Actually, the original code called Analyzer().analyze(smog_text)

        # We can implement a simplified version here or move the logic to Readability
        # Let's see if we can just use the provided stats if all_sentences is True,
        # but if it's False, we need to analyze the specific sentences.

        # To keep it simple and avoid circularity, I'll implement a minimal analyzer here
        # or just use the count_syllables we already have.
        from readable.text.syllables import count_syllables

        mid = len(self.sentences) // 2
        first_10 = self.sentences[:10]
        mid_10 = self.sentences[mid - 5 : mid + 5]
        last_10 = self.sentences[-10:]

        sample_sentences = first_10 + mid_10 + last_10
        poly_syllable_count = 0

        # We need a word tokenizer too
        from nltk.tokenize import TweetTokenizer

        tokenizer = TweetTokenizer()

        for sentence in sample_sentences:
            tokens = tokenizer.tokenize(sentence)
            for token in tokens:
                # Basic punctuation check
                if len(token) == 1 and not token.isalnum():
                    continue
                if count_syllables(token) >= 3:
                    poly_syllable_count += 1

        return {"num_poly_syllable_words": poly_syllable_count}

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return _SMOG_ABOUT


__all__ = ("Smog",)
