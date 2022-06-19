from typing import Iterable, Tuple

import pytest

from measured import Area, Length, Numeric, Unit, conversions
from measured.si import Meter, Second
from measured.us import Acre, Foot, Inch


def test_approximating_requires_units_with_conversion() -> None:
    Bogus = Unit.define(Length, name="bogus", symbol="bog")

    one = 1 * Meter
    other = 1 * Bogus

    assert not one.approximates(other, within=1e100)


def test_unit_conversion_must_be_in_same_dimension() -> None:
    with pytest.raises(TypeError):
        (1 * Meter).in_unit(Second)


def test_finding_conversions_in_different_dimensions_returns_none() -> None:
    assert conversions.find(Meter, Second) is None


def test_unit_always_converts_to_itself() -> None:
    converted = (10 * Meter).in_unit(Meter)
    assert converted.magnitude == 10
    assert converted.unit == Meter


def test_conversion_with_exponents() -> None:
    assert (1 * Foot) ** 2 == (12 * Inch) ** 2
    assert 1 * Foot**2 == 144 * Inch**2

    assert (1 * Foot) ** 3 == (12 * Inch) ** 3
    assert 1 * Foot**3 == 1728 * Inch**3


@pytest.mark.parametrize(
    "start, end, path",
    [
        (Foot, Inch, [(12.0, Inch)]),
        (Foot**2, Meter**2, [(0.09290304, Meter**2)]),
        (Meter**2, Foot**2, [(10.76391041670972, Foot**2)]),
        (Acre, Foot**2, [(43560.0, Foot**2)]),
        (Foot**2, Inch**2, [(144.0, Inch**2)]),
        (
            Acre,
            Inch**2,
            [
                (43560.0, Foot**2),
                (144.0, Inch**2),
            ],
        ),
        (Inch**2, Foot**2, [(0.006944444444444444, Foot**2)]),
        (Foot**2, Acre, [(0.00002295684113865932, Acre)]),
        (
            Inch**2,
            Acre,
            [
                (0.006944444444444444, Foot**2),
                (0.00002295684113865932, Acre),
            ],
        ),
    ],
)
def test_conversion_can_navigate_exponents(
    start: Unit, end: Unit, path: Iterable[Tuple[Numeric, Unit]]
) -> None:
    message = " != ".join(
        [
            conversions.format_path(conversions.find(start, end)),
            conversions.format_path(path),
        ]
    )

    assert conversions.find(start, end) == path, message


def test_backtracking_conversions_with_no_path() -> None:
    # Set up some arbitrary units that don't convert to one another
    Bogus = Unit.define(Length, "bogus", "bog")
    Bangus = Unit.define(Area, "bangus", "bang")

    assert conversions.find(Bogus**2, Bangus) is None
    assert conversions.find(Bangus, Bogus**2) is None