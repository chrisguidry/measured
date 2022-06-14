import json
from contextlib import contextmanager
from json import JSONDecoder, JSONEncoder
from typing import Any, Callable, Dict, Generator, Optional, Union

from . import Dimension, Prefix, Quantity, Unit

MeasuredType = Union[Dimension, Prefix, Quantity, Unit]


class MeasuredJSONEncoder(JSONEncoder):
    def __call__(self, o: Any) -> Any:
        return self.default(o)

    def default(self, o: Any) -> Any:
        json_method = getattr(o, "__json__", None)
        if callable(json_method):
            return {"__measured__": o.__class__.__name__, **json_method()}
        return super().default(o)


class MeasuredJSONDecoder(JSONDecoder):
    def __init__(
        self,
        *,
        parse_float: Optional[Callable[[str], Any]] = None,
        parse_int: Optional[Callable[[str], Any]] = None,
        parse_constant: Optional[Callable[[str], Any]] = None,
        strict: bool = True
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
            return Dimension.from_json(o)
        elif type_name == "Prefix":
            return Prefix.from_json(o)
        elif type_name == "Unit":
            return Unit.from_json(o)

        return o


@contextmanager
def codecs_installed() -> Generator[None, None, None]:
    """A context within which the standard library's `json` module will be aware of
    how to encode and decode `measured` objects."""
    original_encoder = json._default_encoder  # type: ignore
    original_decoder = json._default_decoder  # type: ignore
    json._default_encoder = MeasuredJSONEncoder()  # type: ignore
    json._default_decoder = MeasuredJSONDecoder()  # type: ignore

    try:
        from pydantic.json import ENCODERS_BY_TYPE as PYDANTIC_ENCODERS_BY_TYPE
    except ImportError:  # pragma: no cover
        PYDANTIC_ENCODERS_BY_TYPE = {}

    PYDANTIC_ENCODERS_BY_TYPE[Dimension] = MeasuredJSONEncoder()
    PYDANTIC_ENCODERS_BY_TYPE[Prefix] = MeasuredJSONEncoder()
    PYDANTIC_ENCODERS_BY_TYPE[Unit] = MeasuredJSONEncoder()
    PYDANTIC_ENCODERS_BY_TYPE[Quantity] = MeasuredJSONEncoder()

    try:
        yield
    finally:
        json._default_encoder = original_encoder  # type: ignore
        json._default_decoder = original_decoder  # type: ignore

        del PYDANTIC_ENCODERS_BY_TYPE[Dimension]
        del PYDANTIC_ENCODERS_BY_TYPE[Prefix]
        del PYDANTIC_ENCODERS_BY_TYPE[Unit]
        del PYDANTIC_ENCODERS_BY_TYPE[Quantity]


_installer = codecs_installed()


def install() -> None:
    """Installs the `measured` library's JSON encoder and decoder as the default"""
    _installer.__enter__()


def uninstall() -> None:
    """Uninstalls the `measured` library's JSON encoder and decoder from the default"""
    global _installer
    _installer.__exit__(None, None, None)
    _installer = codecs_installed()
