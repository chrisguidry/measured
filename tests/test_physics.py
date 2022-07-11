import pytest

from measured import (
    Acceleration,
    Area,
    Capacitance,
    Charge,
    Dimension,
    Energy,
    Force,
    Length,
    Mass,
    Number,
    One,
    Quantity,
    Speed,
    Temperature,
    Time,
    Volume,
    physics,
)
from measured.si import (
    Coulomb,
    Dalton,
    ElectronVolt,
    Farad,
    Joule,
    Kelvin,
    Kilogram,
    Mega,
    Meter,
    Second,
    Volt,
)
from measured.us import Foot


@pytest.mark.parametrize(
    "constant, dimension",
    [
        (physics.c, Speed),
        (physics.G, Volume / (Mass * Time**2)),
        (physics.h, Energy * Time),
        (physics.ℏ, Energy * Time),
        (physics.k, Energy / Temperature),
        (physics.e, Charge),
        (physics.ε0, Capacitance / Length),
        (physics.mₑ, Mass),
        (physics.kₑ, ((Force * Area) / Charge**2)),
        (physics.α, Number),
        (physics.gₙ, Acceleration),
    ],
)
def test_constants_have_expected_dimension(
    constant: Quantity, dimension: Dimension
) -> None:
    assert constant.unit.dimension is dimension


# https://en.wikipedia.org/wiki/Physical_constant#Table_of_physical_constants
# While these are redundant (quite a few are _defined_ in Si units), this test is
# intended to give flexibility about redefining constants in terms of others.  This test
# confirms that no matter what, we can always depend on their SI conversions.
@pytest.mark.parametrize(
    "constant, expected",
    [
        (physics.c, 299792458 * Meter / Second),
        (physics.G, 6.6743015e-11 * Meter**3 / (Kilogram * Second**2)),
        (physics.h, 6.62607015e-34 * Joule * Second),
        (physics.ℏ, 1.0545718176461565e-34 * Joule * Second),
        (physics.k, 1.380649e-23 * Joule / Kelvin),
        (physics.e, 1.602176634e-19 * Coulomb),
        (physics.ε0, 8.8541878128e-12 * Farad / Meter),
        (physics.mₑ, 9.1093837015e-31 * Kilogram),
        (physics.mₑ, 0.0005485799090649074 * Dalton),
        (physics.e, 1.602176634e-19 * Coulomb),
        (
            physics.kₑ,
            8.9875517923e9 * (Kilogram * Meter**3) / (Second**2 * Coulomb**2),
        ),
        (physics.α, 1 / 137.035999206 * One),
        (physics.gₙ, 9.80665 * Meter / Second**2),
        (physics.gₙ, 32.174049 * Foot / Second**2),
    ],
)
def test_constants_have_expected_si_values(
    constant: Quantity, expected: Quantity
) -> None:
    constant.assert_approximates(expected)


def test_electronvolt() -> None:
    c = physics.c
    e = physics.e

    assert (1 * ElectronVolt) == e * Volt
    (1 * ElectronVolt / c**2).assert_approximates(1.78266192e-36 * Kilogram)
    (1 * (Mega * ElectronVolt) / c**2).assert_approximates(0.0010735441 * Dalton)
