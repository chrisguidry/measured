from measured import Area, approximately
from measured.metric import Barn, Outhouse, Shake, Shed
from measured.si import Meter, Micro, Nano, Second, Yocto


def test_barn() -> None:
    assert Barn.dimension is Area
    assert Barn.name == "barn"
    assert Barn.symbol == "barn"  # we already have a 'b' symbol at measured.iec.Bit
    assert 1 * Barn == approximately(1e-28 * Meter**2)


def test_outhouse() -> None:
    assert Outhouse.dimension is Area
    assert Outhouse.name == "outhouse"
    assert Outhouse.symbol == "outhouse"
    assert 1 * Outhouse == approximately(1 * Micro * Barn)
    assert 1 * Outhouse == approximately(1e-34 * Meter**2)


def test_shed() -> None:
    assert Shed.dimension is Area
    assert Shed.name == "shed"
    assert Shed.symbol == "shed"
    assert 1 * Shed == approximately(1 * Yocto * Barn)
    assert 1 * Shed == approximately(1e-52 * Meter**2)


def test_shake() -> None:
    assert 1 * Shake == 10 * Nano * Second
