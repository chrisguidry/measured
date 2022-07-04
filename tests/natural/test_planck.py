import pytest

from measured import Length, Mass, Quantity, Temperature, Time
from measured.natural import PlanckLength, PlanckMass, PlanckTemperature, PlanckTime
from measured.physics import G, c, k, ℏ
from measured.si import Joule, Kelvin, Kilogram, Meter, Second


@pytest.mark.parametrize(
    "fundamental_constant, unity",
    [
        (c, 1 * (PlanckLength / PlanckTime)),
        (ℏ, 1 * ((PlanckLength**2 * PlanckMass) / PlanckTime)),
        (G, 1 * (PlanckLength**3 / (PlanckMass * PlanckTime**2))),
        (
            k,
            1
            * (
                (PlanckLength**2 * PlanckMass) / (PlanckTemperature * PlanckTime**2)
            ),
        ),
    ],
)
def test_unity(fundamental_constant: Quantity, unity: Quantity) -> None:
    fundamental_constant.assert_approximates(unity)
    unity.assert_approximates(fundamental_constant)


def test_hbar() -> None:
    ℏ.assert_approximates(1.054571817e-34 * Joule * Second)


def test_length() -> None:
    assert PlanckLength.dimension is Length
    (1 * PlanckLength).assert_approximates(1.616255e-35 * Meter, 1.3e-07)


def test_mass() -> None:
    assert PlanckMass.dimension is Mass
    (1 * PlanckMass).assert_approximates(2.176434e-8 * Kilogram)


def test_time() -> None:
    assert PlanckTime.dimension is Time
    (1 * PlanckTime).assert_approximates(5.391247e-44 * Second)


def test_temperature() -> None:
    assert PlanckTemperature.dimension is Temperature
    (1 * PlanckTemperature).assert_approximates(1.416784e32 * Kelvin)
