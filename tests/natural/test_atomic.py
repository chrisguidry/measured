import pytest

from measured import Charge, Length, Mass, Quantity, Time, approximately
from measured.natural import AtomicCharge, AtomicLength, AtomicMass, AtomicTime
from measured.physics import c, e, kₑ, mₑ, α, ℏ
from measured.si import Coulomb, Kilogram, Meter, Second


@pytest.mark.parametrize(
    "fundamental_constant, unity",
    [
        (e, 1 * AtomicCharge),
        (mₑ, 1 * AtomicMass),
        (ℏ, 1 * ((AtomicLength**2 * AtomicMass) / AtomicTime)),
        (
            kₑ,
            (
                1
                * (AtomicLength**3 * AtomicMass)
                / (AtomicTime**2 * AtomicCharge**2)
            ),
        ),
        (c, α**-1 * (AtomicLength / AtomicTime)),
    ],
)
def test_unity(fundamental_constant: Quantity, unity: Quantity) -> None:
    assert fundamental_constant == approximately(unity)
    assert unity == approximately(fundamental_constant)


def test_length() -> None:
    assert AtomicLength.dimension is Length
    assert 1 * AtomicLength == approximately(5.292e-11 * Meter, within=5e-5)


def test_mass() -> None:
    assert AtomicMass.dimension is Mass
    assert 1 * AtomicMass == approximately(9.109e-31 * Kilogram, within=5e-5)


def test_time() -> None:
    assert AtomicTime.dimension is Time
    assert 1 * AtomicTime == approximately(2.419e-17 * Second, within=5e-5)


def test_charge() -> None:
    assert AtomicCharge.dimension is Charge
    assert 1 * AtomicCharge == approximately(1.6022e-19 * Coulomb, within=2e-5)
