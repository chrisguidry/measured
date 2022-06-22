from fractions import Fraction

import pytest

from measured import Length, Number, One, Unit
from measured.si import Meter, Second


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    base = sorted(Unit.base(), key=lambda u: u.name or "")
    ids = [d.name for d in base]

    # just take a sample of units (with overlaps) to prevent the tests from
    # growing exponentially
    if "a" in metafunc.fixturenames:
        metafunc.parametrize("a", base[:10], ids=ids[:10])
    if "b" in metafunc.fixturenames:
        metafunc.parametrize("b", base[5:15], ids=ids[5:15])
    if "c" in metafunc.fixturenames:
        metafunc.parametrize("c", base[-10:], ids=ids[-10:])

    if "base" in metafunc.fixturenames:
        metafunc.parametrize("base", base, ids=ids)


@pytest.fixture
def identity() -> Unit:
    return One


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


def test_abelian_associativity(a: Unit, b: Unit, c: Unit) -> None:
    # https://en.wikipedia.org/wiki/Abelian_group
    assert (a * b) * c == a * (b * c)


def test_abelian_identity(identity: Unit, a: Unit) -> None:
    assert identity * a == a


def test_abelian_inverse(identity: Unit, a: Unit) -> None:
    inverse = a**-1
    assert inverse * a == a * inverse
    assert inverse * a == identity
    assert identity / a == inverse


def test_abelian_commutativity(a: Unit, b: Unit) -> None:
    assert a * b == b * a


def test_no_dimensional_exponentation(base: Unit) -> None:
    with pytest.raises(TypeError):
        base**base  # type: ignore


def test_no_floating_point_exponentation(base: Unit) -> None:
    with pytest.raises(TypeError):
        base**0.5  # type: ignore


def test_no_fractional_exponentation(base: Unit) -> None:
    with pytest.raises(TypeError):
        base ** Fraction(1, 2)  # type: ignore


def test_repr_roundtrips(base: Unit) -> None:
    from measured import Dimension, Prefix  # noqa: F401

    assert eval(repr(base)) is base


def test_base_units_factor_to_themselves(base: Unit) -> None:
    assert base.factors == {base: 1}


def test_one() -> None:
    assert isinstance(One, Unit)
    assert One.dimension is Number
    assert One.name == "one"
    assert One.symbol == "1"


def test_roots() -> None:
    assert One.root(0) == One
    assert One.root(2) == One
    assert One.root(3) == One
    assert One.root(100) == One
    assert Meter.root(0) == One
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
