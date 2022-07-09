import sys

if sys.version_info < (3, 9):  # pragma: no cover
    # math.gcd changed in Python 3.8 from a two-argument for to a variable argument form
    import math

    from typing_extensions import SupportsIndex

    def recursive_gcd(*integers: SupportsIndex) -> int:
        if len(integers) <= 2:
            return math.gcd(*integers)
        return math.gcd(integers[0], gcd(*integers[1:]))

    _gcd = recursive_gcd

else:  # pragma: no cover
    from math import gcd as _gcd

gcd = _gcd
