import pytest

from measured import Information, One, Quantity
from measured.iec import Bit, Byte, Gibi, Kibi, Mebi, Shannon
from measured.si import Giga, Kilo, Mega, Second


def test_shannons_measure_information() -> None:
    assert Shannon.dimension is Information
    assert Shannon.name == "shannon"
    assert Shannon.symbol == "Sh"


def test_bits_measure_information() -> None:
    assert Bit.dimension is Information
    assert Bit.name == "bit"
    assert Bit.symbol == "b"


def test_bytes_measure_information() -> None:
    assert Byte.dimension is Information
    assert Byte.name == "byte"
    assert Byte.symbol == "B"


def test_bit_is_equivalent_to_shannon() -> None:
    assert 1 * Bit == 1 * Shannon
    assert 1 * Shannon == 1 * Bit


def test_bytes_are_8_bits() -> None:
    assert 8 * Bit == 1 * Byte
    assert 1 * (Byte / Bit) == 8 * One
    assert 1 * Byte / Bit == 8 * One


def test_iec_prefixes() -> None:
    assert 1024 * (Kibi * Byte) == 1 * (Mebi * Byte)


def test_data_rates() -> None:
    assert 1024 * (Mebi * Byte) / Second == 1 * (Gibi * Byte / Second)


@pytest.mark.parametrize(
    "iec, si",
    [
        (1 * (Kilo * Bit), 0.9765625 * (Kibi * Bit)),
        (1 * (Mega * Bit), 0.95367431640625 * (Mebi * Bit)),
        (1 * (Giga * Bit), 0.9313225746154785 * (Gibi * Bit)),
    ],
)
def test_bit_iec_si_compatibility(iec: Quantity, si: Quantity) -> None:
    assert iec == si


@pytest.mark.parametrize(
    "iec, si",
    [
        (1 * (Kilo * Byte), 0.9765625 * (Kibi * Byte)),
        (1 * (Mega * Byte), 0.95367431640625 * (Mebi * Byte)),
        (1 * (Giga * Byte), 0.9313225746154785 * (Gibi * Byte)),
        (1 * (Kilo * Byte), 8 * 0.9765625 * (Kibi * Bit)),
        (1 * (Mega * Byte), 8 * 0.95367431640625 * (Mebi * Bit)),
        (1 * (Giga * Byte), 8 * 0.9313225746154785 * (Gibi * Bit)),
        (8 * (Kilo * Bit), 0.9765625 * (Kibi * Byte)),
        (8 * (Mega * Bit), 0.95367431640625 * (Mebi * Byte)),
        (8 * (Giga * Bit), 0.9313225746154785 * (Gibi * Byte)),
    ],
)
def test_byte_iec_si_compatibility(iec: Quantity, si: Quantity) -> None:
    difference = iec.in_base_units() - si.in_base_units()
    assert iec.approximates(si), f"{iec} and {si} differ by {difference}"
