import re
import subprocess
from subprocess import CalledProcessError

import pytest


def run(command: str) -> str:
    return subprocess.check_output(command, shell=True, encoding="utf-8")


def test_can_run_as_module() -> None:
    output = run("python -m measured 5 m")
    assert "Magnitude: 5" in output
    assert "Unit: meter" in output


def test_can_run_as_script() -> None:
    output = run("measured 5 m")
    assert "Magnitude: 5" in output
    assert "Unit: meter" in output


def test_prints_help_with_no_arguments() -> None:
    output = run("measured")
    assert "usage: measured [-h]" in output
    assert "positional arguments:" in output


def test_can_list_units() -> None:
    output = run("measured --list")
    assert "m (meter, length)" in output
    assert "in. (inch, length)" in output


def test_can_print_conversions() -> None:
    output = run("measured 1 foot")
    assert "Magnitude: 1" in output
    assert "Unit: foot" in output
    assert re.findall(r"12\.0\s+inch", output)
    assert re.findall(r"0\.3048\s+meter", output)


def test_can_handle_no_conversions() -> None:
    output = run("measured 1 steradian")
    assert "Magnitude: 1" in output
    assert "Unit: steradian" in output


def test_handles_parse_errors_gracefully() -> None:
    with pytest.raises(CalledProcessError) as excinfo:
        run("measured flibbidy gibbidy")

    assert excinfo.value.returncode == 1
    assert "Error parsing quantity" in excinfo.value.stdout
