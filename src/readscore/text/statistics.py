# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Concrete implementation of statistics summary for readability measures."""

from dataclasses import dataclass

from readscore.types._interfaces import BaseStatSummary


@dataclass(frozen=True, order=True, slots=True)
class StatSummary(BaseStatSummary):
    """Concrete statistics type for readability measures."""

    def __post_init__(self):
        """Post-initialization checks or setup."""


__all__ = ("StatSummary",)
