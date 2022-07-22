import math
from decimal import Decimal
from typing import Any, Union

import pytest
from pytest import approx

from measured import Numeric, Quantity
from measured.si import Meter, Second
from measured.us import Foot


class Measurement:
    measurand: Quantity
    uncertainty: Quantity

    def __init__(
        self, measureand: Quantity, uncertainty: Union[Numeric, Quantity]
    ) -> None:
        self.measurand = measureand
        if not isinstance(uncertainty, Quantity):
            uncertainty = Quantity(uncertainty, measureand.unit)
        assert uncertainty.unit is measureand.unit
        self.uncertainty = uncertainty

    @property
    def uncertainty_ratio(self) -> float:
        return self.uncertainty.magnitude / self.measurand.magnitude

    @property
    def uncertainty_percent(self) -> float:
        return self.uncertainty_ratio * 100

    def __add__(self, other: "Measurement") -> "Measurement":
        if not isinstance(other, Measurement):
            return NotImplemented

        measureand = self.measurand + other.measurand
        uncertainty = (self.uncertainty**2 + other.uncertainty**2).root(2)
        return Measurement(measureand, uncertainty)

    def __sub__(self, other: "Measurement") -> "Measurement":
        if not isinstance(other, Measurement):
            return NotImplemented

        measureand = self.measurand - other.measurand
        uncertainty = (self.uncertainty**2 + other.uncertainty**2).root(2)
        return Measurement(measureand, uncertainty)

    def __mul__(self, other: "Measurement") -> "Measurement":
        if not isinstance(other, Measurement):
            return NotImplemented

        measureand = self.measurand * other.measurand
        uncertainty = math.sqrt(
            measureand.magnitude**2
            * (
                (self.uncertainty.magnitude**2 / self.measurand.magnitude**2)
                + (other.uncertainty.magnitude**2 / other.measurand.magnitude**2)
            )
        )
        return Measurement(measureand, uncertainty)

    def __truediv__(self, other: "Measurement") -> "Measurement":
        if not isinstance(other, Measurement):
            return NotImplemented

        measureand = self.measurand / other.measurand
        uncertainty = math.sqrt(
            measureand.magnitude**2
            * (
                (self.uncertainty.magnitude**2 / self.measurand.magnitude**2)
                + (other.uncertainty.magnitude**2 / other.measurand.magnitude**2)
            )
        )
        return Measurement(measureand, uncertainty)

    def __pow__(self, exponent: int) -> "Measurement":
        if not isinstance(exponent, int):
            return NotImplemented

        measureand = self.measurand**exponent
        uncertainty = math.sqrt(
            (exponent * self.measurand.magnitude**2 * self.uncertainty.magnitude) ** 2
        )
        return Measurement(measureand, uncertainty)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Measurement):
            return False

        self_lower = self.measurand - self.uncertainty
        self_upper = self.measurand + self.uncertainty
        other_lower = other.measurand - other.uncertainty
        other_upper = other.measurand + other.uncertainty

        overlaps_lower = self_lower <= other_lower <= self_upper
        overlaps_upper = self_lower <= other_upper <= self_upper
        return overlaps_lower or overlaps_upper

    def __repr__(self) -> str:
        return (
            "Measurement("
            f"measurand={self.measurand!r}, "
            f"uncertainty={self.uncertainty.magnitude!r}"
            ")"
        )

    def __str__(self) -> str:
        return self.__format__("")

    def __format__(self, format_specifier: str) -> str:
        uncertainty_format, _, quantity_format = format_specifier.partition(":")

        style, magnitude_format = "", ""
        if uncertainty_format:
            style, magnitude_format = uncertainty_format[0], uncertainty_format[1:]

        if style in ("", "+", "±"):
            magnitude = self.uncertainty.magnitude.__format__(magnitude_format)
            uncertainty = f"±{magnitude}"
        elif style == "%":
            magnitude_format = magnitude_format or ".2f"
            percent = self.uncertainty_percent.__format__(magnitude_format)
            uncertainty = f"±{percent}%"
        else:
            raise ValueError(f"Unrecognized uncertainty style {style!r}")

        magnitude_format, _, unit_format = quantity_format.partition(":")
        magnitude = self.measurand.magnitude.__format__(magnitude_format)
        unit = self.measurand.unit.__format__(unit_format)
        return f"{magnitude}{uncertainty} {unit}"


def test_addition() -> None:
    # adapted from https://www.statisticshowto.com/statistics-basics/error-propagation/
    waistband = Measurement(0.88 * Meter, 0.03)
    pant_length = Measurement(1.12 * Meter, 0.04)
    height = pant_length + waistband
    assert height.measurand == 2.0 * Meter
    assert height.uncertainty == 0.05 * Meter
    assert height.uncertainty_ratio == 0.025


@pytest.mark.parametrize("other", [(1 * Meter, 1.0, 1, Decimal("1.0"))])
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


@pytest.mark.parametrize("other", [(1 * Meter, 1.0, 1, Decimal("1.0"))])
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
    area.uncertainty.assert_approximates(1.56204993518133 * Foot**2)
    assert area.uncertainty_ratio == approx(0.01301708)

    volume = area * height
    assert volume.measurand == 960 * Foot**3
    volume.uncertainty.assert_approximates(17.3251262621662 * Foot**3)
    assert volume.uncertainty_ratio == approx(0.01804700)


@pytest.mark.parametrize("other", [(1 * Meter, 1.0, 1, Decimal("1.0"))])
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
    area.uncertainty.assert_approximates(1.59024805891688 * Foot**2)
    assert area.uncertainty_ratio == approx(0.01987810)

    height = area / width
    assert height.measurand == 8 * Foot
    height.uncertainty.assert_approximates(0.178013732304249 * Foot)
    assert height.uncertainty_ratio == approx(0.02225171)


@pytest.mark.parametrize("other", [(1 * Meter, 1.0, 1, Decimal("1.0"))])
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
        (Measurement(9.9 * Meter, 0.01), 9.9 * Meter),
        (Measurement(9.9 * Meter, 0.01), 9.9),
    ],
)
def test_unequal(left: Measurement, right: Measurement) -> None:
    assert left != right
    assert right != left


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
    with pytest.raises(ValueError, match="Unrecognized uncertainty style '!'"):
        speed.__format__("!")
