from measured import Length
from measured.iec import RackUnit
from measured.us import Inch


def test_rack_unit() -> None:
    assert RackUnit.dimension is Length
    assert RackUnit.name == "rack unit"
    assert RackUnit.symbol == "U"
    assert 1 * RackUnit == 1.75 * Inch
