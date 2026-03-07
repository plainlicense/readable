# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Enums for readability metrics and their metadata."""

from __future__ import annotations

import platform

from dataclasses import FrozenInstanceError, dataclass
from enum import Enum
from types import DynamicClassAttribute
from typing import TYPE_CHECKING, Any, Self

from lateimport import LateImport, lateimport

from readscore.constants.about_metric import ARI as _ARI_ABOUT
from readscore.constants.about_metric import COLEMAN_LIAU as _COLEMAN_LIAU_ABOUT
from readscore.constants.about_metric import DALE_CHALL as _DALE_CHALL_ABOUT
from readscore.constants.about_metric import FLESCH as _FLESCH_ABOUT
from readscore.constants.about_metric import FLESCH_KINCAID as _FLESCH_KINCAID_ABOUT
from readscore.constants.about_metric import GUNNING_FOG as _GUNNING_FOG_ABOUT
from readscore.constants.about_metric import LINSEAR_WRITE as _LINSEAR_WRITE_ABOUT
from readscore.constants.about_metric import SMOG as _SMOG_ABOUT
from readscore.constants.about_metric import SPACHE as _SPACHE_ABOUT


if TYPE_CHECKING:
    from readscore.types._interfaces import BaseMeasure

_classes: dict[str, LateImport | type[BaseMeasure]] = {
    "ARI": lateimport("readscore.metrics.ari", "ARI"),
    "COLEMAN_LIAU": lateimport("readscore.metrics.coleman_liau", "ColemanLiau"),
    "DALE_CHALL": lateimport("readscore.metrics.dale_chall", "DaleChall"),
    "FLESCH": lateimport("readscore.metrics.flesch", "Flesch"),
    "FLESCH_KINCAID": lateimport("readscore.metrics.flesch_kincaid", "FleschKincaid"),
    "GUNNING_FOG": lateimport("readscore.metrics.gunning_fog", "GunningFog"),
    "LINSEAR_WRITE": lateimport("readscore.metrics.linsear_write", "LinsearWrite"),
    "SMOG": lateimport("readscore.metrics.smog", "Smog"),
    "SPACHE": lateimport("readscore.metrics.spache", "Spache"),
}


def _add_enum_alias[EnumT: Enum](enum_instance_member: EnumT, alias_name: str) -> None:
    """Add an alias to an Enum member."""
    if platform.python_version_tuple() >= ("3", "13"):
        enum_instance_member._add_alias_(alias_name)  # ty:ignore[unresolved-attribute]
    # life will be simpler when we can drop support for <3.13
    else:
        enum_cls = type(enum_instance_member)
        found_descriptor = None
        descriptor_type = None
        class_type = None
        for base in enum_cls.__mro__[1:]:
            attr = base.__dict__.get(alias_name)
            if attr is not None:
                if isinstance(attr, property | DynamicClassAttribute):
                    found_descriptor = attr
                    class_type = base
                    descriptor_type = "enum"
                    break
                if (
                    hasattr(attr, "__get__")
                    or hasattr(attr, "__set__")
                    or hasattr(attr, "__delete__")
                ):
                    found_descriptor = attr
                    descriptor_type = descriptor_type or "desc"
                    class_type = class_type or base
                    continue
                descriptor_type = "attr"
                class_type = base
        if found_descriptor:
            redirect = property()
            redirect.member = enum_instance_member  # ty:ignore[unresolved-attribute]
            redirect.__set_name__(enum_cls, alias_name)  # ty:ignore[unresolved-attribute]
            if descriptor_type in ("enum", "desc"):
                # earlier descriptor found; copy fget, fset, fdel to this one.
                redirect.fget = getattr(found_descriptor, "fget", None)
                redirect._get = getattr(  # ty:ignore[unresolved-attribute]
                    found_descriptor, "__get__", None
                )
                redirect.fset = getattr(found_descriptor, "fset", None)
                redirect._set = getattr(  # ty:ignore[unresolved-attribute]
                    found_descriptor, "__set__", None
                )
                redirect.fdel = getattr(found_descriptor, "fdel", None)
                redirect._del = getattr(  # ty:ignore[unresolved-attribute]
                    found_descriptor, "__delete__", None
                )
            redirect._attr_type = descriptor_type  # ty:ignore[unresolved-attribute]
            redirect._cls_type = class_type  # ty:ignore[unresolved-attribute]
            setattr(enum_cls, alias_name, redirect)
        else:
            setattr(enum_cls, alias_name, enum_instance_member)
        enum_cls._member_map_[alias_name] = enum_instance_member


def _add_enum_member[EnumT: Enum](
    enum_cls: type[EnumT], member_name: str, member_value: Any
) -> None:
    """Add a new member to an Enum class."""
    if platform.python_version_tuple() >= ("3", "13"):
        enum_cls._add_member_(member_name, member_value)  # ty:ignore[unresolved-attribute]
    else:
        _add_enum_alias(enum_cls(member_value), member_name)


