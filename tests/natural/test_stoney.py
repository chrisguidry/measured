from measured import Charge, Length, Mass, Time
from measured.natural import StoneyCharge, StoneyLength, StoneyMass, StoneyTime
from measured.si import Coulomb, Kilogram, Meter, Second


def test_length() -> None:
    assert StoneyLength.dimension is Length
    (1 * StoneyLength).assert_approximates(1.3807e-36 * Meter, within=2e-5)


def test_mass() -> None:
    assert StoneyMass.dimension is Mass
    (1 * StoneyMass).assert_approximates(1.8592e-9 * Kilogram, within=5e-6)


def test_time() -> None:
    assert StoneyTime.dimension is Time
    (1 * StoneyTime).assert_approximates(4.6054e-45 * Second, within=2e-5)


def test_charge() -> None:
    assert StoneyCharge.dimension is Charge
    (1 * StoneyCharge).assert_approximates(1.6022e-19 * Coulomb, within=2e-5)