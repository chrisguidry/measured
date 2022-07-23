import pytest

from measured import Quantity, Volume, approximately
from measured.si import Centi, Kilo, Liter, Meter, Milli
from measured.us import (
    Acre,
    AcreFoot,
    BoardFoot,
    Cord,
    Cup,
    FluidOunce,
    Foot,
    Gallon,
    Hogshead,
    Inch,
    Mile,
    Rick,
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
    assert left == approximately(right)
    assert right == approximately(left)


def test_abe() -> None:
    abes_car = (40 * Rod) / (1 * Hogshead)

    assert (40 * Rod) == approximately(0.125 * Mile)
    assert 1 * Hogshead == 63 * Gallon

    assert abes_car == approximately((0.125 / 63) * Mile / Gallon, 0)
    assert 0.00198 * Mile / Gallon <= abes_car <= 0.00199 * Mile / Gallon


def test_boardfoot() -> None:
    assert BoardFoot.dimension is Volume
    assert BoardFoot.name == "boardfoot"
    assert BoardFoot.symbol == "FBM"
    assert 1 * BoardFoot == 12 * 12 * 1 * Inch**3
    assert 1 * BoardFoot == approximately(2359.737 * (Centi * Meter) ** 3)
    assert 1 * BoardFoot == approximately(0.002359737 * Meter**3)
    assert 1 * BoardFoot == approximately(2.359737 * Liter)


def test_cord_and_rick() -> None:
    assert 1 * Cord == 3 * Rick
    assert 1 * Cord == approximately(3.623 * Meter**3, within=5e-4)


def test_acrefoot() -> None:
    assert AcreFoot.dimension is Volume
    assert AcreFoot.name == "acre-foot"
    assert AcreFoot.symbol == "acre-ft."
    assert 1 * AcreFoot == 1 * Acre * Foot
    assert 1 * AcreFoot == approximately(325851 * Gallon, within=2e-6)
    assert 1 * AcreFoot == approximately(1233 * Meter**3, within=4e-4)
