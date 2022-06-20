from measured.si import Liter, Milli
from measured.us import (
    Cup,
    FluidOunce,
    Gallon,
    Hogshead,
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


def test_abe() -> None:
    # https://www.reddit.com/r/theydidthemath/comments/1y38bs/calculation_of_abe_simpsons_gas_mileage_a_star_is/

    abes_car = (40 * Rod) / (1 * Hogshead)

    assert 40 * Rod == 0.125 * Mile
    assert 1 * Hogshead == 63 * Gallon

    assert abes_car == (0.125 / 63) * Mile / Gallon
    assert 0.00198 * Mile / Gallon <= abes_car <= 0.00199 * Mile / Gallon
