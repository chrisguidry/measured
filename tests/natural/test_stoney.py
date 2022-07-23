import pytest

from measured import Charge, Length, Mass, Quantity, Time, approximately
from measured.natural import StoneyCharge, StoneyLength, StoneyMass, StoneyTime
from measured.physics import G, c, e, kₑ, α, ℏ
from measured.si import Coulomb, Kilogram, Meter, Second


@pytest.mark.parametrize(
    "fundamental_constant, unity",
    [
        (c, 1 * (StoneyLength / StoneyTime)),
        (G, 1 * (StoneyLength**3 / (StoneyMass * StoneyTime**2))),
        (e, 1 * StoneyCharge),
        (
            kₑ,
            1
            * (
                (StoneyLength**3 * StoneyMass) / (StoneyTime**2 * StoneyCharge**2)
            ),
        ),
        (ℏ, α**-1 * ((StoneyLength**2 * StoneyMass) / StoneyTime)),
    ],
)
def test_unity(fundamental_constant: Quantity, unity: Quantity) -> None:
    assert fundamental_constant == approximately(unity)
    assert unity == approximately(fundamental_constant)


def test_length() -> None:
    assert StoneyLength.dimension is Length
    assert 1 * StoneyLength == approximately(1.3807e-36 * Meter, within=2e-5)


def test_mass() -> None:
    assert StoneyMass.dimension is Mass
    assert 1 * StoneyMass == approximately(1.8592e-9 * Kilogram, within=5e-6)


def test_time() -> None:
    assert StoneyTime.dimension is Time
    assert 1 * StoneyTime == approximately(4.6054e-45 * Second, within=2e-5)


def test_charge() -> None:
    assert StoneyCharge.dimension is Charge
    assert 1 * StoneyCharge == approximately(1.6022e-19 * Coulomb, within=2e-5)
