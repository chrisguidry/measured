from fractions import Fraction

import pytest

from measured import (
    AmountOfSubstance,
    Area,
    Current,
    Frequency,
    Length,
    LuminousIntensity,
    Mass,
    Number,
    One,
    Temperature,
    Time,
    Unit,
    Volume,
)
from measured.si import Ampere, Candela, Gram, Hertz, Kelvin, Meter, Mole, Second


def pytest_generate_tests(metafunc):
    base = Unit.base()
    ids = [d.name for d in base]

    for exemplar in ["a", "b", "c"]:
        if exemplar in metafunc.fixturenames:
            metafunc.parametrize(exemplar, base, ids=ids)

    if "base" in metafunc.fixturenames:
        metafunc.parametrize("base", base, ids=ids)


@pytest.fixture
def identity() -> Unit:
    return One


def test_homogenous_under_addition(a: Unit, b: Unit):
    # https://en.wikipedia.org/wiki/Oneional_analysis#Dimensional_homogeneity
    #
    # Only commensurable quantities (physical quantities having the same dimension) may
    # be compared, equated, added, or subtracted.
    if a is b:
        assert a + b == a
    else:
        with pytest.raises(TypeError):
            a + b


def test_homogenous_under_subtraction(a: Unit, b: Unit):
    # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
    #
    # Only commensurable quantities (physical quantities having the same dimension) may
    # be compared, equated, added, or subtracted.
    if a is b:
        assert a - b == a
    else:
        with pytest.raises(TypeError):
            a - b


def test_abelian_associativity(a: Unit, b: Unit, c: Unit):
    # https://en.wikipedia.org/wiki/Abelian_group
    assert (a * b) * c == a * (b * c)


def test_abelian_identity(identity: Unit, a: Unit):
    assert identity * a == a


def test_abelian_inverse(identity: Unit, a: Unit):
    inverse = a**-1
    assert inverse * a == a * inverse
    assert inverse * a == identity
    assert identity / a == inverse


def test_abelian_commutativity(a: Unit, b: Unit):
    assert a * b == b * a


def test_no_dimensional_exponentation(base: Unit):
    with pytest.raises(TypeError):
        base**base  # type: ignore


def test_no_floating_point_exponentation(base: Unit):
    with pytest.raises(TypeError):
        base**0.5  # type: ignore


def test_no_fractional_exponentation(base: Unit):
    with pytest.raises(TypeError):
        base ** Fraction(1, 2)  # type: ignore


def test_repr(base: Unit):
    r = repr(base)
    assert r.startswith("<Unit(dimension=")
    assert base.dimension.name and base.dimension.name in r
    assert base.name and base.name in r
    assert base.symbol and base.symbol in r
    assert r.endswith(")>")


def test_base_units_factor_to_themselves(base: Unit):
    assert base.factors == {base: 1}


def test_one():
    assert isinstance(One, Unit)
    assert One.dimension is Number
    assert One.name == "one"
    assert One.symbol == "1"


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
