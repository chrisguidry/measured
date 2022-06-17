from fractions import Fraction

import pytest

from measured import Number, One, Unit


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


def test_repr(base: Unit) -> None:
    r = repr(base)
    assert r.startswith("<Unit(dimension=")
    assert base.dimension.name and base.dimension.name in r
    assert base.name and base.name in r
    assert base.symbol and base.symbol in r
    assert r.endswith(")>")


def test_base_units_factor_to_themselves(base: Unit) -> None:
    assert base.factors == {base: 1}


def test_one() -> None:
    assert isinstance(One, Unit)
    assert One.dimension is Number
    assert One.name == "one"
    assert One.symbol == "1"
