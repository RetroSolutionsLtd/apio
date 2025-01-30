# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2018 FPGAwars
# -- Author Jesús Arroyo
# -- License GPLv2
# -- Derived from:
# ---- Platformio project
# ---- (C) 2014-2016 Ivan Kravets <me@ikravets.com>
# ---- License Apache v2
"""A class that manages the console output of the apio process."""

from io import StringIO
from dataclasses import dataclass
from typing import Optional
from rich.console import Console
from rich.ansi import AnsiDecoder
from rich.theme import Theme
from rich.text import Text

# -- The names of the Rich library color names is available at:
# -- https://rich.readthedocs.io/en/stable/appendix/colors.html

DOCS_TITLE = "dark_red bold"
DOCS_EMPHASIZE = "deep_sky_blue4 bold"
HELP_SUBCOMMANDS = "dark_red bold"


# -- Redemanded table cell padding. 1 space on the left and 3 on the right.
PADDING = padding = (0, 3, 0, 1)

# -- Line width when rendering help and docs.
DOCS_WIDTH = 70


# -- This console state is initialized at the end of this file.
@dataclass
class ConsoleState:
    """Contains the state of the apio console."""

    color_system: Optional[str] = None
    force_terminal: bool = None
    console: Console = None
    decoder: AnsiDecoder = None


_state: ConsoleState = ConsoleState()


def configure(*, colors: bool = None, force_terminal: bool = None) -> None:
    """Turn the color support on or off."""
    # -- Update color system if specified.
    if colors is not None:
        _state.color_system = "auto" if colors else None

    # -- Update force terminal if specified.
    if force_terminal is not None:
        _state.force_terminal = True if force_terminal else None

    # -- Construct the new console. The highlighting colors are optimized
    # -- for 'apio docs'.
    _state.console = Console(
        color_system=_state.color_system,
        force_terminal=_state.force_terminal,
        theme=Theme(
            {
                "repr.str": DOCS_EMPHASIZE,
                "code": DOCS_EMPHASIZE,
                "repr.url": DOCS_EMPHASIZE,
                "repr.number": "",
            }
        ),
    )

    # -- Construct the helper decoder.
    _state.decoder = AnsiDecoder()


def console():
    """Returns the underlying console. This value should not be cached as
    the console object changes when the configure() or reset() are called."""
    return _state.console


def reset():
    """Reset to initial configuration."""
    configure(colors=True, force_terminal=False)


def cunstyle(text: str) -> str:
    """A replacement for click unstyle(). This function removes ansi colors
    from a string."""
    text_obj: Text = _state.decoder.decode_line(text)
    return text_obj.plain


def cout(
    *text_lines: str,
    style: Optional[str] = None,
    nl: bool = True,
) -> None:
    """Prints lines of text to the console, using the optional style."""

    # -- If no args, just do an empty println.
    if not text_lines:
        text_lines = [""]

    for text_line in text_lines:
        # -- User is responsible to conversion to strings.
        assert isinstance(text_line, str)

        # -- If colors are off, strip potential coloring in the text.
        # -- This may be coloring that we received from the scons process.
        if not _state.console.color_system:
            text_line = cunstyle(text_line)

        # -- Determine end of line
        end = "\n" if nl else ""

        # -- Write it out using the given style.
        _state.console.out(text_line, style=style, highlight=False, end=end)


def cerror(*text_lines: str) -> None:
    """Prints one or more text lines, adding to the first one the prefix
    'Error: ' and applying to all of them the red color."""
    # -- Output the first line.
    _state.console.out(f"Error: {text_lines[0]}", style="red", highlight=False)
    # -- Output the rest of the lines.
    for text_line in text_lines[1:]:
        _state.console.out(text_line, highlight=False, style="red")


def cwarning(*text_lines: str) -> None:
    """Prints one or more text lines, adding to the first one the prefix
    'Warning: ' and applying to all of them the yellow color."""
    # -- Emit first line.
    _state.console.out(
        f"Warning: {text_lines[0]}", style="yellow", highlight=False
    )
    # -- Emit the rest of the lines
    for text_line in text_lines[1:]:
        _state.console.out(text_line, highlight=False, style="yellow")


def cprint(
    markdown_text: str, *, style: Optional[str] = None, highlight: bool = False
) -> None:
    """Render the given markdown text. Applying optional style and if enabled,
    highlighting semantic elements such as strings if enabled."""
    _state.console.print(
        markdown_text,
        highlight=highlight,
        style=style,
    )


class ConsoleCapture:
    """A context manager to output into a string."""

    def __init__(self):
        self._saved_file = None
        self._buffer = None

    def __enter__(self):
        self._saved_file = _state.console.file
        self._buffer = StringIO()
        _state.console.file = self._buffer
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        _state.console.file = self._saved_file

    @property
    def value(self):
        """Returns the captured text."""
        return self._buffer.getvalue()


def cstyle(text: str, style: Optional[str] = None) -> str:
    """Render the text to a string using an optional style."""
    with ConsoleCapture() as capture:
        _state.console.out(text, style=style, highlight=False, end="")
        return capture.value


def docs_text(
    markdown_text: str, width: int = DOCS_WIDTH, end: str = "\n"
) -> None:
    """A wrapper around Console.print that is specialized for rendering
    help and docs."""
    _state.console.print(markdown_text, highlight=True, width=width, end=end)


def docs_rule(width: int = DOCS_WIDTH):
    """Print a docs horizontal separator."""
    cout("─" * width, style="dim")


def is_terminal():
    """Returns True if the console writes to a terminal (vs a pipe)."""
    return _state.console.is_terminal


def cwidth():
    """Return the console width."""
    return _state.console.width


# -- Initialize the module.
reset()
