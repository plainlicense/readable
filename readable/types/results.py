"""Result types for readability measures."""

from dataclasses import dataclass

from ._interfaces import BaseResult


@dataclass(frozen=True, order=True, slots=True)
class ScoreResult(BaseResult):
    """A basic score result."""
    score: float


@dataclass(frozen=True, order=True, slots=True)
class GradeResult(BaseResult):
    """A result with a score and grade levels."""
    score: float
    grade_levels: list[str]

    @property
    def grade_level(self) -> str:
        """Return the primary grade level as a string."""
        return self.grade_levels[0] if self.grade_levels else "na"


@dataclass(frozen=True, order=True, slots=True)
class ARIResult(GradeResult):
    """A result for the Automated Readability Index."""
    ages: list[int]


@dataclass(frozen=True, order=True, slots=True)
class FleschResult(GradeResult):
    """A result for the Flesch Reading Ease score."""
    ease: str


@dataclass(frozen=True, order=True, slots=True)
class FleschKincaidResult(GradeResult):
    """A result for the Flesch-Kincaid Grade Level."""


@dataclass(frozen=True, order=True, slots=True)
class ColemanLiauResult(GradeResult):
    """A result for the Coleman-Liau Index."""


@dataclass(frozen=True, order=True, slots=True)
class DaleChallResult(GradeResult):
    """A result for the Dale-Chall Readability Score."""


@dataclass(frozen=True, order=True, slots=True)
class GunningFogResult(GradeResult):
    """A result for the Gunning Fog Index."""


@dataclass(frozen=True, order=True, slots=True)
class LinsearWriteResult(GradeResult):
    """A result for the Linsear Write Formula."""


@dataclass(frozen=True, order=True, slots=True)
class SmogResult(GradeResult):
    """A result for the SMOG Index."""


@dataclass(frozen=True, order=True, slots=True)
class SpacheResult(GradeResult):
    """A result for the Spache Readability Formula."""
