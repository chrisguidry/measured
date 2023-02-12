from decimal import Decimal

from measured import approximately
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


def test_simple_subtraction() -> None:
    distance_one = Decimal("4.68") * Meter
    distance_two = Decimal("3.45") * Meter
    assert distance_one - distance_two == Decimal("1.23") * Meter


def test_exponentation() -> None:
    distance = Decimal("1.23") * Meter
    volume = distance**3
    assert volume == Decimal("1.860867") * Meter**3
    assert volume.root(3) == approximately(distance)


def test_complex_addition() -> None:
    resistance_one = Decimal("1.23") * Ohm
    resistance_two = Decimal("3.45") * Ohm
    assert resistance_one + resistance_two == Decimal("4.68") * Ohm
