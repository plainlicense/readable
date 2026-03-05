"""The readable library for modern readability scoring."""

from readable.readability import Readability
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


__version__ = "0.1.0"
__all__ = [
    "ARIResult",
    "ColemanLiauResult",
    "DaleChallResult",
    "FleschKincaidResult",
    "FleschResult",
    "GunningFogResult",
    "LinsearWriteResult",
    "Readability",
    "SmogResult",
    "SpacheResult",
]
