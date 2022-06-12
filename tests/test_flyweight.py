from measured import Dimension, Prefix, Unit


def test_classes_do_not_share_known_cache():
    known_dimensions = set(Dimension.known())
    known_prefixes = set(Prefix.known())
    known_units = set(Unit.known())

    assert known_dimensions.isdisjoint(known_prefixes)
    assert known_units.isdisjoint(known_prefixes)
    assert known_units.isdisjoint(known_dimensions)
