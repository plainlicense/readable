# SPDX-FileCopyrightText: 2026 PlainLicense <https://plainlicense.org>
#
# SPDX-License-Identifier: LicenseRef-PlainMIT or MIT

"""Resource management for readability metrics."""

from __future__ import annotations

from types import MappingProxyType

# === MANAGED EXPORTS ===
# Exportify manages this section. It contains lazy-loading infrastructure
# for the package: imports and runtime declarations (__all__, __getattr__,
# __dir__). Manual edits will be overwritten by `exportify fix`.
from typing import TYPE_CHECKING

from lateimport import create_late_getattr


if TYPE_CHECKING:
    from readable.resources.loader import ResourceLoader
    from readable.resources.stemmer import Stemmer

_dynamic_imports: MappingProxyType[str, tuple[str, str]] = MappingProxyType({
    "ResourceLoader": (__spec__.parent, "loader"),
    "Stemmer": (__spec__.parent, "stemmer"),
})

__getattr__ = create_late_getattr(_dynamic_imports, globals(), __name__)

__all__ = ("ResourceLoader", "Stemmer")


def __dir__() -> list[str]:
    """List available attributes for the package."""
    return list(__all__)
