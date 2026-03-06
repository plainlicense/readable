# SPDX-FileCopyrightText: 2026 PlainLicense <https://plainlicense.org>
#
# SPDX-License-Identifier: LicenseRef-PlainMIT or MIT

"""Readability metric implementations."""

from __future__ import annotations

from types import MappingProxyType

# === MANAGED EXPORTS ===
# Exportify manages this section. It contains lazy-loading infrastructure
# for the package: imports and runtime declarations (__all__, __getattr__,
# __dir__). Manual edits will be overwritten by `exportify fix`.
from typing import TYPE_CHECKING

from lateimport import create_late_getattr


if TYPE_CHECKING:
    from readscore.metrics.ari import ARI
    from readscore.metrics.coleman_liau import ColemanLiau
    from readscore.metrics.dale_chall import DaleChall
    from readscore.metrics.flesch import Flesch
    from readscore.metrics.flesch_kincaid import FleschKincaid
    from readscore.metrics.gunning_fog import GunningFog
    from readscore.metrics.linsear_write import LinsearWrite
    from readscore.metrics.smog import Smog
    from readscore.metrics.spache import Spache

_dynamic_imports: MappingProxyType[str, tuple[str, str]] = MappingProxyType({
    "ARI": (__spec__.parent, "ari"),
    "ColemanLiau": (__spec__.parent, "coleman_liau"),
    "DaleChall": (__spec__.parent, "dale_chall"),
    "Flesch": (__spec__.parent, "flesch"),
    "FleschKincaid": (__spec__.parent, "flesch_kincaid"),
    "GunningFog": (__spec__.parent, "gunning_fog"),
    "LinsearWrite": (__spec__.parent, "linsear_write"),
    "Smog": (__spec__.parent, "smog"),
    "Spache": (__spec__.parent, "spache"),
})

__getattr__ = create_late_getattr(_dynamic_imports, globals(), __name__)

__all__ = (
    "ARI",
    "ColemanLiau",
    "DaleChall",
    "Flesch",
    "FleschKincaid",
    "GunningFog",
    "LinsearWrite",
    "Smog",
    "Spache",
)


def __dir__() -> list[str]:
    """List available attributes for the package."""
    return list(__all__)
