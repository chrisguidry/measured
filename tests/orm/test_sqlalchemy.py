"""
From the [SQLAlchemy documentation][1]:

    The requirements for the custom datatype class are that it have a constructor which
    accepts positional arguments corresponding to its column format, and also provides a
    method __composite_values__() which returns the state of the object as a list or
    tuple, in order of its column-based attributes. It also should supply adequate
    __eq__() and __ne__() methods which test the equality of two instances.

    [1]: https://docs.sqlalchemy.org/en/20/orm/composites.html
"""
import pytest

pytest.importorskip("sqlalchemy")

# flake8: noqa: E402 (imports not at top of file)

from typing import Generator, Tuple

from sqlalchemy import Column, Float, Integer, String, create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, composite, declarative_base

from measured import Numeric, Quantity
from measured.si import Kelvin, Meter, Ohm, Second
from measured.us import Fahrenheit, Inch


@pytest.mark.parametrize(
    "quantity, values",
    [
        (5 * Meter, (5, "m")),
        (5.0 * Meter, (5.0, "m")),
        (5.0 * Ohm, (5.0, "Ω")),
        (5.0 * Meter / Second, (5.0, "m⋅s⁻¹")),
        (5.0 * Meter**2 / Second, (5.0, "m²⋅s⁻¹")),
    ],
)
def test_quantity_composite_values_roundtrip(
    quantity: Quantity, values: Tuple[Numeric, str]
) -> None:
    assert quantity.__composite_values__() == values
    assert Quantity(*quantity.__composite_values__()) == quantity


Base = declarative_base()


class Measurement(Base):  # type: ignore
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True)

    temperature_magnitude = Column(Integer)
    temperature_unit = Column(String)
    temperature = composite(Quantity, temperature_magnitude, temperature_unit)

    area_magnitude = Column(Float)
    area_unit = Column(String)
    area = composite(Quantity, area_magnitude, area_unit)


@pytest.fixture
def engine() -> Generator[Engine, None, None]:
    engine = create_engine("sqlite://", future=True)
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def test_saving_and_reading_quantities(session: Session) -> None:
    first = Measurement(id=1, temperature=110 * Kelvin, area=10.5 * Meter**2)
    second = Measurement(id=2, temperature=350 * Fahrenheit, area=22.47 * Inch**2)
    session.add_all([first, second])
    session.flush()

    saved = set(session.query(Measurement))

    assert saved == {first, second}
    assert {m.temperature for m in saved} == {110 * Kelvin, 350 * Fahrenheit}
    assert {m.area for m in saved} == {10.5 * Meter**2, 22.47 * Inch**2}


def test_querying_for_quantities_exactly(session: Session) -> None:
    first = Measurement(id=1, temperature=110 * Kelvin, area=10.5 * Meter**2)
    second = Measurement(id=2, temperature=350 * Fahrenheit, area=22.47 * Inch**2)
    session.add_all([first, second])
    session.flush()

    found = set(
        session.query(Measurement).filter(Measurement.temperature == 110 * Kelvin)
    )

    assert found == {first}
