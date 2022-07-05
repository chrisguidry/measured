from measured import Force, Pressure
from measured.physics import gₙ
from measured.si import Kilo, Newton, Pascal
from measured.us import PSI, Inch, Pound, PoundForce


def test_poundforce() -> None:
    assert PoundForce.name == "pound-force"
    assert PoundForce.symbol == "lbf"
    assert PoundForce.dimension is Force
    assert 1 * PoundForce == 1 * Pound * gₙ
    assert 1 * PoundForce == 4.4482216152605 * Newton


def test_psi() -> None:
    assert PSI.name == "pound per square inch"
    assert PSI.symbol == "psi"
    assert PSI.dimension == Pressure
    assert 1 * PSI == 1 * PoundForce / Inch**2
    assert 1 * PSI == 6.894757293168 * Kilo * Pascal