@dataclass(frozen=True, slots=True)
class Metric:
    """Class to hold metric information."""

    about: str
    variable_name: str
    short_name: str
    full_name: str

    @property
    def _name(self) -> str:
        """Return the primary name of the metric."""
        return self.short_name.capitalize()

    def __str__(self) -> str:
        """Return the string representation of the metric."""
        return self.short_name

    @property
    def all_names(self) -> tuple[str, ...]:
        """Generate all alternative names for the metric."""
        names = {self.variable_name, self.short_name, self.full_name}
        if "_" in self.variable_name:
            names.update({
                self.variable_name.replace("_", " "),
                self.variable_name.replace("_", "-"),
                "".join(n[0] for n in self.variable_name.split("_") if n and n[0].isalpha()),
            })
        elif self.variable_name in {"smog", "spache"}:
            names.add(self.variable_name[:1])
        else:
            names.add(self.variable_name[0])
        return tuple(
            sorted({
                n
                for name in names
                for n in (name.lower(), name.upper(), name.title())
                if name and n
            })
        )

    @property
    def _value(self) -> Self:
        """Return the variable name of the metric."""
        return self


class ReadabilityMetric(Metric, Enum):
    """Enum for readability metrics."""

    ARI = Metric(_ARI_ABOUT, "ari", "ARI", "Automated Readability Index")
    COLEMAN_LIAU = Metric(_COLEMAN_LIAU_ABOUT, "coleman_liau", "Coleman-Liau", "Coleman-Liau Index")
    DALE_CHALL = Metric(
        _DALE_CHALL_ABOUT, "dale_chall", "Dale-Chall", "Dale-Chall Readability Score"
    )
    FLESCH = Metric(_FLESCH_ABOUT, "flesch", "Flesch", "Flesch Reading Ease")
    FLESCH_KINCAID = Metric(
        _FLESCH_KINCAID_ABOUT, "flesch_kincaid", "Flesch-Kincaid", "Flesch-Kincaid Grade Level"
    )
    GUNNING_FOG = Metric(_GUNNING_FOG_ABOUT, "gunning_fog", "Gunning Fog", "Gunning Fog Index")
    LINSEAR_WRITE = Metric(
        _LINSEAR_WRITE_ABOUT, "linsear_write", "Linsear Write", "Linsear Write Formula"
    )
    SMOG = Metric(_SMOG_ABOUT, "smog", "SMOG", "Simple Measure of Gobbledygook Index")
    SPACHE = Metric(_SPACHE_ABOUT, "spache", "Spache", "Spache Readability Formula")

    def __setattr__(self, name: str, value: Any) -> None:  # ty:ignore[invalid-method-override]
        """Allow Enum internals while preserving frozen field semantics."""
        if name in Metric.__dataclass_fields__:
            raise FrozenInstanceError(f"cannot assign to field {name!r}")
        object.__setattr__(self, name, value)

    def __new__(cls, value: Metric) -> Self:
        """Create a new ReadabilityMetric enum member."""
        obj = object.__new__(cls)
        object.__setattr__(obj, "_value_", value)
        return obj

    def __init__(self, metric: Metric) -> None:
        """Initialize the ReadabilityMetric enum member."""
        for key in metric.__annotations__:
            val = getattr(metric, key)
            object.__setattr__(self, key, val)

    def __str__(self) -> str:
        """Return the string representation of the readability metric."""
        return str(self.value)

    @property
    def short(self) -> str:
        """Return the short name of the readability metric."""
        return self.short_name

    @property
    def full(self) -> str:
        """Return the full name of the readability metric."""
        return self.full_name

    @classmethod
    def metrics(cls) -> list[str]:
        """Return a list of all readability metrics."""
        return sorted(cls.__members__.keys())

    @property
    def measure_class(self) -> type[BaseMeasure]:
        """Return the measure class for this metric."""
        entry = _classes[self.name]
        return entry._resolve() if isinstance(entry, LateImport) else entry

    @classmethod
    def from_name(cls, name: str) -> ReadabilityMetric:
        """Create a ReadabilityMetric enum member from a name."""
        for metric in cls:
            if name.lower() in metric.all_names:
                return metric
        raise ValueError(f"No readability metric found for name: {name}")

    @classmethod
    def register(cls, new_member: Metric, measure_class: type[BaseMeasure]) -> None:
        """Register a new metric member to the enum.

        Supports dynamic addition of new metrics at runtime. The new member should be an instance of Metric, and the measure_class should be the corresponding class that implements the metric's calculation.
        """
        member_name = new_member.variable_name.upper()
        _add_enum_member(cls, member_name, new_member)
        _classes[member_name] = measure_class


__all__ = ("Metric", "ReadabilityMetric")
