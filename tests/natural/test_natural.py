from measured import Charge, Length, Mass, Time
from measured.fundamental import c, mₑ, ℏ
from measured.natural import NaturalCharge, NaturalLength, NaturalMass, NaturalTime
from measured.si import Coulomb, Kilogram, Meter, Second


def test_unity() -> None:
    c.assert_approximates(1 * (NaturalLength / NaturalTime))
    mₑ.assert_approximates(1 * NaturalMass)
    ℏ.assert_approximates(1 * ((NaturalLength**2 * NaturalMass) / NaturalTime))

    # TODO: this is failing to find a conversion
    # ε0.assert_approximates(
    #     1
    #     * ((NaturalTime**2 * NaturalCharge**2) / (NaturalMass * NaturalLength**3))
    # )


def test_length() -> None:
    assert NaturalLength.dimension is Length
    (1 * NaturalLength).assert_approximates(3.862e-13 * Meter, within=2e-4)


def test_mass() -> None:
    assert NaturalMass.dimension is Mass
    (1 * NaturalMass).assert_approximates(9.109e-31 * Kilogram, within=5e-5)


def test_time() -> None:
    assert NaturalTime.dimension is Time
    (1 * NaturalTime).assert_approximates(1.288e-21 * Second, within=7e-5)


def test_charge() -> None:
    assert NaturalCharge.dimension is Charge
    (1 * NaturalCharge).assert_approximates(5.291e-19 * Coulomb, within=4e-5)
