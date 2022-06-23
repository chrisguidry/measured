import pytest

from measured import Quantity
from measured.si import Giga, Gram, Kilo, Kilogram, Mega, Milli


@pytest.mark.parametrize(
    "grams, kilograms",
    [
        (1 * Gram, 0.001 * Kilogram),
        (1 * Kilo * Gram, 1 * Kilogram),
        (1 * (Kilo * Gram), 1 * Kilogram),
        (1000 * (Kilo * Gram), 1000 * Kilogram),
        (1000 * (Kilo * Gram), 1 * (Mega * Gram)),
        (1000 * (Kilo * Gram), 1 * Kilo * Kilogram),
        (1 * Milli * Kilogram, 1 * Gram),
        (1 * Mega * Kilogram, 1 * (Giga * Gram)),
    ],
)
def test_kilogram_and_gram_equivalent(grams: Quantity, kilograms: Quantity) -> None:
    """Give special consideration to the equivalence between grams and kilograms, as
    they are derived as separate units in order to simplify the energy-related units"""
    assert grams == kilograms
    assert kilograms == grams
