import pytest

from measured import Length, Mass, Quantity, Temperature, Time, approximately
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
    assert fundamental_constant == approximately(unity)
    assert unity == approximately(fundamental_constant)


def test_hbar() -> None:
    assert ℏ == approximately(1.054571817e-34 * Joule * Second)


def test_length() -> None:
    assert PlanckLength.dimension is Length
    assert 1 * PlanckLength == approximately(1.616255e-35 * Meter, 1.3e-7)


def test_mass() -> None:
    assert PlanckMass.dimension is Mass
    assert 1 * PlanckMass == approximately(2.176434e-8 * Kilogram, 1.6e-7)


def test_time() -> None:
    assert PlanckTime.dimension is Time
    assert 1 * PlanckTime == approximately(5.391247e-44 * Second, 1.1e-7)


def test_temperature() -> None:
    assert PlanckTemperature.dimension is Temperature
    assert 1 * PlanckTemperature == approximately(1.416784e32 * Kelvin, 1.2e-7)
