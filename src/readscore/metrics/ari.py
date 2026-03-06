# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Automated Readability Index (ARI) implementation."""

import math

from dataclasses import dataclass

from readscore.constants.about_metric import ARI as _ARI_ABOUT
from readscore.types._interfaces import BaseMeasure
from readscore.types.results import ARIResult


_ARI_AGES: tuple[tuple[int, int], ...] = (
    (5, 6),  # score <= 1
    (6, 7),  # score <= 2
    (7, 9),  # score <= 3
    (9, 10),  # score <= 4
    (10, 11),  # score <= 5
    (11, 12),  # score <= 6
    (12, 13),  # score <= 7
    (13, 14),  # score <= 8
    (14, 15),  # score <= 9
    (15, 16),  # score <= 10
    (16, 17),  # score <= 11
    (17, 18),  # score <= 12
    (18, 24),  # score <= 13
    (24, 100),  # score > 13
)


@dataclass(frozen=True, slots=True)
class ARI(BaseMeasure):
    """Automated Readability Index (ARI)."""

    @property
    def score(self) -> ARIResult:
        """Calculate and return the score."""
        score = self._score()
        return ARIResult(
            score=score, grade_levels=self._grade_levels(score), ages=self._ages(score)
        )

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        letters_per_word = stats.num_letters / stats.num_words
        words_per_sent = stats.num_words / stats.num_sentences
        return 4.71 * letters_per_word + 0.5 * words_per_sent - 21.43

    def _grade_levels(self, score: float) -> list[str]:
        """Internal method to calculate grade levels based on the score."""
        score_ceil = math.ceil(score)
        if score_ceil <= 1:
            return ["K"]
        if score_ceil <= 2:
            return ["1", "2"]
        if score_ceil <= 12:
            return [str(score_ceil)]
        return ["college"] if score_ceil <= 13 else ["college_graduate"]

    def _ages(self, score: float) -> list[int]:
        """Internal method to calculate ages based on the score."""
        idx = min(max(math.ceil(score) - 1, 0), len(_ARI_AGES) - 1)
        return list(_ARI_AGES[idx])

    @property
    def grade_level(self) -> int:
        """Return the primary grade level as an integer."""
        score_ceil = math.ceil(self._score())
        if score_ceil <= 1:
            return 0
        if score_ceil <= 12:
            return score_ceil
        return 13 if score_ceil <= 13 else 14

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return _ARI_ABOUT


__all__ = ("ARI",)
