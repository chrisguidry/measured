from measured import approximately
from measured.eu import Gradian
from measured.geometry import π
from measured.si import Arcminute, Degree, Radian


def test_gradian() -> None:
    assert 1 * Gradian == (π / 200 * Radian)
    assert 1 * Gradian == (9 / 10 * Degree)
    assert 1 * Gradian == approximately(54 * Arcminute)
