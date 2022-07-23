import pytest

from measured import Quantity, approximately
from measured.si import Kelvin, Kilo, Milli
from measured.us import Fahrenheit, Rankine


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
    assert kelvin == approximately(rankine)
    assert rankine == approximately(kelvin)


@pytest.mark.parametrize(
    "rankine, fahrenheit",
    [
        (0 * Rankine, -459.67 * Fahrenheit),
        (459.67 * Rankine, 0 * Fahrenheit),
    ],
)
def test_rankine_equals_fahrenheit(rankine: Quantity, fahrenheit: Quantity) -> None:
    assert rankine == fahrenheit
    assert fahrenheit == rankine


@pytest.mark.parametrize(
    "rankine, fahrenheit",
    [
        (459.68 * Rankine, 10 * Milli * Fahrenheit),
        (559.67 * Rankine, 100 * Fahrenheit),
        (559670.0 * Milli * Rankine, 100 * Fahrenheit),
    ],
)
def test_rankine_approximates_fahrenheit(
    rankine: Quantity, fahrenheit: Quantity
) -> None:
    assert rankine == approximately(fahrenheit)
    assert fahrenheit == approximately(rankine)
