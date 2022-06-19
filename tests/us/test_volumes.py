from measured.si import Liter, Milli
from measured.us import Cup, FluidOunce, Tablespoon, Teaspoon


def test_common_cooking_measures() -> None:
    assert 1 * Teaspoon == 4.92892159375 * Milli * Liter

    assert 1 * Tablespoon == 14.78676478125 * Milli * Liter
    assert 1 * Tablespoon == 3 * Teaspoon

    assert 1 * Cup == 236.5882365 * Milli * Liter
    assert 1 * Cup == 8 * FluidOunce
