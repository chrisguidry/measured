import pytest

from measured import One, Quantity
from measured.si import Hertz, Meter, Second


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    examples = [
        1 * Meter,
        2 * Second,
        3 * Hertz,
        4 * Meter / Second,
        5 * Meter**2,
        6 * Meter**2 / Second**2,
    ]

    for exemplar in ["a", "b", "c"]:
        if exemplar in metafunc.fixturenames:
            metafunc.parametrize(exemplar, examples)


@pytest.fixture
def identity() -> Quantity:
    return 1 * One


def test_multiplication_associativity(a: Quantity, b: Quantity, c: Quantity) -> None:
    assert (a * b) * c == a * (b * c)


def test_multiplication_identity(identity: Quantity, a: Quantity) -> None:
    assert a * identity == a
    assert identity * a == a


def test_multiplication_inverse(identity: Quantity, a: Quantity) -> None:
    inverse = a**-1
    assert inverse * a == a * inverse
    assert inverse * a == identity
    assert identity / a == inverse


def test_multiplication_commutativity(a: Quantity, b: Quantity) -> None:
    assert a * b == b * a
