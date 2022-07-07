from measured import Acceleration, Force
from measured.physics import gₙ
from measured.si import Newton, Second
from measured.us import Foot, GForce, Pound, PoundForce


def test_g_force() -> None:
    assert GForce.name == "g-force"
    assert GForce.symbol == "g-force"
    assert GForce.dimension is Acceleration
    assert 1 * GForce == gₙ
    assert 1 * GForce == 32.17405 * Foot / Second**2


def test_poundforce() -> None:
    assert PoundForce.name == "pound-force"
    assert PoundForce.symbol == "lbf"
    assert PoundForce.dimension is Force
    assert 1 * PoundForce == 1 * Pound * gₙ
    assert 1 * PoundForce == 1 * Pound * GForce
    assert 1 * PoundForce == 4.4482216152605 * Newton
