from measured import Acceleration, Force, Mass
from measured.si import Gram, Kilo, Meter, Milli, Newton, Second


def test_newtons_second_law_gram_meter():
    mass = 5 * Gram
    assert mass.unit.dimension == Mass

    acceleration = 3 * Meter / Second**2
    assert acceleration.unit.dimension == Acceleration

    force = mass * acceleration
    assert force.unit.dimension == Force

    assert force == 15 * Gram * Meter / Second**2
    assert force == 0.015 * Newton


def test_newtons_second_law_kilogram_millimeter():
    mass = 5 * (Kilo * Gram)
    assert mass.unit.dimension == Mass

    acceleration = 3 * (Milli * Meter) / Second**2
    assert acceleration.unit.dimension == Acceleration

    force = mass * acceleration
    assert force.unit.dimension == Force

    assert force == 15 * Gram * Meter / Second**2
    assert force == 0.015 * Newton
