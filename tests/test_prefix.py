import pytest

from measured import IdentityPrefix, One, Prefix
from measured.iec import Bit, Kibi, Mebi
from measured.si import Deci, Kilo, Mega, Meter, Micro, Milli, Second


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "prefix" in metafunc.fixturenames:
        examples = [Kibi, Mebi, Milli, Deci, Kilo, Mega]
        ids = [d.name for d in examples]
        metafunc.parametrize("prefix", examples, ids=ids)


def test_repr(prefix: Prefix) -> None:
    assert repr(prefix) == f"Prefix(base={prefix.base!r}, exponent={prefix.exponent!r})"


def test_repr_roundtrips(prefix: Prefix) -> None:
    assert eval(repr(prefix)) is prefix


def test_prefixes_scale_quantities_up() -> None:
    length = 3 * (Kilo * Meter)
    assert length == 3000 * Meter


def test_prefixes_scale_quantities_down() -> None:
    length = 3 * (Micro * Meter)
    assert length == 0.000003 * Meter


def test_equal_prefixes_cancel() -> None:
    speed = (15 * (Kilo * Meter)) / (3 * (Kilo * Second))
    assert speed == (5 * (Kilo * Meter)) / (Kilo * Second)
    assert speed == (5000 * Meter) / (1000 * Second)
    assert speed == 5 * Meter / Second


def test_different_prefixes_cancel() -> None:
    speed = (15 * (Mega * Meter)) / (3 * (Kilo * Second))
    assert speed == (15 * (Kilo * Meter)) / (3 * Second)
    assert speed == (5 * (Kilo * Meter)) / Second
    assert speed == 5000 * Meter / Second


def test_can_compare_quantities_with_different_prefixes() -> None:
    assert 1.0 * (Kibi * Bit) == 1.024 * (Kilo * Bit)


def test_can_multiply_prefixes_with_same_base() -> None:
    assert 5 * ((Kilo * Mega) * Meter) == 5000000000 * Meter


def test_can_multiply_prefixes_with_different_bases() -> None:
    iec_first = 5 * (Kibi * Mega) * Meter
    si_first = 5 * (Mega * Kibi) * Meter
    iec_first.assert_approximates(si_first, within=1e-3)
    iec_first.assert_approximates(5120000000 * Meter, within=1e-3)
    si_first.assert_approximates(5120000000 * Meter, within=1e-3)


def test_can_divide_prefixes_with_same_base() -> None:
    assert 5 * (Mega / Kilo) * Meter == 5000 * Meter


def test_can_divide_prefixes_with_different_bases() -> None:
    (5 * (Mebi / Kilo) * Meter).assert_approximates(5242.88 * Meter, within=1e-6)
    (5 * (Mega / Kibi) * Meter).assert_approximates(4882.8125 * Meter, within=1e-6)


def test_multiplying_produces_number_quantities() -> None:
    assert 5 * Kilo == 5000 * One
    assert 5 * Milli == 0.005 * One


def test_associative_with_multiplication() -> None:
    assert (5 * Kilo) * Meter == 5 * (Kilo * Meter)


def test_associative_in_denominator() -> None:
    assert 10000 * Meter / (5 * Kilo * Second) == 2 * Meter / Second


def test_multiplying_by_random_things() -> None:
    with pytest.raises(TypeError):
        "hello" * Kilo  # type: ignore

    with pytest.raises(TypeError):
        Kilo * "hello"  # type: ignore


def test_dividing_by_random_things() -> None:
    with pytest.raises(TypeError):
        "hello" / Kilo  # type: ignore

    with pytest.raises(TypeError):
        Kilo / "hello"  # type: ignore


def test_roots() -> None:
    assert Mega.root(0) == IdentityPrefix
    assert Mega.root(2) == Kilo
    assert Mebi.root(2) == Kibi


def test_only_integer_roots() -> None:
    with pytest.raises(TypeError):
        Deci.root(0.5)  # type: ignore


def test_whole_power_roots_only() -> None:
    with pytest.raises(ValueError):
        Deci.root(3)
