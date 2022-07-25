import pytest

from measured import Level, Logarithm, Numeric, Quantity, approximately
from measured.iec import Bel, Decibel, Neper
from measured.si import Deci, Meter, Micro, Milli, Watt


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


dBW = Decibel[1 * Watt]


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
