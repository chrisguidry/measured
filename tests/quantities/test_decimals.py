from decimal import Decimal

from measured.si import Ampere, Meter, Ohm, Second, Volt


def test_simple_conversion() -> None:
    distance = Decimal("10") * Meter
    duration = Decimal("4") * Second
    speed = Decimal("2.5") * (Meter / Second)
    assert distance / duration == speed
    assert speed * duration == distance
    assert distance / speed == duration


def test_complex_conversion() -> None:
    current = Decimal("2.5") * Ampere
    resistance = Decimal("3") * Ohm
    voltage = Decimal("7.5") * Volt
    assert voltage == current * resistance
    assert current == voltage / resistance
    assert resistance == voltage / current


def test_simple_addition() -> None:
    distance_one = Decimal("1.23") * Meter
    distance_two = Decimal("3.45") * Meter
    assert distance_one + distance_two == Decimal("4.68") * Meter


def test_complex_addition() -> None:
    resistance_one = Decimal("1.23") * Ohm
    resistance_two = Decimal("3.45") * Ohm
    assert resistance_one + resistance_two == Decimal("4.68") * Ohm
