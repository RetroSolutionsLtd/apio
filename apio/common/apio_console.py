# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2018 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2
# -- Derived from:
# ---- Platformio project
# ---- (C) 2014-2016 Ivan Kravets <me@ikravets.com>
# ---- Licence Apache v2
"""A class that manages the console output of the apio process."""

from io import StringIO
from typing import Optional
from rich.console import Console
from rich.ansi import AnsiDecoder
from rich.text import Text

# Suppress earning about access to the global variables.
# pylint: disable=global-statement


# This console state is initialized at the end of this file.
_color_system: Optional[str] = None
_force_terminal: bool = None
_console: Console = None
_decoder: AnsiDecoder = None


def configure(*, colors: bool = None, force_terminal: bool = None) -> None:
    """Turn the color support on or off."""
    global _console, _decoder, _color_system, _force_terminal
    # -- Update color system if specified.
    if colors is not None:
        _color_system = "auto" if colors else None

    # -- Update force terminal if specified.
    if force_terminal is not None:
        _force_terminal = True if force_terminal else None

    # -- Construct the new console.
    _console = Console(
        color_system=_color_system,
        force_terminal=_force_terminal,
    )

    # -- Construct the helper decoder.
    _decoder = AnsiDecoder()


def reset():
    """Reset to initial configuration."""
    configure(colors=True, force_terminal=False)


def cunstyle(text: str) -> str:
    """A replacement for click unstype(). This function removes ansi colors
    from a string."""
    text_obj: Text = _decoder.decode_line(text)
    return text_obj.plain


def cout(
    *text_lines: str,
    style: Optional[str] = None,
    nl: bool = True,
) -> None:
    """Prints lines of text to the console, using the optional style."""

    for text_line in text_lines:
        # -- User is reponsible to conversion to strings.
        assert isinstance(text_line, str)

        # -- If colors are off, strip potential coloring in the text.
        # -- This may be coloring that we recieved from the scons process.
        if not _console.color_system:
            text_line = cunstyle(text_line)

        # -- Determine end of line
        end = "\n" if nl else ""

        # -- Write it out using the given style.
        _console.out(text_line, style=style, highlight=False, end=end)


def cerror(*text_lines: str) -> None:
    """Prints one or more text lines, adding to the first one the prefix
    'Error: ' and aplying to all of them the red color."""
    # -- Output the first line.
    _console.out(f"Error: {text_lines[0]}", style="red", highlight=False)
    # -- Output the rest of the lines.
    for text_line in text_lines[1:]:
        _console.out(text_line, highlight=False, style="red")


def cwarning(*text_lines: str) -> None:
    """Prints one or more text lines, adding to the first one the prefix
    'Warning: ' and aplying to all of them the yellow color."""
    # -- Emit first line.
    _console.out(f"Warning: {text_lines[0]}", style="yellow", highlight=False)
    # -- Emit the rest of the lines
    for text_line in text_lines[1:]:
        _console.out(text_line, highlight=False, style="yellow")


def cprint(
    markdown_text: str, *, style: Optional[str] = None, highlight: bool = False
) -> None:
    """Render the given markdown text. Applying optional style and if enabled,
    highlighting semantic elements such as strings if enabled."""
    _console.print(
        markdown_text,
        highlight=highlight,
        style=style,
    )


def cstyle(text: str, style: Optional[str] = None) -> str:
    """Render the text to a string using an optional style."""
    # -- Save the old output.
    file_save = _console.file
    # -- Set output to a buffer.
    _console.file = StringIO()
    # -- Output to buffer.
    _console.out(text, style=style, highlight=False, end="")
    # -- Get captured string.
    result = _console.file.getvalue()
    # -- Restore old output.
    _console.file = file_save
    # -- Return the capture value.
    return result


def is_terminal():
    """Returns True if the console writes to a terminal (vs a pipe)."""
    return _console.is_terminal


def width():
    """Return the console width."""
    return _console.width


# -- Initialize the module.
reset()
