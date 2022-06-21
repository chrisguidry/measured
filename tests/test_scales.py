import pytest

from measured import Quantity
from measured.si import Celsius, Kelvin
from measured.us import Fahrenheit, Rankine


# https://en.wikipedia.org/wiki/Rankine_scale
@pytest.mark.parametrize(
    "kelvin, celsius, fahrenheit, rankine",
    [
        # Absolute zero
        (0 * Kelvin, -273.15 * Celsius, -459.67 * Fahrenheit, 0 * Rankine),
        # freezing point of brine
        (
            255.372222222 * Kelvin,
            -17.777777777 * Celsius,
            0 * Fahrenheit,
            459.67 * Rankine,
        ),
        # freezing point of water
        (273.15 * Kelvin, 0 * Celsius, 32 * Fahrenheit, 491.67 * Rankine),
        # boiling point of water
        (
            373.1339 * Kelvin,
            99.9839 * Celsius,
            211.97102 * Fahrenheit,
            671.64102 * Rankine,
        ),
    ],
)
def test_temperature_conversion_scale(
    kelvin: Quantity, celsius: Quantity, fahrenheit: Quantity, rankine: Quantity
) -> None:
    kelvin.assert_approximates(celsius)
    celsius.assert_approximates(kelvin)
    celsius.assert_approximates(fahrenheit)
    fahrenheit.assert_approximates(celsius)
    fahrenheit.assert_approximates(rankine)
    rankine.assert_approximates(kelvin)
    rankine.assert_approximates(celsius)
    kelvin.assert_approximates(rankine)
