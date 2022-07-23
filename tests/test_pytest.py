import pytest

from measured.pytest import MeasuredPlugin
from measured.si import Meter, Second


@pytest.fixture
def plugin() -> MeasuredPlugin:
    return MeasuredPlugin()


def test_explaining_assertions(plugin: MeasuredPlugin) -> None:
    explanation = plugin.pytest_assertrepr_compare(
        op="==",
        left=1 * Meter,
        right=1 * Second,
    )
    assert isinstance(explanation, list)
    assert all(isinstance(line, str) for line in explanation)


def test_only_explains_measured_things(plugin: MeasuredPlugin) -> None:
    explanation = plugin.pytest_assertrepr_compare(op="==", left=1, right=2)
    assert explanation is None
