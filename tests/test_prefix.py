import pytest

from measured import One
from measured.iec import Bit, Kibi, Mebi
from measured.si import Kilo, Mega, Meter, Micro, Milli, Second


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


def test_can_compare_quantities_with_different_prefixes():
    assert 1.0 * (Kibi * Bit) == 1.024 * (Kilo * Bit)


def test_can_multiply_prefixes_with_same_base():
    assert 5 * ((Kilo * Mega) * Meter) == 5000000000 * Meter


def test_can_multiply_prefixes_with_different_bases():
    iec_first = 5 * (Kibi * Mega) * Meter
    si_first = 5 * (Mega * Kibi) * Meter
    assert iec_first.approximates(si_first, within=1e-3)
    assert iec_first.approximates(5120000000 * Meter, within=1e-3)
    assert si_first.approximates(5120000000 * Meter, within=1e-3)


def test_can_divide_prefixes_with_same_base():
    assert 5 * (Mega / Kilo) * Meter == 5000 * Meter


def test_can_divide_prefixes_with_different_bases():
    assert (5 * (Mebi / Kilo) * Meter).approximates(5242.88 * Meter, within=1e-6)
    assert (5 * (Mega / Kibi) * Meter).approximates(4882.8125 * Meter, within=1e-6)


def test_multiplying_produces_number_quantities():
    assert 5 * Kilo == 5000 * One
    assert 5 * Milli == 0.005 * One


def test_associative_with_multiplication():
    assert (5 * Kilo) * Meter == 5 * (Kilo * Meter)


def test_associative_in_denominator():
    assert 10000 * Meter / (5 * Kilo * Second) == 2 * Meter / Second


def test_multiplying_by_random_things():
    with pytest.raises(TypeError):
        "hello" * Kilo

    with pytest.raises(TypeError):
        Kilo * "hello"


def test_dividing_by_random_things():
    with pytest.raises(TypeError):
        "hello" / Kilo

    with pytest.raises(TypeError):
        Kilo / "hello"
