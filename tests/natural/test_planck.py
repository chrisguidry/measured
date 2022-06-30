from measured import Length, Mass, Temperature, Time
from measured.fundamental import ℏ
from measured.natural import PlanckLength, PlanckMass, PlanckTemperature, PlanckTime
from measured.si import Joule, Kelvin, Kilogram, Meter, Second


def test_hbar() -> None:
    ℏ.assert_approximates(1.054571817e-34 * Joule * Second)


def test_length() -> None:
    assert PlanckLength.dimension is Length
    (1 * PlanckLength).assert_approximates(1.616255e-35 * Meter)


def test_mass() -> None:
    assert PlanckMass.dimension is Mass
    (1 * PlanckMass).assert_approximates(2.176434e-8 * Kilogram)


def test_time() -> None:
    assert PlanckTime.dimension is Time
    (1 * PlanckTime).assert_approximates(5.391247e-44 * Second)


def test_temperature() -> None:
    assert PlanckTemperature.dimension is Temperature
    (1 * PlanckTemperature).assert_approximates(1.416784e32 * Kelvin)
