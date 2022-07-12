import pytest

from measured import Quantity
from measured.energy import BritishThermalUnit, Calorie, TonneOfTNT, TonOfRefrigeration
from measured.si import ElectronVolt, Hour, Joule, Kilo, Watt
from measured.us import Foot, PoundForce


@pytest.mark.parametrize(
    "equivalent, within",
    [
        (4.184 * Joule, 0),
        (1.162e-6 * (Kilo * Watt) * Hour, 2e-4),
        (2.611e19 * ElectronVolt, 2e-4),
    ],
)
def test_calorie(equivalent: Quantity, within: float) -> None:
    (1 * Calorie).assert_approximates(equivalent, within=within)
    equivalent.assert_approximates(1 * Calorie, within=within)


@pytest.mark.parametrize(
    "equivalent, within",
    [
        (1.054350 * Kilo * Joule, 1e-6),
        (0.2931 * Watt * Hour, 8e-4),
        (252.2 * Calorie, 9e-4),
        (0.2522 * Kilo * Calorie, 9e-4),
        (778.2 * Foot * PoundForce, 8e-4),
    ],
)
def test_btus(equivalent: Quantity, within: float) -> None:
    (1 * BritishThermalUnit).assert_approximates(equivalent, within=within)
    equivalent.assert_approximates(1 * BritishThermalUnit, within=within)


def test_refrigeration() -> None:
    (1 * TonOfRefrigeration).assert_approximates(12000 * BritishThermalUnit / Hour, 0)
    (1 * TonOfRefrigeration).assert_approximates(3.51685 * Kilo * Watt, 0)
    (1 * TonOfRefrigeration).assert_approximates(
        3025.97 * (Kilo * Calorie) / Hour, 2e-7
    )


@pytest.mark.parametrize(
    "equivalent, within",
    [
        (4.184e9 * Joule, 0),
        (1.0e9 * Calorie, 0),
        (3.96831e6 * BritishThermalUnit, 3e-6),
        (3.086e9 * Foot * PoundForce, 2e-5),
        (1.162e3 * Kilo * Watt * Hour, 2e-4),
    ],
)
def test_tnt_equivalent(equivalent: Quantity, within: float) -> None:
    (1 * TonneOfTNT).assert_approximates(equivalent, within=within)
    equivalent.assert_approximates(1 * TonneOfTNT, within=within)
