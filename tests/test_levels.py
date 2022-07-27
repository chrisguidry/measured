import pytest

from measured import (
    Bel,
    Decibel,
    Level,
    Logarithm,
    Neper,
    Numeric,
    Power,
    Pressure,
    Quantity,
    approximately,
)
from measured.acoustics import dBSPL
from measured.electronics import dBW
from measured.si import Deci, Meter, Micro, Milli, Volt, Watt


def test_logarithmic_units_are_singletons() -> None:
    assert Logarithm(base=10) is Bel
    assert (Deci * Bel) is Decibel


def test_logarithmic_units_are_not_compatible_with_linear_units() -> None:
    with pytest.raises(TypeError):
        assert Meter * Bel  # type: ignore


def test_logarithmic_units_can_be_multiplied_by_prefixes() -> None:
    decibel = Deci * Bel
    assert decibel is Decibel
    assert decibel.base == 10
    assert decibel.prefix == Deci

    millibel = Milli * Bel
    assert millibel.base == 10
    assert millibel.prefix == Milli

    microbel = Milli * (Milli * Bel)
    assert microbel.base == 10
    assert microbel.prefix == Micro


def test_logarithmic_units_do_not_produce_levels() -> None:
    with pytest.raises(TypeError):
        assert 10 * Bel  # type: ignore


def test_logarithmic_units_have_names_and_symbols() -> None:
    assert Bel.name == "bel"
    assert Bel.symbol == "bel"

    assert Decibel.name == "decibel"
    assert Decibel.symbol == "dB"

    assert Neper.name == "neper"
    assert Neper.symbol == "Np"


@pytest.mark.parametrize(
    "power, level",
    [
        (1 * Watt, 0 * dBW),
        (10 * Watt, 10 * dBW),
        (100 * Watt, 20 * dBW),
        (0.1 * Watt, -10 * dBW),
        (0.01 * Watt, -20 * dBW),
    ],
)
def test_dBW(power: Quantity, level: Level) -> None:
    assert power == level
    assert level == power


@pytest.mark.parametrize(
    "bels, decibels",
    [
        (10, 100),
        (2, 20),
        (1, 10),
        (0.1, 1),
        (0.01, 0.1),
        (0, 0),
        (-1, -10),
        (-2, -20),
        (-10, -100),
    ],
)
def test_comparing_bels_to_decibels(bels: Numeric, decibels: Numeric) -> None:
    assert bels * Bel[1 * Watt] == decibels * dBW
    assert decibels * dBW == bels * Bel[1 * Watt]


@pytest.mark.parametrize(
    "decibels, nepers",
    [
        (10, 1.151277918),
        (8.685889638, 1),
        (2, 0.2302555836),
        (1, 0.1151277918),
        (0.1, 0.0115127792),
        (0.01, 0.0011512779),
        (0, 0),
        (-1, -0.1151277918),
        (-2, -0.2302555836),
        (-8.685889638, -1),
        (-10, -1.151277918),
    ],
)
def test_comparing_decibels_to_nepers(decibels: Numeric, nepers: Numeric) -> None:
    assert nepers * Neper[1 * Watt] == approximately(decibels * dBW, within=1e5)
    assert decibels * dBW == approximately(nepers * Neper[1 * Watt], within=1e5)


def test_logarithmic_addition() -> None:
    # Example adapted from
    # https://en.wikipedia.org/wiki/Decibel#Representation_of_addition_operations
    # But switched to the less controversial unit dBW for simplicity
    assert 70 * dBW + 90 * dBW == 90.04321373782642 * dBW


def test_addition_and_subtraction_only_by_levels() -> None:
    with pytest.raises(TypeError):
        (10 * dBW) + (1 * Watt)  # type: ignore

    with pytest.raises(TypeError):
        (10 * dBW) - (1 * Watt)  # type: ignore


def test_addition_and_subtraction_only_within_same_unit() -> None:
    with pytest.raises(TypeError):
        10 * dBW + 1 * Decibel[1 * Volt]

    with pytest.raises(TypeError):
        10 * dBW - 1 * Decibel[1 * Volt]


def test_logarithmic_subtraction() -> None:
    # Example adapted from
    # https://en.wikipedia.org/wiki/Decibel#Representation_of_addition_operations
    # But switched to the less controversial unit dBW for simplicity
    assert 87 * dBW - 83 * dBW == 84.79519169458092 * dBW


def test_logarithmic_multiplication() -> None:
    assert (10 * dBW) * 2 == 12 * dBW


def test_logarithmic_division() -> None:
    assert (10 * dBW) / 2 == 8 * dBW


def test_logarithmic_multiplication_only_by_numerics() -> None:
    with pytest.raises(TypeError):
        (10 * dBW) * (2 * dBW)  # type: ignore

    with pytest.raises(TypeError):
        (10 * dBW) / (2 * dBW)  # type: ignore


def test_power_ratios() -> None:
    # https://en.wikipedia.org/wiki/Power,_root-power,_and_field_quantities

    assert dBW.reference.unit.dimension is Power
    assert dBW.power_ratio == 1

    assert dBSPL.reference.unit.dimension is Pressure
    assert dBSPL.power_ratio == 2
