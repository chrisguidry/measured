import pytest

from measured import Quantity
from measured.si import Kilo, Liter, Meter, Milli
from measured.us import (
    Cup,
    FluidOunce,
    Foot,
    Gallon,
    Hogshead,
    Inch,
    Mile,
    Rod,
    Tablespoon,
    Teaspoon,
)


def test_common_cooking_measures() -> None:
    assert 1 * Teaspoon == 4.92892159375 * Milli * Liter

    assert 1 * Tablespoon == 14.78676478125 * Milli * Liter
    assert 1 * Tablespoon == 3 * Teaspoon

    assert 1 * Cup == 236.5882365 * Milli * Liter
    assert 1 * Cup == 8 * FluidOunce


@pytest.mark.parametrize(
    "left, right",
    [
        (1 * Foot**3, 1728 * Inch**3),
        (1 * Mile / Foot**3, 1 / 1728 * Mile / Inch**3),
        (10 * Gallon / Mile, 0.023521459 * Liter / Meter),
        (10 * Gallon / Mile, 23.521459 * Liter / (Kilo * Meter)),
        (10 * Mile / Gallon, 4251.4370 * Meter / Liter),
        (10 * Mile / Gallon, 4.2514370 * (Kilo * Meter) / Liter),
    ],
)
def test_volume_conversions(left: Quantity, right: Quantity) -> None:
    left.assert_approximates(right)
    right.assert_approximates(left)


def test_abe() -> None:
    abes_car = (40 * Rod) / (1 * Hogshead)

    (40 * Rod).assert_approximates(0.125 * Mile)
    assert 1 * Hogshead == 63 * Gallon

    abes_car.assert_approximates((0.125 / 63) * Mile / Gallon, 0)
    assert 0.00198 * Mile / Gallon <= abes_car <= 0.00199 * Mile / Gallon
