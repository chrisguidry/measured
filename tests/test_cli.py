import subprocess


def run(command: str) -> str:
    return subprocess.check_output(command, shell=True, encoding="utf-8")


def test_can_run_as_module() -> None:
    output = run("python -m measured 5m")
    assert "Magnitude: 5" in output
    assert "Unit: meter" in output


def test_can_run_as_script() -> None:
    output = run("measured 5m")
    assert "Magnitude: 5" in output
    assert "Unit: meter" in output
