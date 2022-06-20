from measured.si import Centi, Deci, Kilo, Liter, Meter, Milli

cm = Centi * Meter
km = Kilo * Meter


def test_length_equivalence() -> None:
    assert 1 * Meter == 100 * cm
    assert 1 * Meter == 0.001 * km


def test_length_conversions() -> None:
    assert (1 * Meter).in_unit(cm).unit is cm
    assert (1 * Meter).in_unit(cm).magnitude == 100

    assert (1 * Meter).in_unit(km).unit is km
    assert (1 * Meter).in_unit(km).magnitude == 0.001


def test_area_equivalence() -> None:
    assert 1 * Meter**2 == 10000 * cm**2
    assert 1 * Meter**2 == 0.000001 * km**2


def test_area_conversions() -> None:
    assert (1 * Meter**2).in_unit(cm**2).unit is cm ** 2
    assert (1 * Meter**2).in_unit(cm**2).magnitude == 10000

    assert (1 * Meter**2).in_unit(km**2).unit is km ** 2
    assert (1 * Meter**2).in_unit(km**2).magnitude == 0.000001


def test_volume_equivalence() -> None:
    assert 1 * Liter == 0.001 * Meter**3
    assert 1 * Liter == 1 * (Deci * Meter) ** 3
    assert 1 * Liter == 1000 * (Milli * Liter)


def test_volume_conversions() -> None:
    assert (1 * Liter).in_unit(Meter**3).unit == Meter**3
    assert (1 * Liter).in_unit(Meter**3).magnitude == 0.001

    assert (1 * Liter).in_unit((Deci * Meter) ** 3).unit == (Deci * Meter) ** 3
    assert (1 * Liter).in_unit((Deci * Meter) ** 3).magnitude == 1
