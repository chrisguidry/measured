import json
from typing import Generator, Optional

import pytest
from pydantic import BaseModel

import measured.json
from measured import Dimension, Length, Prefix, Quantity, Unit
from measured.si import Kilo, Meter


@pytest.fixture
def codecs_installed() -> Generator[None, None, None]:
    with measured.json.codecs_installed():
        yield


class ExampleModel(BaseModel):
    dimension: Dimension = Length
    optional_dimension: Optional[Dimension] = None

    prefix: Prefix = Kilo
    optional_prefix: Optional[Prefix] = None

    unit: Unit = Meter
    optional_unit: Optional[Unit] = None

    quantity: Quantity = 5 * Meter
    optional_quantity: Optional[Quantity] = None


def test_dimension_field() -> None:
    model = ExampleModel(dimension=Length)
    assert model.dimension == Length
    assert model.dimension is Length


def test_prefix_field() -> None:
    model = ExampleModel(prefix=Kilo)
    assert model.prefix == Kilo
    assert model.prefix is Kilo


def test_unit_field() -> None:
    model = ExampleModel(unit=Meter)
    assert model.unit == Meter
    assert model.unit is Meter


def test_quantity_field() -> None:
    model = ExampleModel(quantity=2 * Meter)
    assert model.quantity == 2 * Meter


def test_dimension_field_from_string() -> None:
    model = ExampleModel(dimension="length")
    assert model.dimension == Length
    assert model.dimension is Length


def test_prefix_field_from_string() -> None:
    model = ExampleModel(prefix="kilo")
    assert model.prefix == Kilo
    assert model.prefix is Kilo


def test_unit_field_from_string() -> None:
    model = ExampleModel(unit="meter")
    assert model.unit == Meter
    assert model.unit is Meter


def test_dimension_field_from_none() -> None:
    model = ExampleModel(optional_dimension=None)
    assert model.optional_prefix is None


def test_prefix_field_from_none() -> None:
    model = ExampleModel(optional_prefix=None)
    assert model.optional_prefix is None


def test_unit_field_from_none() -> None:
    model = ExampleModel(optional_unit=None)
    assert model.optional_unit is None


def test_quantity_field_from_none() -> None:
    model = ExampleModel(optional_quantity=None)
    assert model.optional_quantity is None


def test_dimension_field_from_incompatible() -> None:
    with pytest.raises(ValueError):
        ExampleModel(dimension=11)


def test_prefix_field_from_incompatible() -> None:
    with pytest.raises(ValueError):
        ExampleModel(prefix=11)


def test_unit_field_from_incompatible() -> None:
    with pytest.raises(ValueError):
        ExampleModel(unit=11)


def test_quantity_field_from_incompatible() -> None:
    with pytest.raises(ValueError):
        ExampleModel(quantity=11)


def test_dimension_field_from_string_must_exist() -> None:
    with pytest.raises(ValueError, match="'flibbity' is not a named Dimension"):
        ExampleModel(dimension="flibbity")


def test_dimension_field_from_string_must_be_named() -> None:
    with pytest.raises(ValueError, match="'area' is not a named Dimension"):
        ExampleModel(dimension="area")


def test_prefix_field_from_string_must_exist() -> None:
    with pytest.raises(ValueError, match="'kibbity' is not a named Prefix"):
        ExampleModel(prefix="kibbity")


def test_unit_field_from_string_must_exist() -> None:
    with pytest.raises(ValueError, match="'kibbity' is not a named Unit"):
        ExampleModel(unit="kibbity")


@pytest.fixture
def instance() -> ExampleModel:
    return ExampleModel()


def test_to_dict(instance: ExampleModel) -> None:
    assert instance.dict() == {
        "dimension": Length,
        "optional_dimension": None,
        "prefix": Kilo,
        "optional_prefix": None,
        "unit": Meter,
        "optional_unit": None,
        "quantity": 5 * Meter,
        "optional_quantity": None,
    }


def test_to_json_without_codecs_installed(instance: ExampleModel) -> None:
    with pytest.raises(TypeError, match="is not JSON serializable"):
        assert instance.json()


def test_to_json(codecs_installed: None, instance: ExampleModel) -> None:
    assert json.loads(instance.json(), cls=json.JSONDecoder) == {
        "dimension": {
            "__measured__": "Dimension",
            "name": "length",
            "symbol": "L",
            "exponents": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        },
        "optional_dimension": None,
        "prefix": {
            "__measured__": "Prefix",
            "name": "kilo",
            "symbol": "k",
            "base": 10,
            "exponent": 3,
        },
        "optional_prefix": None,
        "unit": {
            "__measured__": "Unit",
            "name": "meter",
            "symbol": "m",
            "prefix": None,
            "factors": None,
            "dimension": {
                "__measured__": "Dimension",
                "name": "length",
                "symbol": "L",
                "exponents": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            },
        },
        "optional_unit": None,
        "quantity": {
            "__measured__": "Quantity",
            "magnitude": 5,
            "unit": {
                "__measured__": "Unit",
                "name": "meter",
                "symbol": "m",
                "prefix": None,
                "factors": None,
                "dimension": {
                    "__measured__": "Dimension",
                    "name": "length",
                    "symbol": "L",
                    "exponents": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                },
            },
        },
        "optional_quantity": None,
    }
