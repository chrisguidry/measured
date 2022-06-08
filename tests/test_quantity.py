import pytest

from measured import Meter, Second


@pytest.mark.xfail
def test_constructing_quantities_by_multiplying_units():
    assert Meter * 5 == 5 * Meter


@pytest.mark.xfail
def test_constructing_quantities_by_dividing_units():
    assert Second / 4 == 0.25 * Second
