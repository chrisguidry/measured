from measured.computing import Furman
from measured.geometry import π
from measured.si import Arcsecond, Degree, Radian


def test_furman() -> None:
    assert 65536 * Furman == 2 * π * Radian
    assert 65536 * Furman == 360 * Degree
    assert 19.77 * Arcsecond < 1 * Furman < 20 * Arcsecond
