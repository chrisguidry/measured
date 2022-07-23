from decimal import Decimal
from typing import Any

import pytest
from pytest import approx

from measured import Measurement, approximately
from measured.si import Meter, Second
from measured.us import Foot


def test_addition() -> None:
    # adapted from https://www.statisticshowto.com/statistics-basics/error-propagation/
    waistband = Measurement(0.88 * Meter, 0.03)
    pant_length = Measurement(1.12 * Meter, 0.04)
    height = pant_length + waistband
    assert height.measurand == 2.0 * Meter
    assert height.uncertainty == 0.05 * Meter
    assert height.uncertainty_ratio == 0.025


def test_addition_with_quantity() -> None:
    waistband = Measurement(0.88 * Meter, 0.03)
    pant_length = 1.12 * Meter
    height = pant_length + waistband
    assert height.measurand == 2.0 * Meter
    assert height.uncertainty == 0.03 * Meter
    assert height.uncertainty_ratio == 0.015


@pytest.mark.parametrize("other", [(1.0, 1, Decimal("1.0"))])
def test_addition_only_with_measurements(other: Any) -> None:
    with pytest.raises(TypeError):
        Measurement(1 * Meter, 0.1) + other

    with pytest.raises(TypeError):
        other + Measurement(1 * Meter, 0.1)


def test_subtraction() -> None:
    # https://www.statisticshowto.com/statistics-basics/error-propagation/
    height = Measurement(2.00 * Meter, 0.03)
    waistband = Measurement(0.88 * Meter, 0.04)
    pant_length = height - waistband
    assert pant_length.measurand == 1.12 * Meter
    assert pant_length.uncertainty == 0.05 * Meter
    assert pant_length.uncertainty_ratio == approx(0.04464285)


def test_subtraction_from_quantity() -> None:
    # https://www.statisticshowto.com/statistics-basics/error-propagation/
    height = 2.00 * Meter
    waistband = Measurement(0.88 * Meter, 0.04)
    pant_length = height - waistband
    assert pant_length.measurand == 1.12 * Meter
    assert pant_length.uncertainty == 0.04 * Meter
    assert pant_length.uncertainty_ratio == approx(0.03571428)


def test_subtraction_of_quantity() -> None:
    # https://www.statisticshowto.com/statistics-basics/error-propagation/
    height = Measurement(2.00 * Meter, 0.03)
    waistband = 0.88 * Meter
    pant_length = height - waistband
    assert pant_length.measurand == 1.12 * Meter
    assert pant_length.uncertainty == 0.03 * Meter
    assert pant_length.uncertainty_ratio == approx(0.02678571)


@pytest.mark.parametrize("other", [(1.0, 1, Decimal("1.0"))])
def test_subtraction_only_with_measurements(other: Any) -> None:
    with pytest.raises(TypeError):
        Measurement(1 * Meter, 0.1) - other

    with pytest.raises(TypeError):
        other - Measurement(1 * Meter, 0.1)


def test_multiplication() -> None:
    # adapted from https://www.statisticshowto.com/statistics-basics/error-propagation/,
    # which absolutely has the wrong answer
    # Plugging the same problem into https://uncertaintycalculator.com/ agrees with
    # the results from measured
    length = Measurement(12 * Foot, 0.1)
    width = Measurement(10 * Foot, 0.1)
    height = Measurement(8 * Foot, 0.1)

    area = length * width
    assert area.measurand == 120 * Foot**2
    assert area.uncertainty == approximately(1.56204993518133 * Foot**2)
    assert area.uncertainty_ratio == approx(0.01301708)

    volume = area * height
    assert volume.measurand == 960 * Foot**3
    assert volume.uncertainty == approximately(17.3251262621662 * Foot**3)
    assert volume.uncertainty_ratio == approx(0.01804700)


def test_multiplication_by_quantity() -> None:
    length = Measurement(12 * Foot, 0.1)
    width = 10 * Foot

    area = length * width
    assert area.measurand == 120 * Foot**2
    area.uncertainty == 1.0 * Foot**2
    assert area.uncertainty_ratio == approx(0.00833333)


@pytest.mark.parametrize("other", [(1.0, 1, Decimal("1.0"))])
def test_multiplication_only_with_measurements(other: Any) -> None:
    with pytest.raises(TypeError):
        Measurement(1 * Meter, 0.1) * other

    with pytest.raises(TypeError):
        other * Measurement(1 * Meter, 0.1)


def test_division() -> None:
    volume = Measurement(960 * Foot**3, 17.3251262621662)
    length = Measurement(12 * Foot, 0.1)
    width = Measurement(10 * Foot, 0.1)

    area = volume / length
    assert area.measurand == 80 * Foot**2
    assert area.uncertainty == approximately(1.59024805891688 * Foot**2)
    assert area.uncertainty_ratio == approx(0.01987810)

    height = area / width
    assert height.measurand == 8 * Foot
    assert height.uncertainty == approximately(0.178013732304249 * Foot)
    assert height.uncertainty_ratio == approx(0.02225171)


def test_division_of_quantity() -> None:
    volume = 960 * Foot**3
    length = Measurement(12 * Foot, 0.1)

    area = volume / length
    assert area.measurand == 80 * Foot**2
    assert area.uncertainty == approximately(0.6666666666 * Foot**2)
    assert area.uncertainty_ratio == approx(0.00833333)


def test_division_by_quantity() -> None:
    volume = Measurement(960 * Foot**3, 17.3251262621662)
    length = 12 * Foot

    area = volume / length
    assert area.measurand == 80 * Foot**2
    assert area.uncertainty == approximately(1.443760522 * Foot**2)
    assert area.uncertainty_ratio == approx(0.01804700)


