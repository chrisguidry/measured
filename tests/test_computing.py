from measured.computing import Furman, Nibble
from measured.geometry import π
from measured.iec import Bit, Byte
from measured.si import Arcsecond, Degree, Radian


def test_furman() -> None:
    assert 65536 * Furman == 2 * π * Radian
    assert 65536 * Furman == 360 * Degree
    assert 19.77 * Arcsecond < 1 * Furman < 20 * Arcsecond


def test_nibblee() -> None:
    assert 1 * Nibble == 4 * Bit
    assert 2 * Nibble == 1 * Byte
