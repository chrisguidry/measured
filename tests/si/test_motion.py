from measured import Acceleration, Crackle, Jerk, Length, Pop, Snap, Speed
from measured.si import Meter, Second

# https://en.wikipedia.org/wiki/Fourth,_fifth,_and_sixth_derivatives_of_position


def test_derivatives_of_position() -> None:
    length = 128 * Meter
    assert length.unit.dimension is Length

    speed = length / (2 * Second)
    assert speed.unit.dimension is Speed
    assert speed == 64 * Meter / Second

    acceleration = speed / (2 * Second)
    assert acceleration.unit.dimension is Acceleration
    assert acceleration == 32 * Meter / Second**2

    jerk = acceleration / (2 * Second)
    assert jerk.unit.dimension is Jerk
    assert jerk == 16 * Meter / Second**3

    snap = jerk / (2 * Second)
    assert snap.unit.dimension is Snap
    assert snap == 8 * Meter / Second**4

    crackle = snap / (2 * Second)
    assert crackle.unit.dimension is Crackle
    assert crackle == 4 * Meter / Second**5

    pop = crackle / (2 * Second)
    assert pop.unit.dimension is Pop
    assert pop == 2 * Meter / Second**6
