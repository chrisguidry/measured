from measured import Charge, Length, Mass, Time
from measured.natural import AtomicCharge, AtomicLength, AtomicMass, AtomicTime
from measured.si import Coulomb, Kilogram, Meter, Second


def test_length() -> None:
    assert AtomicLength.dimension is Length
    (1 * AtomicLength).assert_approximates(5.292e-11 * Meter, within=5e-5)


def test_mass() -> None:
    assert AtomicMass.dimension is Mass
    (1 * AtomicMass).assert_approximates(9.109e-31 * Kilogram, within=5e-5)


def test_time() -> None:
    assert AtomicTime.dimension is Time
    (1 * AtomicTime).assert_approximates(2.419e-17 * Second, within=5e-5)


def test_charge() -> None:
    assert AtomicCharge.dimension is Charge
    (1 * AtomicCharge).assert_approximates(1.6022e-19 * Coulomb, within=2e-05)
