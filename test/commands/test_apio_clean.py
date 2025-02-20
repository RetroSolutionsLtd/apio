"""
  Test for the "apio clean" command
"""

from os.path import join
from pathlib import Path
from test.conftest import ApioRunner
from apio.commands.apio import cli as apio


def test_clean_without_apio_ini(apio_runner: ApioRunner):
    """Tests the apio clean command without an apio.ini file."""

    with apio_runner.in_sandbox() as sb:

        # -- Run "apio clean" with no apio.ini
        result = sb.invoke_apio_cmd(apio, "clean")
        assert result.exit_code != 0, result.output
        assert "Error: Missing project file apio.ini" in result.output


# R0801: Similar lines in 2 files
# pylint: disable=R0801
def test_clean_with_apio_ini(apio_runner: ApioRunner):
    """Tests the apio clean command with an apio.ini file."""

    with apio_runner.in_sandbox() as sb:

        # -- Run "apio clean" with a valid apio.ini and no dirty files.
        sb.write_default_apio_ini()
        result = sb.invoke_apio_cmd(apio, "clean")
        assert result.exit_code == 0, result.output

        # -- Run "apio clean" with apio.ini and dirty files.
        sb.write_default_apio_ini()
        sb.write_file(".sconsign.dblite", "dummy text")
        sb.write_file("_build/hardware.out", "dummy text")
        assert Path(".sconsign.dblite").exists()
        assert Path("_build/hardware.out").exists()
        assert Path("_build").exists()
        result = sb.invoke_apio_cmd(apio, "clean")
        assert result.exit_code == 0, result.output
        assert "Removed .sconsign.dblite" in result.output
        assert f"Removed {join('_build', 'hardware.out')}" in result.output
        assert "Removed directory _build" in result.output
        assert not Path(".sconsign.dblite").exists()
        assert not Path("_build/hardware.out").exists()
        assert not Path("_build").exists()
