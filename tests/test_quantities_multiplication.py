import pytest

from measured import Hertz, Meter, One, Quantity, Second


def pytest_generate_tests(metafunc):
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


def test_abelian_multiplication_associativity(a: Quantity, b: Quantity, c: Quantity):
    assert (a * b) * c == a * (b * c)


def test_abelian_multiplication_identity(identity: Quantity, a: Quantity):
    assert a * identity == a
    assert identity * a == a


def test_abelian_multiplication_inverse(identity: Quantity, a: Quantity):
    inverse = a**-1
    assert inverse * a == a * inverse
    assert inverse * a == identity
    assert identity / a == inverse


def test_abelian_multiplication_commutativity(a: Quantity, b: Quantity):
    assert a * b == b * a
