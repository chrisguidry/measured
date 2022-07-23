import pytest

from measured import Charge, Length, Mass, Quantity, Time, approximately
from measured.natural import NaturalCharge, NaturalLength, NaturalMass, NaturalTime
from measured.physics import c, mₑ, ε0, ℏ
from measured.si import Coulomb, Kilogram, Meter, Second


@pytest.mark.parametrize(
    "fundamental_constant, unity",
    [
        (c, 1 * (NaturalLength / NaturalTime)),
        (mₑ, 1 * NaturalMass),
        (ℏ, 1 * ((NaturalLength**2 * NaturalMass) / NaturalTime)),
        (
            ε0,
            (
                1
                * (
                    (NaturalTime**2 * NaturalCharge**2)
                    / (NaturalMass * NaturalLength**3)
                )
            ),
        ),
    ],
)
def test_unity(fundamental_constant: Quantity, unity: Quantity) -> None:
    assert fundamental_constant == approximately(unity)
    assert unity == approximately(fundamental_constant)


def test_length() -> None:
    assert NaturalLength.dimension is Length
    assert 1 * NaturalLength == approximately(3.862e-13 * Meter, within=2e-4)


def test_mass() -> None:
    assert NaturalMass.dimension is Mass
    assert 1 * NaturalMass == approximately(9.109e-31 * Kilogram, within=5e-5)


def test_time() -> None:
    assert NaturalTime.dimension is Time
    assert 1 * NaturalTime == approximately(1.288e-21 * Second, within=7e-5)


def test_charge() -> None:
    assert NaturalCharge.dimension is Charge
    assert 1 * NaturalCharge == approximately(5.291e-19 * Coulomb, within=4e-5)
