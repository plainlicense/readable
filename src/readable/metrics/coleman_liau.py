# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Coleman-Liau Index implementation."""

from dataclasses import dataclass

from readable.constants.about_metric import COLEMAN_LIAU as _COLEMAN_LIAU_ABOUT
from readable.types._interfaces import BaseMeasure
from readable.types.results import ColemanLiauResult


@dataclass(frozen=True, slots=True)
class ColemanLiau(BaseMeasure):
    """Coleman-Liau Index."""

    @property
    def score(self) -> ColemanLiauResult:
        """Calculate and return the score."""
        score = self._score()
        return ColemanLiauResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        # l is the average number of letters per 100 words
        letters_per_100 = (stats.num_letters / stats.num_words) * 100
        # s is the average number of sentences per 100 words
        sentences_per_100 = (stats.num_sentences / stats.num_words) * 100
        return 0.0588 * letters_per_100 - 0.296 * sentences_per_100 - 15.8

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return _COLEMAN_LIAU_ABOUT


__all__ = ("ColemanLiau",)