@pytest.mark.parametrize("other", [(1.0, 1, Decimal("1.0"))])
def test_division_only_with_measurements(other: Any) -> None:
    with pytest.raises(TypeError):
        Measurement(1 * Meter, 0.1) / other

    with pytest.raises(TypeError):
        other / Measurement(1 * Meter, 0.1)


def test_exponentation() -> None:
    side = Measurement(10 * Meter, 0.1)
    volume = side**3
    assert volume.measurand == 1000 * Meter**3
    assert volume.uncertainty == 30 * Meter**3
    assert volume.uncertainty_ratio == 0.03


@pytest.mark.parametrize("other", [(1 * Meter, 1.0, Decimal("1.0"))])
def test_exponentation_only_with_integers(other: Any) -> None:
    with pytest.raises(TypeError):
        Measurement(1 * Meter, 0.1) ** other

    with pytest.raises(TypeError):
        other ** Measurement(1 * Meter, 0.1)


@pytest.mark.parametrize(
    "left, right",
    [
        (Measurement(10 * Meter, 1), Measurement(10 * Meter, 1)),
        (Measurement(10 * Meter, 0.01), Measurement(10 * Meter, 0.01)),
        (Measurement(10 * Meter, 0.0000000001), Measurement(10 * Meter, 0.0000000001)),
        (Measurement(9.9 * Meter, 0.1), Measurement(10.1 * Meter, 0.1)),
        (Measurement(9.8 * Meter, 0.2), Measurement(10.2 * Meter, 0.2)),
        (Measurement(10 * Meter, 1), Measurement(11 * Meter, 1)),
        (Measurement(9.9 * Meter, 0.01), 9.9 * Meter),
    ],
)
def test_equality(left: Measurement, right: Measurement) -> None:
    assert left == right
    assert right == left


@pytest.mark.parametrize(
    "left, right",
    [
        (Measurement(10 * Meter, 1), Measurement(13 * Meter, 1)),
        (Measurement(10 * Meter, 0.01), Measurement(10.2 * Meter, 0.01)),
        (Measurement(9.9 * Meter, 0.01), Measurement(10.1 * Meter, 0.01)),
        (Measurement(9.9 * Meter, 0.01), 10 * Meter),
        (Measurement(9.9 * Meter, 0.01), 9.9),
    ],
)
def test_unequal(left: Measurement, right: Measurement) -> None:
    assert left != right
    assert right != left


def test_simple_inequality() -> None:
    small = Measurement(10 * Meter, 1)
    medium = Measurement(20 * Meter, 1)
    large = Measurement(30 * Meter, 1)

    assert small <= medium < large
    assert large >= medium > small


def test_inequalities_based_on_uncertainty() -> None:
    assert Measurement(10 * Meter, 1.0) < Measurement(10 * Meter, 0.1)
    assert Measurement(10 * Meter, 1.0) < Measurement(9.9 * Meter, 0.1)
    assert Measurement(10 * Meter, 1.0) > Measurement(10 * Meter, 0.5)
    assert Measurement(10 * Meter, 1.0) > Measurement(10.1 * Meter, 0.2)


def test_inequalities_coerce_to_measurements() -> None:
    length = Measurement(10 * Meter, 1)
    lesser = 8 * Meter
    greater = 20 * Meter

    assert lesser < length < greater
    assert lesser <= length <= greater
    assert greater > length > lesser
    assert greater >= length >= lesser


def test_inequalities_only_with_measurements_or_quantities() -> None:
    length = Measurement(10 * Meter, 1)

    with pytest.raises(TypeError):
        length < 100
    with pytest.raises(TypeError):
        length <= 100
    with pytest.raises(TypeError):
        length > 1
    with pytest.raises(TypeError):
        length >= 1


def test_repr() -> None:
    assert repr(Measurement(100 * Meter, 0.01)) == (
        "Measurement("
        "measurand=Quantity(magnitude=100, unit=Unit.named('meter')), "
        "uncertainty=0.01"
        ")"
    )


def test_str() -> None:
    assert str(Measurement(100 * Meter, 0.01)) == "100±0.01 m"


@pytest.mark.parametrize(
    "template, expected",
    [
        ("{speed}", "1234.5678±0.234 m⋅s⁻¹"),
        ("{speed:+}", "1234.5678±0.234 m⋅s⁻¹"),
        ("{speed:+.2f}", "1234.5678±0.23 m⋅s⁻¹"),
        ("{speed:+:.2f}", "1234.57±0.234 m⋅s⁻¹"),
        ("{speed:+:.2f:/}", "1234.57±0.234 m/s"),
        ("{speed:+.2f:.2f:/}", "1234.57±0.23 m/s"),
        ("{speed:%}", "1234.5678±0.02% m⋅s⁻¹"),  # default to 2 decimal places
        ("{speed:%.3f}", "1234.5678±0.019% m⋅s⁻¹"),
        ("{speed:%.3f::/}", "1234.5678±0.019% m/s"),
    ],
)
def test_formatting(template: str, expected: str) -> None:
    speed = Measurement(1234.5678 * Meter / Second, 0.234)
    assert template.format(speed=speed) == expected


def test_unrecognized_format_specifier() -> None:
    speed = Measurement(1234.5678 * Meter / Second, 0.234)
    with pytest.raises(ValueError, match="Unrecognized uncertainty style '🤷'"):
        speed.__format__("🤷")
