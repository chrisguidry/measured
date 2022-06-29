from measured import (
    Capacitance,
    Charge,
    Current,
    MagneticBField,
    MagneticFlux,
    Potential,
    Resistance,
)
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


def test_ampere() -> None:
    assert Ampere.name == "ampere"
    assert Ampere.symbol == "A"
    assert Ampere.dimension is Current
    assert 1 * Ampere == 1 * Coulomb / Second


def test_coulomb() -> None:
    assert Coulomb.name == "coulomb"
    assert Coulomb.symbol == "C"
    assert Coulomb.dimension is Charge
    assert 1 * Coulomb == 1 * Ampere * Second


def test_farad() -> None:
    assert Farad.name == "farad"
    assert Farad.symbol == "F"
    assert Farad.dimension is Capacitance


def test_ohm() -> None:
    assert Ohm.name == "ohm"
    assert Ohm.symbol == "Ω"
    assert Ohm.dimension is Resistance


def test_tesla() -> None:
    assert Tesla.name == "tesla"
    assert Tesla.symbol == "T"
    assert Tesla.dimension is MagneticBField


def test_volt() -> None:
    assert Volt.name == "volt"
    assert Volt.symbol == "V"
    assert Volt.dimension is Potential


def test_weber() -> None:
    assert Weber.name == "weber"
    assert Weber.symbol == "Wb"
    assert Weber.dimension is MagneticFlux


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

    b_field = flux / area
    assert b_field == 12000000 * Tesla
