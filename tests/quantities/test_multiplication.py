import pytest
from hypothesis import assume, given

from measured import One, Quantity
from measured.hypothesis import quantities


@pytest.fixture(scope="module")
def identity() -> Quantity:
    return 1 * One


@given(a=quantities(), b=quantities(), c=quantities())
def test_associativity(a: Quantity, b: Quantity, c: Quantity) -> None:
    ((a * b) * c).assert_approximates(a * (b * c))


@given(a=quantities())
def test_identity(identity: Quantity, a: Quantity) -> None:
    assert a * identity == a
    assert identity * a == a


@given(a=quantities())
def test_inverse(identity: Quantity, a: Quantity) -> None:
    assume(a.magnitude != 0)

    inverse = a**-1
    assert inverse * a == a * inverse
    (inverse * a).assert_approximates(identity)
    (identity / a).assert_approximates(inverse)


@given(a=quantities(), b=quantities())
def test_commutativity(a: Quantity, b: Quantity) -> None:
    assert a * b == b * a
