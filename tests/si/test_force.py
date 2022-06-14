from measured import Acceleration, Energy, Force, Mass, Power
from measured.si import Gram, Joule, Kilo, Meter, Milli, Newton, Second, Watt


def test_newtons_second_law_gram_meter() -> None:
    mass = 5 * Gram
    assert mass.unit.dimension == Mass

    acceleration = 3 * Meter / Second**2
    assert acceleration.unit.dimension == Acceleration

    force = mass * acceleration
    assert force.unit.dimension == Force

    assert force == 15 * Gram * Meter / Second**2
    assert force == 0.015 * Newton


def test_newtons_second_law_kilogram_millimeter() -> None:
    mass = 5 * (Kilo * Gram)
    assert mass.unit.dimension == Mass

    acceleration = 3 * (Milli * Meter) / Second**2
    assert acceleration.unit.dimension == Acceleration

    force = mass * acceleration
    assert force.unit.dimension == Force

    assert force == 15 * Gram * Meter / Second**2
    assert force == 0.015 * Newton


def test_energy_is_force_through_distance() -> None:
    force = 10 * Newton
    distance = 5 * Meter
    energy = force * distance
    assert energy.unit == Joule
    assert energy.unit.dimension == Energy


def test_power_is_energy_per_time() -> None:
    energy = 10 * Joule
    power = energy / (2 * Second)
    assert power.unit == Watt
    assert power.unit.dimension == Power