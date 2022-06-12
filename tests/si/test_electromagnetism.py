from measured.si import (
    Ampere,
    Coulomb,
    Farad,
    Meter,
    Milli,
    Ohm,
    Second,
    Tesla,
    Volt,
    Weber,
)


def test_ohms_law() -> None:
    I = 4 * Ampere
    V = 12 * Volt
    R = 3 * Ohm

    assert I == V / R
    assert R == V / I
    assert V == I * R


def test_capacitance_is_charge_per_potential() -> None:
    charge = 5 * Coulomb
    potential = 10 * Volt
    capacitance = charge / potential
    assert capacitance == 0.5 * Farad


def test_magnetic_inductance_is_magnetic_flux_per_area() -> None:
    flux = 12 * Volt * Second
    assert flux == 12 * Weber

    area = (1 * (Milli * Meter)) ** 2

    induction = flux / area
    assert induction == 12000000 * Tesla
