import json
from decimal import Decimal
from typing import AsyncGenerator, Generator, List, Optional

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel

import measured.json
from measured import Dimension, Length, Prefix, Quantity, Unit
from measured.si import Kilo, Meter


def test_dimension_json_roundtrips_without_codecs() -> None:
    with pytest.raises(TypeError, match="not JSON serializable"):
        json.loads(json.dumps(Length))


def test_prefix_json_roundtrips_without_codecs() -> None:
    with pytest.raises(TypeError, match="not JSON serializable"):
        json.loads(json.dumps(Kilo))


def test_unit_json_roundtrips_without_codecs() -> None:
    with pytest.raises(TypeError, match="not JSON serializable"):
        json.loads(json.dumps(Meter))


def test_quantity_json_roundtrips_without_codecs() -> None:
    with pytest.raises(TypeError, match="not JSON serializable"):
        json.loads(json.dumps(5 * Kilo * Meter))


@pytest.fixture
def codecs_installed() -> Generator[None, None, None]:
    with measured.json.codecs_installed():
        yield


def test_dimension_json_roundtrips(codecs_installed: None) -> None:
    assert json.loads(json.dumps(Length)) == Length


def test_prefix_json_roundtrips(codecs_installed: None) -> None:
    assert json.loads(json.dumps(Kilo)) == Kilo


def test_unit_json_roundtrips(codecs_installed: None) -> None:
    assert json.loads(json.dumps(Meter)) == Meter


def test_quantity_json_roundtrips(codecs_installed: None) -> None:
    assert json.loads(json.dumps(5 * Kilo * Meter)) == 5 * Kilo * Meter


class ExampleModel(BaseModel):
    dimension: Dimension = Length
    optional_dimension: Optional[Dimension] = None

    prefix: Prefix = Kilo
    optional_prefix: Optional[Prefix] = None

    unit: Unit = Meter
    optional_unit: Optional[Unit] = None

    quantity: Quantity = 5 * Meter
    optional_quantity: Optional[Quantity] = None


class ParentModel(BaseModel):
    one_example: ExampleModel

    some_examples: List[ExampleModel]


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
    model = ExampleModel(dimension="length")  # type: ignore[arg-type]
    assert model.dimension == Length
    assert model.dimension is Length


def test_prefix_field_from_string() -> None:
    model = ExampleModel(prefix="kilo")  # type: ignore[arg-type]
    assert model.prefix == Kilo
    assert model.prefix is Kilo


def test_unit_field_from_string() -> None:
    model = ExampleModel(unit="meter")  # type: ignore[arg-type]
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
        ExampleModel(dimension=11)  # type: ignore[arg-type]


def test_prefix_field_from_incompatible() -> None:
    with pytest.raises(ValueError):
        ExampleModel(prefix=11)  # type: ignore[arg-type]


def test_unit_field_from_incompatible() -> None:
    with pytest.raises(ValueError):
        ExampleModel(unit=11)  # type: ignore[arg-type]


def test_quantity_field_from_incompatible() -> None:
    with pytest.raises(ValueError):
        ExampleModel(quantity=11)  # type: ignore[arg-type]


def test_dimension_field_from_string_must_exist() -> None:
    with pytest.raises(ValueError, match="'flibbity' is not a named Dimension"):
        ExampleModel(dimension="flibbity")  # type: ignore[arg-type]


def test_prefix_field_from_string_must_exist() -> None:
    with pytest.raises(ValueError, match="'kibbity' is not a named Prefix"):
        ExampleModel(prefix="kibbity")  # type: ignore[arg-type]


def test_unit_field_from_string_must_exist() -> None:
    with pytest.raises(ValueError, match="'kibbity' is not a named Unit"):
        ExampleModel(unit="kibbity")  # type: ignore[arg-type]


@pytest.fixture
def example() -> ExampleModel:
    return ExampleModel()


@pytest.fixture
def parent() -> ParentModel:
    return ParentModel(
        one_example=ExampleModel(),
        some_examples=[ExampleModel(), ExampleModel()],
    )


def test_to_dict(example: ExampleModel) -> None:
    assert example.model_dump() == {
        "dimension": Length,
        "optional_dimension": None,
        "prefix": Kilo,
        "optional_prefix": None,
        "unit": Meter,
        "optional_unit": None,
        "quantity": 5 * Meter,
        "optional_quantity": None,
    }


def test_to_json(codecs_installed: None, example: ExampleModel) -> None:
    as_json = example.model_dump_json()
    assert json.loads(as_json, cls=json.JSONDecoder, object_hook=None) == {
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
            "unit": "m",
        },
        "optional_quantity": None,
    }


def test_example_dict_roundtrip(example: ExampleModel) -> None:
    assert ExampleModel.model_validate(example.model_dump()) == example


def test_parent_dict_roundtrip(parent: ParentModel) -> None:
    assert ParentModel.model_validate(parent.model_dump()) == parent


def test_example_json_roundtrip(codecs_installed: None, example: ExampleModel) -> None:
    assert ExampleModel.model_validate_json(example.model_dump_json()) == example


def test_parent_json_roundtrip(codecs_installed: None, parent: ParentModel) -> None:
    assert ParentModel.model_validate_json(parent.model_dump_json()) == parent


def test_decimal_json_roundtrip(codecs_installed: None, example: ExampleModel) -> None:
    example.quantity = Decimal("1.2345") * Meter
    assert ExampleModel.model_validate_json(example.model_dump_json()) == example


@pytest.fixture
def api(codecs_installed: None) -> FastAPI:
    app = FastAPI()

    @app.post("/example")  # type: ignore[misc]
    def echo_example(example: ExampleModel) -> ExampleModel:
        return example

    @app.post("/parent")  # type: ignore[misc]
    def echo_parent(parent: ParentModel) -> ParentModel:
        return parent

    return app


@pytest.fixture
async def client(api: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=api)  # type: ignore[arg-type]
    async with AsyncClient(base_url="http://measured", transport=transport) as client:
        yield client


async def test_example_api_roundtrip(
    client: AsyncClient, example: ExampleModel
) -> None:
    response = await client.post("/example", content=example.model_dump_json())
    assert response.status_code == 200
    assert ExampleModel.model_validate_json(response.text) == example


async def test_parent_api_roundtrip(client: AsyncClient, parent: ParentModel) -> None:
    response = await client.post("/parent", content=parent.model_dump_json())
    assert response.status_code == 200
    assert ParentModel.model_validate_json(response.text) == parent


def test_codec_installation_is_nestable() -> None:
    with pytest.raises(TypeError, match="not JSON serializable"):
        json.dumps(Length)

    with measured.json.codecs_installed():
        assert json.loads(json.dumps(Length)) is Length
        with measured.json.codecs_installed():
            assert json.loads(json.dumps(Length)) is Length
            with measured.json.codecs_installed():
                assert json.loads(json.dumps(Length)) is Length
            assert json.loads(json.dumps(Length)) is Length
        assert json.loads(json.dumps(Length)) is Length

    with pytest.raises(TypeError, match="not JSON serializable"):
        json.dumps(Length)


def test_decimal_quantity_roundtrips(codecs_installed: None) -> None:
    quantity = Decimal("1.23456") * Meter
    assert json.loads(json.dumps(quantity)) == Decimal("1.23456") * Meter
