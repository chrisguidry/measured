from importlib import metadata

import measured


def test_package_version():
    assert measured.__version__ == metadata.version("measured")
