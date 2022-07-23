import pytest

from measured import Quantity, approximately
from measured.si import Celsius, Kelvin, Kilo, Milli


@pytest.mark.parametrize(
    "kelvin, celsius",
    [
        (0 * Kelvin, -273.15 * Celsius),
        (273.15 * Kelvin, 0 * Celsius),
        (373.15 * Kelvin, 100 * Celsius),
        (10273.15 * Kelvin, 10 * Kilo * Celsius),
        (1 * Kilo * Kelvin, 726.85 * Celsius),
    ],
)
def test_kelvin_equals_celsius(kelvin: Quantity, celsius: Quantity) -> None:
    assert kelvin == approximately(celsius, 0)
    assert celsius == approximately(kelvin, 0)


@pytest.mark.parametrize(
    "kelvin, celsius",
    [
        (273.16 * Kelvin, 10 * Milli * Celsius),
        (283150.0 * Milli * Kelvin, 10 * Celsius),
    ],
)
def test_kelvin_approximates_celsius(kelvin: Quantity, celsius: Quantity) -> None:
    assert kelvin == approximately(celsius)
    assert celsius == approximately(kelvin)
