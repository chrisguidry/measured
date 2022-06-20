import pytest

from measured import Quantity
from measured.si import Kelvin, Kilo, Milli
from measured.us import Rankine


@pytest.mark.parametrize(
    "kelvin, rankine",
    [
        # Absolute Zero
        (0 * Kelvin, 0 * Rankine),
        # Combined with prefixes > 1
        (10 * Kilo * Kelvin, 18 * Kilo * Rankine),
        (10 * Kilo * Kelvin, 18000 * Rankine),
        (10000 * Kelvin, 18 * Kilo * Rankine),
    ],
)
def test_kelvin_and_rankine(kelvin: Quantity, rankine: Quantity) -> None:
    assert kelvin == rankine
    assert rankine == kelvin


@pytest.mark.parametrize(
    "kelvin, rankine",
    [
        # Freezing point of brine
        (255.37 * Kelvin, 459.665999 * Rankine),
        # Freezing point of water
        (273.15 * Kelvin, 491.67 * Rankine),
        # Boiling point of water
        (373.1339 * Kelvin, 671.64102 * Rankine),
        # Combined with prefixes < 1
        (10 * Milli * Kelvin, 18 * Milli * Rankine),
        (10 * Milli * Kelvin, 0.018 * Rankine),
        (0.01 * Kelvin, 18 * Milli * Rankine),
    ],
)
def test_kelvin_approximates_rankine(kelvin: Quantity, rankine: Quantity) -> None:
    kelvin.assert_approximates(rankine)
    rankine.assert_approximates(kelvin)
