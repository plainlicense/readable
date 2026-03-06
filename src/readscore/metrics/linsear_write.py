# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Linsear Write Formula implementation."""

from dataclasses import dataclass

from readscore.constants.about_metric import LINSEAR_WRITE as _LINSEAR_WRITE_ABOUT
from readscore.types._interfaces import BaseMeasure
from readscore.types.results import LinsearWriteResult


@dataclass(frozen=True, slots=True)
class LinsearWrite(BaseMeasure):
    """Linsear Write Formula."""

    @property
    def score(self) -> LinsearWriteResult:
        """Calculate and return the score."""
        score = self._score()
        return LinsearWriteResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        num_easy_words = stats.num_words - stats.num_poly_syllable_words
        num_hard_words = stats.num_poly_syllable_words
        # Note: This is an approximation based on the original library's implementation
        inter_score = (num_easy_words + (num_hard_words * 3)) / stats.num_sentences
        return inter_score / 2 if inter_score > 20 else (inter_score - 2) / 2

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return _LINSEAR_WRITE_ABOUT


__all__ = ("LinsearWrite",)
