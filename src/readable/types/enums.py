"""Enums for readability metrics and their metadata."""

# ruff: noqa: SLF001
from enum import Enum
from typing import TYPE_CHECKING, NamedTuple


if TYPE_CHECKING:
    from ._interfaces import BaseMeasure


class MetricNames(NamedTuple):
    """Named tuple for readability metric names."""

    var: str
    short: str
    full: str
    all: tuple[str, ...]

class ReadabilityMetric(Enum):
    """Enum for readability metrics."""

    ARI = 1
    COLEMAN_LIAU = 2
    DALE_CHALL = 3
    FLESCH = 4
    FLESCH_KINCAID = 5
    GUNNING_FOG = 6
    LINSEAR_WRITE = 7
    SMOG = 8
    SPACHE = 9

    def __str__(self) -> str:
        """Return the string representation of the readability metric."""
        return self._names.short

    @property
    def _names(self) -> MetricNames:
        """Return the name of the readability metric."""
        return {
            ReadabilityMetric.ARI: MetricNames(var="ari", short="ARI", full="Automated Readability Index", all=()),
            ReadabilityMetric.COLEMAN_LIAU: MetricNames(var="coleman_liau", short="Coleman-Liau", full="Coleman-Liau Index", all=()),
            ReadabilityMetric.DALE_CHALL: MetricNames(var="dale_chall", short="Dale-Chall", full="Dale-Chall Readability Score", all=()),
            ReadabilityMetric.FLESCH: MetricNames(var="flesch", short="Flesch", full="Flesch Reading Ease", all=()),
            ReadabilityMetric.FLESCH_KINCAID: MetricNames(var="flesch_kincaid", short="Flesch-Kincaid", full="Flesch-Kincaid Grade Level", all=()),
            ReadabilityMetric.GUNNING_FOG: MetricNames(var="gunning_fog", short="Gunning Fog", full="Gunning Fog Index", all=()),
            ReadabilityMetric.LINSEAR_WRITE: MetricNames(var="linsear_write", short="Linsear Write", full="Linsear Write Formula", all=()),
            ReadabilityMetric.SMOG: MetricNames(var="smog", short="SMOG", full="Simple Measure of Gobbledygook Index", all=()),
            ReadabilityMetric.SPACHE: MetricNames(var="spache", short="Spache", full="Spache Readability Formula", all=()),
        }[self]

    @property
    def _all_names(self) -> tuple[str, ...]:
        """Generate alternative names for a readability metric."""
        varname = self._names.var
        names = [varname]
        if "_" in varname:
            new_names = []
            for name in names:
                if "_" in name:
                    new_names.extend((
                        name.replace("_", " "),
                        name.replace("_", "-"),
                        "".join(n[0] for n in name.split("_") if n and n[0].isalpha()),
                    ))
            names.extend(new_names)
        elif varname in {"smog", "spache"}:
            names.append(varname[:1])
        else:
            names.append(varname[0])
        if varname in {"coleman_liau", "dale_chall", "gunning_fog", "linsear_write"}:
            names.append(varname[0])
        return tuple(
            sorted({
                n
                for name in names
                for n in (name.lower(), name.upper(), name.title())
                if name and n
            })
        )

    @classmethod
    def metrics(cls) -> list[str]:
        """Return a list of all readability metrics."""
        return sorted(cls.__members__.keys())

    @property
    def measure_class(self) -> type["BaseMeasure"]:
        """Return the measure class for this metric."""
        from readable.metrics.ari import ARI
        from readable.metrics.coleman_liau import ColemanLiau
        from readable.metrics.dale_chall import DaleChall
        from readable.metrics.flesch import Flesch
        from readable.metrics.flesch_kincaid import FleschKincaid
        from readable.metrics.gunning_fog import GunningFog
        from readable.metrics.linsear_write import LinsearWrite
        from readable.metrics.smog import Smog
        from readable.metrics.spache import Spache

        return {
            ReadabilityMetric.ARI: ARI,
            ReadabilityMetric.COLEMAN_LIAU: ColemanLiau,
            ReadabilityMetric.DALE_CHALL: DaleChall,
            ReadabilityMetric.FLESCH: Flesch,
            ReadabilityMetric.FLESCH_KINCAID: FleschKincaid,
            ReadabilityMetric.GUNNING_FOG: GunningFog,
            ReadabilityMetric.LINSEAR_WRITE: LinsearWrite,
            ReadabilityMetric.SMOG: Smog,
            ReadabilityMetric.SPACHE: Spache,
        }[self]
