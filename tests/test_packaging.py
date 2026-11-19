import subprocess
import sys
from importlib import metadata

import measured


def test_package_version() -> None:
    assert measured.__version__ == metadata.version("measured")
    assert measured.__version__.count(".") >= 2


def test_imports_with_only_its_declared_dependencies() -> None:
    """measured declares no dependencies, so every module it ships must
    import where nothing else is installed.  A None entry in sys.modules
    makes Python raise ImportError for that name, which stands in for a
    package that is absent."""
    script = (
        "import sys; "
        "sys.modules['typing_extensions'] = None; "
        "import measured, measured.formatting, measured.conversions"
    )
    subprocess.run([sys.executable, "-c", script], check=True)
