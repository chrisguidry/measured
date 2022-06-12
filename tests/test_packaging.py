from importlib import metadata

import measured


def test_package_version() -> None:
    assert measured.__version__ == metadata.version("measured")
