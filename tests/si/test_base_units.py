from measured import (
    AmountOfSubstance,
    Area,
    Current,
    Frequency,
    Length,
    LuminousIntensity,
    Mass,
    One,
    Temperature,
    Time,
    Unit,
    Volume,
)
from measured.si import Ampere, Candela, Gram, Hertz, Kelvin, Meter, Mole, Second


def test_meter():
    assert isinstance(Meter, Unit)
    assert Meter.dimension is Length
    assert Meter.name == "meter"
    assert Meter.symbol == "m"


def test_square_meter():
    square_meter = Meter**2
    assert square_meter.dimension is Area
    assert square_meter.factors == {Meter: 2}
    assert square_meter is Meter * Meter


def test_cubic_meter():
    cubic_meter = Meter**3
    assert cubic_meter.dimension is Volume
    assert cubic_meter.factors == {Meter: 3}
    assert cubic_meter is Meter * Meter * Meter


def test_second():
    assert isinstance(Second, Unit)
    assert Second.dimension is Time
    assert Second.name == "second"
    assert Second.symbol == "s"


def test_hertz():
    assert Hertz.dimension is Frequency
    assert Hertz.factors == {Second: -1}
    assert Hertz.name == "hertz"
    assert Hertz.symbol == "Hz"
    assert Hertz is One / Second
    assert Hertz is Second**-1


def test_gram():
    assert isinstance(Gram, Unit)
    assert Gram.dimension is Mass
    assert Gram.name == "gram"
    assert Gram.symbol == "g"


def test_ampere():
    assert isinstance(Ampere, Unit)
    assert Ampere.dimension is Current
    assert Ampere.name == "ampere"
    assert Ampere.symbol == "A"


def test_kelvin():
    assert isinstance(Kelvin, Unit)
    assert Kelvin.dimension is Temperature
    assert Kelvin.name == "kelvin"
    assert Kelvin.symbol == "K"


def test_mole():
    assert isinstance(Mole, Unit)
    assert Mole.dimension is AmountOfSubstance
    assert Mole.name == "mole"
    assert Mole.symbol == "mol"


def test_candela():
    assert isinstance(Candela, Unit)
    assert Candela.dimension is LuminousIntensity
    assert Candela.name == "candela"
    assert Candela.symbol == "cd"
