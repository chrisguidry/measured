from fractions import Fraction

import pytest
from hypothesis import example, given, strategies

from measured import Length, Number, One, Unit
from measured.hypothesis import base_units, units, units_with_symbols
from measured.iec import Byte
from measured.si import Liter, Meter, Second


@pytest.fixture(scope="module")
def identity() -> Unit:
    return One


@given(a=units(), b=units())
def test_homogenous_under_addition(a: Unit, b: Unit) -> None:
    # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
    #
    # Only commensurable quantities (physical quantities having the same dimension) may
    # be compared, equated, added, or subtracted.
    if a is b:
        assert a + b == a
    else:
        with pytest.raises(TypeError):
            a + b


@given(a=units(), b=units())
def test_homogenous_under_subtraction(a: Unit, b: Unit) -> None:
    # https://en.wikipedia.org/wiki/Dimensional_analysis#Dimensional_homogeneity
    #
    # Only commensurable quantities (physical quantities having the same dimension) may
    # be compared, equated, added, or subtracted.
    if a is b:
        assert a - b == a
    else:
        with pytest.raises(TypeError):
            a - b


@given(a=units(), b=units(), c=units())
def test_abelian_associativity(a: Unit, b: Unit, c: Unit) -> None:
    # https://en.wikipedia.org/wiki/Abelian_group
    assert (a * b) * c == a * (b * c)


@given(a=units())
def test_abelian_identity(identity: Unit, a: Unit) -> None:
    assert identity * a == a


@given(a=units())
@example(a=Byte)
def test_abelian_inverse(identity: Unit, a: Unit) -> None:
    inverse = a**-1
    assert inverse * a == a * inverse
    assert inverse * a == identity
    assert identity / a == inverse


@given(a=units(), b=units())
def test_abelian_commutativity(a: Unit, b: Unit) -> None:
    assert a * b == b * a


@given(unit=units())
def test_no_dimensional_exponentation(unit: Unit) -> None:
    with pytest.raises(TypeError):
        unit**unit  # type: ignore


@given(unit=units())
def test_no_floating_point_exponentation(unit: Unit) -> None:
    with pytest.raises(TypeError):
        unit**0.5  # type: ignore


@given(unit=units())
def test_no_fractional_exponentation(unit: Unit) -> None:
    with pytest.raises(TypeError):
        unit ** Fraction(1, 2)  # type: ignore


@given(unit=units())
def test_repr_roundtrips(unit: Unit) -> None:
    from measured import Dimension, Prefix  # noqa: F401

    assert eval(repr(unit)) is unit


@given(base=base_units())
def test_base_units_factor_to_themselves(base: Unit) -> None:
    assert base.factors == {base: 1}


def test_one() -> None:
    assert isinstance(One, Unit)
    assert One.dimension is Number
    assert One.name == "one"
    assert One.symbol == "1"


@given(root=strategies.integers())
def test_identity_to_any_root(root: int) -> None:
    assert One.root(0) == One
    assert One.root(2) == One
    assert One.root(3) == One
    assert One.root(100) == One


@given(unit=units())
def test_zeroth_root_always_one(unit: Unit) -> None:
    assert unit.root(0) is One


def test_roots() -> None:
    assert (Meter**2).root(0) == One
    assert (Meter**2).root(2) == Meter
    assert (Meter**4).root(2) == Meter**2
    assert (Meter**16 / Second**12).root(4) == Meter**4 / Second**3


def test_only_integer_roots() -> None:
    with pytest.raises(TypeError):
        (Meter**2).root(0.5)  # type: ignore


def test_whole_power_roots_only() -> None:
    with pytest.raises(ValueError):
        (Meter**3).root(2)


def test_names_unique() -> None:
    with pytest.raises(ValueError, match="already defined"):
        Length.unit("meter", "totally unique")

    with pytest.raises(ValueError, match="already defined"):
        Unit.derive(Meter / Second, name="ohm", symbol="totally unique")


def test_symbols_unique() -> None:
    with pytest.raises(ValueError, match="already defined"):
        Length.unit("totally unique", "m")

    with pytest.raises(ValueError, match="already defined"):
        Unit.derive(Meter / Second, name="totally unique", symbol="Ω")


@given(unit=units_with_symbols())
@example(unit=Liter)  # liter is interesting in that it includes a prefix
def test_units_str_to_their_symbols(unit: Unit) -> None:
    assert str(unit) == unit.symbol
