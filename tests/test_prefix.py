import pytest

from measured.iec import Bit, Kibi
from measured.si import Kilo, Mega, Meter, Micro, Second


def test_prefixes_scale_quantities_up():
    length = 3 * (Kilo * Meter)
    assert length == 3000 * Meter


def test_prefixes_scale_quantities_down():
    length = 3 * (Micro * Meter)
    assert length == 0.000003 * Meter


def test_equal_prefixes_cancel():
    speed = (15 * (Kilo * Meter)) / (3 * (Kilo * Second))
    assert speed == (5 * (Kilo * Meter)) / (Kilo * Second)
    assert speed == (5000 * Meter) / (1000 * Second)
    assert speed == 5 * Meter / Second


def test_different_prefixes_cancel():
    speed = (15 * (Mega * Meter)) / (3 * (Kilo * Second))
    assert speed == (15 * (Kilo * Meter)) / (3 * Second)
    assert speed == (5 * (Kilo * Meter)) / Second
    assert speed == 5000 * Meter / Second


def test_cannot_multiply_prefixes_in_different_bases():
    with pytest.raises(TypeError):
        5 * (Kilo * Kibi) * Meter


def test_cannot_divide_prefixes_in_different_bases():
    with pytest.raises(TypeError):
        5 * (Kilo / Kibi) * Meter


def test_can_compare_quantities_with_different_prefixes():
    assert 1.0 * (Kibi * Bit) == 1.024 * (Kilo * Bit)


def test_can_mix_prefixes_with_same_base():
    assert 5 * ((Kilo * Mega) * Meter) == 5000000000 * Meter


def test_prefixes_cannot_be_multiplied_by_numbers():
    with pytest.raises(TypeError):
        5 * Kilo

    with pytest.raises(TypeError):
        Kilo * 5


def test_prefixes_cannot_divide_with_numbers():
    with pytest.raises(TypeError):
        Kilo / 5

    with pytest.raises(TypeError):
        5 / Kilo
