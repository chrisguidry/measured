from measured import Charge, Length, Mass, Time
from measured.fundamental import c, e, mₑ, α, ℏ
from measured.natural import AtomicCharge, AtomicLength, AtomicMass, AtomicTime
from measured.si import Coulomb, Kilogram, Meter, Second


def test_unity() -> None:
    e.assert_approximates(1 * AtomicCharge)
    mₑ.assert_approximates(1 * AtomicMass)
    ℏ.assert_approximates(1 * ((AtomicLength**2 * AtomicMass) / AtomicTime))

    # TODO: this is failing to find a conversion
    # kₑ.assert_approximates(
    #     1 * ((AtomicLength**3 * AtomicMass) / (AtomicTime**2 * AtomicCharge**2))
    # )

    c.assert_approximates(α**-1 * (AtomicLength / AtomicTime))


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
