import re
import subprocess


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


def test_can_print_conversions() -> None:
    output = run("measured 1 foot")
    assert "Magnitude: 1" in output
    assert "Unit: foot" in output
    assert re.findall(r"12\.0\s+inch", output)
    assert re.findall(r"0\.3048\s+meter", output)


def test_can_handle_no_conversions() -> None:
    output = run("measured 1 hertz")
    assert "Magnitude: 1" in output
    assert "Unit: hertz" in output
