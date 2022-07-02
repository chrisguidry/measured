"""
From the [SQLAlchemy documentation][1]:

    The requirements for the custom datatype class are that it have a constructor which
    accepts positional arguments corresponding to its column format, and also provides a
    method __composite_values__() which returns the state of the object as a list or
    tuple, in order of its column-based attributes. It also should supply adequate
    __eq__() and __ne__() methods which test the equality of two instances.

    [1]: https://docs.sqlalchemy.org/en/20/orm/composites.html
"""

from typing import Tuple

import pytest

from measured import Numeric, Quantity
from measured.si import Meter, Ohm, Second


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
