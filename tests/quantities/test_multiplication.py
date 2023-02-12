import pytest
from hypothesis import HealthCheck, assume, given, settings

from measured import One, Quantity, approximately
from measured.hypothesis import quantities


@pytest.fixture(scope="module")
def identity() -> Quantity:
    return 1 * One


@given(a=quantities(), b=quantities(), c=quantities())
@settings(suppress_health_check=(HealthCheck.too_slow,))
def test_associativity(a: Quantity, b: Quantity, c: Quantity) -> None:
    assert (a * b) * c == approximately(a * (b * c))


@given(a=quantities())
def test_identity(identity: Quantity, a: Quantity) -> None:
    assert a * identity == a
    assert identity * a == a


@given(a=quantities())
def test_inverse(identity: Quantity, a: Quantity) -> None:
    assume(a.magnitude != 0)

    inverse = a**-1
    assert inverse * a == a * inverse
    assert inverse * a == approximately(identity)
    assert identity / a == approximately(inverse)


@given(a=quantities(), b=quantities())
def test_commutativity(a: Quantity, b: Quantity) -> None:
    assert a * b == b * a
