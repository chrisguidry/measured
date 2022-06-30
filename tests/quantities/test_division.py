import pytest

from measured import Length
from measured.si import Meter


def test_division_of_numbers_by_integer_quantities() -> None:
    assert 1 / 5 * Meter == 0.20 * Meter
    assert 1 / (5 * Meter) == 0.20 * Meter

    assert 4 / 2 * Meter == 2 * Meter
    assert 4 / (2 * Meter) == 2 * Meter


def test_division_of_numbers_by_float_quantities() -> None:
    assert 1.0 / 5 * Meter == 0.20 * Meter
    assert 1.0 / (5 * Meter) == 0.20 * Meter


def test_only_numbers_may_be_divided_by_quantities() -> None:
    with pytest.raises(TypeError):
        "wat" / (1 * Meter)  # type: ignore

    with pytest.raises(TypeError):
        Length / (1 * Meter)  # type: ignore
