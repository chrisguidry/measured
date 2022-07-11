from measured.eu import Gradian
from measured.geometry import π
from measured.si import Arcminute, Degree, Radian


def test_gradian() -> None:
    assert (1 * Gradian) == (π / 200 * Radian)
    assert (1 * Gradian) == (9 / 10 * Degree)
    (1 * Gradian).assert_approximates((54 * Arcminute))
