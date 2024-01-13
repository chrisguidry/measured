from pytest_benchmark.fixture import BenchmarkFixture

from measured import One, Quantity
from measured.astronomical import JulianYear
from measured.si import Ampere, Meter, Ohm, Second, Volt
from measured.us import Ounce, Ton


def test_quantity_construction(benchmark: BenchmarkFixture) -> None:
    def quantity_construction() -> Quantity:
        return Quantity(1000001, Meter)

    result = benchmark(quantity_construction)

    assert result == Quantity(1000001, Meter)


def test_low_dimensional_equality(benchmark: BenchmarkFixture) -> None:
    a = Quantity(1000, Meter)
    b = Quantity(1000, Meter)

    def low_dimensional_equality() -> bool:
        return bool(a == b)

    assert benchmark(low_dimensional_equality) is True


def test_high_dimensional_equality(benchmark: BenchmarkFixture) -> None:
    a = Quantity(1000, Ohm)
    b = Quantity(1000, Ohm)

    def high_dimensional_equality() -> bool:
        return bool(a == b)

    assert benchmark(high_dimensional_equality) is True


def test_computing_resistances(benchmark: BenchmarkFixture) -> None:
    a = Quantity(1000, Ampere)
    v = Quantity(1000, Volt)

    def computing_resistances() -> Quantity:
        return v / a

    assert benchmark(computing_resistances) == Quantity(1, Ohm)


def test_complicated_conversions(benchmark: BenchmarkFixture) -> None:
    o = Quantity(1000, Ounce / (JulianYear * Ampere))
    t = Quantity(1000, Ton / (Second * Ampere))

    def divide() -> Quantity:
        return (t / o).in_unit(One)

    assert benchmark(divide).unit == One
