from measured import Charge, Length, Mass, Time
from measured.fundamental import G, c, e, α, ℏ
from measured.natural import StoneyCharge, StoneyLength, StoneyMass, StoneyTime
from measured.si import Coulomb, Kilogram, Meter, Second


def test_unity() -> None:
    c.assert_approximates(1 * (StoneyLength / StoneyTime))
    G.assert_approximates(1 * (StoneyLength**3 / (StoneyMass * StoneyTime**2)))
    e.assert_approximates(1 * StoneyCharge)

    # TODO: this is failing to find a conversion
    # kₑ.assert_approximates(
    #     1 * ((AtomicLength**3 * AtomicMass) / (AtomicTime**2 * AtomicCharge**2))
    # )

    ℏ.assert_approximates(α**-1 * ((StoneyLength**2 * StoneyMass) / StoneyTime))


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
