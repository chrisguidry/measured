from measured import Acceleration, Force, Pressure, approximately
from measured.physics import gₙ
from measured.si import Kilo, Newton, Pascal, Second
from measured.us import PSI, Foot, GForce, Pound, PoundForce


def test_g_force() -> None:
    assert GForce.name == "g-force"
    assert GForce.symbol == "g-force"
    assert GForce.dimension is Acceleration
    assert 1 * GForce == gₙ
    assert 1 * GForce == approximately(32.17405 * Foot / Second**2, 5e-8)


def test_poundforce() -> None:
    assert PoundForce.name == "pound-force"
    assert PoundForce.symbol == "lbf"
    assert PoundForce.dimension is Force
    assert 1 * PoundForce == 1 * Pound * gₙ
    assert 1 * PoundForce == 1 * Pound * GForce
    assert 1 * PoundForce == 4.4482216152605 * Newton


def test_psi() -> None:
    assert PSI.name == "pounds per square inch"
    assert PSI.symbol == "psi"
    assert PSI.dimension is Pressure
    assert 1 * PSI == approximately(6894.757 * Pascal, 5e-8)
    assert 1 * PSI == approximately(6.894757 * Kilo * Pascal, 5e-8)
