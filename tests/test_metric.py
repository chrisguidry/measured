from measured import Area
from measured.metric import Barn, Outhouse, Shake, Shed
from measured.si import Meter, Micro, Nano, Second, Yocto


def test_barn() -> None:
    assert Barn.dimension is Area
    assert Barn.name == "barn"
    assert Barn.symbol == "barn"  # we already have a 'b' symbol at measured.iec.Bit
    (1 * Barn).assert_approximates(1e-28 * Meter**2)


def test_outhouse() -> None:
    assert Outhouse.dimension is Area
    assert Outhouse.name == "outhouse"
    assert Outhouse.symbol == "outhouse"
    (1 * Outhouse).assert_approximates(1 * Micro * Barn)
    (1 * Outhouse).assert_approximates(1e-34 * Meter**2)


def test_shed() -> None:
    assert Shed.dimension is Area
    assert Shed.name == "shed"
    assert Shed.symbol == "shed"
    (1 * Shed).assert_approximates(1 * Yocto * Barn)
    (1 * Shed).assert_approximates(1e-52 * Meter**2)


def test_shake() -> None:
    assert 1 * Shake == 10 * Nano * Second
