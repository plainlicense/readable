# ruff: noqa: SLF001
from enum import Enum
from typing import Literal, NamedTuple

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
            ReadabilityMetric.ARI: MetricNames(var="ari", short="ARI", full="Automated Readability Index", all=ReadabilityMetric.ARI._all_names),
            ReadabilityMetric.COLEMAN_LIAU: MetricNames(var="coleman_liau", short="Coleman-Liau", full="Coleman-Liau Index", all=ReadabilityMetric.COLEMAN_LIAU._all_names),
            ReadabilityMetric.DALE_CHALL: MetricNames(var="dale_chall", short="Dale-Chall", full="Dale-Chall Readability Score", all=ReadabilityMetric.DALE_CHALL._all_names),
            ReadabilityMetric.FLESCH: MetricNames(var="flesch", short="Flesch", full="Flesch Reading Ease", all=ReadabilityMetric.FLESCH._all_names),
            ReadabilityMetric.FLESCH_KINCAID: MetricNames(var="flesch_kincaid", short="Flesch-Kincaid", full="Flesch-Kincaid Grade Level", all=ReadabilityMetric.FLESCH_KINCAID._all_names),
            ReadabilityMetric.GUNNING_FOG: MetricNames(var="gunning_fog", short="Gunning Fog", full="Gunning Fog Index", all=ReadabilityMetric.GUNNING_FOG._all_names),
            ReadabilityMetric.LINSEAR_WRITE: MetricNames(var="linsear_write", short="Linsear Write", full="Linsear Write Formula", all=ReadabilityMetric.LINSEAR_WRITE._all_names),
            ReadabilityMetric.SMOG: MetricNames(var="smog", short="SMOG", full="Simple Measure of Gobbledygook Index", all=ReadabilityMetric.SMOG._all_names),
            ReadabilityMetric.SPACHE: MetricNames(var="spache", short="Spache", full="Spache Readability Formula", all=ReadabilityMetric.SPACHE._all_names),
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
