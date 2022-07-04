from hypothesis.strategies import DrawFn, SearchStrategy, composite, sampled_from

from measured import systems  # noqa: F401
from measured import Dimension, Prefix, Unit

DIMENSIONS = sorted(Dimension.fundamental(), key=lambda d: d.exponents)
PREFIXES = sorted(Prefix._known.values(), key=lambda p: (p.base, p.exponent))
BASE_UNITS = sorted(Unit.base(), key=lambda u: u.name or "")
UNITS = sorted(Unit._known.values(), key=lambda u: u.name or "")


@composite
def dimensions(draw: DrawFn) -> SearchStrategy[Dimension]:
    return draw(sampled_from(DIMENSIONS))


@composite
def prefixes(draw: DrawFn) -> SearchStrategy[Prefix]:
    return draw(sampled_from(PREFIXES))


@composite
def units(draw: DrawFn) -> SearchStrategy[Unit]:
    return draw(sampled_from(UNITS))


@composite
def base_units(draw: DrawFn) -> SearchStrategy[Unit]:
    return draw(sampled_from(BASE_UNITS))
