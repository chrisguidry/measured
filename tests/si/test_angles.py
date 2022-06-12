from measured import One
from measured.si import Meter, Radian, Steradian


def test_radian_is_dimensionless() -> None:
    assert Radian == Meter / Meter
    assert Radian == One
    assert Radian.name == "one"
    assert Radian.symbol == "1"
    assert Radian.names == ["one", "radian", "steradian"]
    assert Radian.symbols == ["1", "rad", "sr"]


def test_steradian_is_dimensionless() -> None:
    assert Steradian == Meter / Meter
    assert Steradian == One
    assert Steradian.name == "one"
    assert Steradian.symbol == "1"
    assert Steradian.names == ["one", "radian", "steradian"]
    assert Steradian.symbols == ["1", "rad", "sr"]
