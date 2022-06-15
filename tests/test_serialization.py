import json
import pickle
from copy import copy
from types import ModuleType
from typing import Generator, List, Union

try:
    import cloudpickle
except ImportError:  # pragma: no cover
    cloudpickle = None

import pytest

import measured.json
from measured import Area, Dimension, Length, Prefix, Quantity, Resistance, Unit
from measured.json import MeasuredJSONDecoder, MeasuredJSONEncoder, install, uninstall
from measured.si import Giga, Hertz, Kilo, Meter, Milli, Ohm


@pytest.fixture
def codecs_installed() -> Generator[None, None, None]:
    with measured.json.codecs_installed():
        yield


NamedType = Union[Dimension, Prefix, Unit]
MeasuredType = Union[NamedType, Quantity]

DIMENSIONS: List[NamedType] = [Length, Area, Resistance]
PREFIXES: List[NamedType] = [Kilo, Milli, Kilo * Giga]
UNITS: List[NamedType] = [Meter, Kilo * Meter, Hertz, Ohm]
NAMED = DIMENSIONS + PREFIXES + UNITS

QUANTITIES: List[MeasuredType] = [5 * Meter, 5 * Hertz, 5.1 * Ohm]

SERIALIZERS = [json, pickle] + ([cloudpickle] if cloudpickle else [])


@pytest.mark.parametrize("named", NAMED, ids=[d.name for d in NAMED])
def test_named_type_copies_are_singletons(named: NamedType) -> None:
    assert copy(named) is named


@pytest.mark.parametrize("quantity", QUANTITIES, ids=map(str, QUANTITIES))
def test_quantiy_copies_are_new(quantity: NamedType) -> None:
    assert copy(quantity) == quantity
    assert copy(quantity) is not quantity


@pytest.mark.parametrize("serializer", SERIALIZERS)
@pytest.mark.parametrize("named", NAMED, ids=[d.name for d in NAMED])
def test_named_type_serializer_roundtrip(
    codecs_installed: None,
    serializer: ModuleType,
    named: NamedType,
) -> None:
    prior_name = named.name
    prior_symbol = named.symbol

    roundtripped: NamedType = serializer.loads(serializer.dumps(named))

    assert roundtripped == named
    assert roundtripped is named
    assert roundtripped.name == prior_name
    assert roundtripped.symbol == prior_symbol


@pytest.mark.parametrize("serializer", SERIALIZERS)
@pytest.mark.parametrize("quantity", QUANTITIES, ids=map(str, QUANTITIES))
def test_quantity_serializer_roundtrip(
    codecs_installed: None,
    serializer: ModuleType,
    quantity: Quantity,
) -> None:
    roundtripped: Quantity = serializer.loads(serializer.dumps(quantity))

    assert roundtripped == quantity
    assert roundtripped is not quantity


@pytest.mark.parametrize("named", NAMED, ids=[d.name for d in NAMED])
def test_named_type_explicit_json_roundtrip(named: NamedType) -> None:
    prior_name = named.name
    prior_symbol = named.symbol

    roundtripped: NamedType = json.loads(
        json.dumps(named, cls=MeasuredJSONEncoder),
        cls=MeasuredJSONDecoder,
    )

    assert roundtripped == named
    assert roundtripped is named
    assert roundtripped.name == prior_name
    assert roundtripped.symbol == prior_symbol


INSTANCES = [Length, Kilo, Meter, 5 * Meter]
INSTANCE_IDS = [str(i) for i in INSTANCES]


@pytest.mark.parametrize("obj", INSTANCES, ids=INSTANCE_IDS)
def test_not_naturally_json_serializable(obj: MeasuredType) -> None:
    with pytest.raises(TypeError, match="is not JSON serializable"):
        json.dumps(obj)


@pytest.mark.parametrize("obj", INSTANCES, ids=INSTANCE_IDS)
def test_json_temporarily_installed(obj: MeasuredType) -> None:
    with pytest.raises(TypeError, match="is not JSON serializable"):
        json.dumps(obj)

    with measured.json.codecs_installed():
        assert json.loads(json.dumps(obj)) == obj

    with pytest.raises(TypeError, match="is not JSON serializable"):
        json.dumps(obj)


@pytest.mark.parametrize("obj", INSTANCES, ids=INSTANCE_IDS)
def test_json_installation(obj: MeasuredType) -> None:
    with pytest.raises(TypeError, match="is not JSON serializable"):
        json.dumps(obj)

    try:
        install()
        assert json.loads(json.dumps(obj)) == obj
    finally:
        uninstall()

    with pytest.raises(TypeError, match="is not JSON serializable"):
        json.dumps(obj)


def test_still_raises_on_unrecognized_types() -> None:
    with pytest.raises(TypeError, match="not JSON serializable"):
        json.dumps(object(), cls=MeasuredJSONEncoder)


def test_ignores_unknown_measured_types(codecs_installed: None) -> None:
    unknown = {"__measured__": "wat", "no": "idea"}
    assert json.loads(json.dumps(unknown)) == unknown
