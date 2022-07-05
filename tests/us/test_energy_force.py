from measured import Force
from measured.physics import gₙ
from measured.si import Newton
from measured.us import Pound, PoundForce


def test_poundforce() -> None:
    assert PoundForce.name == "pound-force"
    assert PoundForce.symbol == "lbf"
    assert PoundForce.dimension is Force
    assert 1 * PoundForce == 1 * Pound * gₙ
    assert 1 * PoundForce == 4.4482216152605 * Newton
