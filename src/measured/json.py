import json
from contextlib import contextmanager
from json import JSONDecoder, JSONEncoder
from typing import Any, Callable, Dict, Generator, Optional, Union, cast

from . import Dimension, Prefix, Quantity, Unit

MeasuredType = Union[Dimension, Prefix, Quantity, Unit]


class MeasuredJSONEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        json_method = getattr(o, "__json__", None)
        if callable(json_method):
            return json_method()
        return super().default(o)


class MeasuredJSONDecoder(JSONDecoder):
    def __init__(
        self,
        *,
        parse_float: Optional[Callable[[str], Any]] = None,
        parse_int: Optional[Callable[[str], Any]] = None,
        parse_constant: Optional[Callable[[str], Any]] = None,
        strict: bool = True,
    ) -> None:
        super().__init__(
            object_hook=self.object_hook,
            object_pairs_hook=None,
            parse_float=parse_float,
            parse_int=parse_int,
            parse_constant=parse_constant,
            strict=strict,
        )

    def object_hook(self, o: Dict[str, Any]) -> Union[MeasuredType, Dict[str, Any]]:
        type_name = o.get("__measured__")

        if type_name == "Dimension":
            return Dimension.__from_json__(o)
        elif type_name == "Prefix":
            return Prefix.__from_json__(o)
        elif type_name == "Unit":
            return Unit.__from_json__(o)
        elif type_name == "Quantity":
            return Quantity.__from_json__(o)

        return o


@contextmanager
def codecs_installed() -> Generator[None, None, None]:
    """A context within which the standard library's `json` module will be aware of
    how to encode and decode `measured` objects."""
    if isinstance(json._default_encoder, MeasuredJSONEncoder):  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType] typeshed omits json's module-level codecs
        yield
        return

    original_encoder = json._default_encoder  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownVariableType] typeshed omits json's module-level codecs
    original_decoder = json._default_decoder  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownVariableType] typeshed omits json's module-level codecs
    original_object_hook = cast(Dict[str, Any], json.loads.__kwdefaults__)[
        "object_hook"
    ]

    encoder = MeasuredJSONEncoder()
    decoder = MeasuredJSONDecoder()

    json._default_encoder = encoder  # pyright: ignore[reportAttributeAccessIssue] typeshed omits json's module-level codecs
    json._default_decoder = decoder  # pyright: ignore[reportAttributeAccessIssue] typeshed omits json's module-level codecs
    cast(Dict[str, Any], json.loads.__kwdefaults__)["object_hook"] = decoder.object_hook

    try:
        from pydantic.json import ENCODERS_BY_TYPE as pydantic_encoders
    except ImportError:  # pragma: no cover
        pydantic_encoders = {}

    pydantic_encoders[Dimension] = encoder
    pydantic_encoders[Prefix] = encoder
    pydantic_encoders[Unit] = encoder
    pydantic_encoders[Quantity] = encoder

    try:
        yield
    finally:
        json._default_encoder = original_encoder  # pyright: ignore[reportAttributeAccessIssue] typeshed omits json's module-level codecs
        json._default_decoder = original_decoder  # pyright: ignore[reportAttributeAccessIssue] typeshed omits json's module-level codecs
        cast(Dict[str, Any], json.loads.__kwdefaults__)["object_hook"] = (
            original_object_hook
        )

        del pydantic_encoders[Dimension]
        del pydantic_encoders[Prefix]
        del pydantic_encoders[Unit]
        del pydantic_encoders[Quantity]


_installer = codecs_installed()


def install() -> None:
    """Installs the `measured` library's JSON encoder and decoder as the default"""
    _installer.__enter__()


def uninstall() -> None:
    """Uninstalls the `measured` library's JSON encoder and decoder from the default"""
    global _installer
    _installer.__exit__(None, None, None)
    _installer = codecs_installed()
