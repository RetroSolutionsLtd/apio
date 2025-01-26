"""
  Test for the "apio preferences" command
"""

from test.conftest import ApioRunner
from click import unstyle
from apio.commands.apio import cli as apio


def test_colors_on_off(apio_runner: ApioRunner):
    """Test "apio preferences" with different parameters"""

    with apio_runner.in_sandbox() as sb:

        # -- Execute "apio preferences set --colors on"
        result = sb.invoke_apio_cmd(
            apio, ["preferences", "set", "--colors", "on"]
        )
        sb.assert_ok(result)
        assert "Colors set to [on]" in result.output
        assert result.output != unstyle(result.output)  # Colored.

        # -- Execute "apio preferences list". It should reports colors on,
        # -- in colors.
        result = sb.invoke_apio_cmd(apio, ["preferences", "list"])
        sb.assert_ok(result)
        assert result.output != unstyle(result.output)  # Colored.

        # -- Execute "apio system info". It should emit colors.
        result = sb.invoke_apio_cmd(apio, ["system", "info"])
        sb.assert_ok(result)
        assert result.output != unstyle(result.output)  # Colored.

        # -- Execute "apio preferences set --colors off"
        result = sb.invoke_apio_cmd(
            apio, ["preferences", "set", "--colors", "off"]
        )
        sb.assert_ok(result)
        assert "Colors set to [off]" in result.output

        # -- Execute "apio preferences list". It should reports colors off,
        # -- without colors.
        result = sb.invoke_apio_cmd(apio, ["preferences", "list"])
        sb.assert_ok(result)
        assert "\nColors:   off\n" in result.output
        assert result.output == unstyle(result.output)  # Non colored..

        # -- Execute "apio system info". It should not emit colors.
        result = sb.invoke_apio_cmd(apio, ["system", "info"])
        sb.assert_ok(result)
        assert result.output == unstyle(result.output)
