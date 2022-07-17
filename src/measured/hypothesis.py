from hypothesis.strategies import (
    SearchStrategy,
    builds,
    floats,
    integers,
    one_of,
    sampled_from,
)

from measured import systems  # noqa: F401
from measured import Dimension, Prefix, Quantity, Unit

DIMENSIONS = sorted(Dimension.fundamental(), key=lambda d: d.exponents)
PREFIXES = sorted(Prefix._by_name.values(), key=lambda p: (p.base, p.exponent))
BASE_UNITS = sorted(Unit.base(), key=lambda u: u.name or "")
UNITS = sorted(Unit._known.values(), key=lambda u: u.name or "")
for this in BASE_UNITS:
    UNITS.append(this**2)
    UNITS.append(this**3)
    UNITS.append(this**-2)
    UNITS.append(this**-3)
    for other in BASE_UNITS:
        UNITS.append(this / other)
        UNITS.append(this * other)
UNITS_WITH_SYMBOLS = [u for u in UNITS if u.symbol]


def dimensions() -> SearchStrategy[Dimension]:
    return sampled_from(DIMENSIONS)


def prefixes() -> SearchStrategy[Prefix]:
    return sampled_from(PREFIXES)


def units() -> SearchStrategy[Unit]:
    return sampled_from(UNITS)


def base_units() -> SearchStrategy[Unit]:
    return sampled_from(BASE_UNITS)


def units_with_symbols() -> SearchStrategy[Unit]:
    return sampled_from(UNITS_WITH_SYMBOLS)


def quantities() -> SearchStrategy[Quantity]:
    return builds(
        Quantity,
        magnitude=one_of(
            floats(min_value=-1e30, max_value=-1e-30),
            sampled_from([0.0]),
            floats(min_value=1e-30, max_value=1e-30),
            integers(),
        ),
        unit=units(),
    )
