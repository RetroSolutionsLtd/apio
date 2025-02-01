# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- License GPLv2
"""Implementation of 'apio docs options'."""

import sys
import click
from apio.managers import project
from apio.apio_context import ApioContext, ApioContextScope
from apio.utils import cmd_util
from apio.common.styles import TITLE
from apio.common.styles import INFO
from apio.common.apio_console import (
    docs_text,
    docs_rule,
    cout,
    cerror,
    cstyle,
)


# -- apio docs options

# -- Text in the markdown format of the python rich library.
APIO_DOCS_OPTIONS_HELP = """
The command 'apio docs options' provides information about the required \
project file 'apio.ini'.

Examples:[code]
  apio docs options              # List an overview and all options.
  apio docs options top-module   # List a single option.[/code]
"""

# -- Text in the markdown format of the python rich library.
APIO_INI_DOC = """
Every Apio project is required to have an 'apio.ini' project configuration \
file. These are properties text files with '#' comments and a single section \
called '\\[env]' that contains the required and optional options for this \
project.

Example:[code]
  \\[env]
  board = alhambra-ii   # Board id
  top-module = my_main  # Top module name[/code]

Following is a list of the apio.ini options and their descriptions.
"""


@click.command(
    name="options",
    cls=cmd_util.ApioCommand,
    short_help="Apio.ini options documentation.",
    help=APIO_DOCS_OPTIONS_HELP,
)
@click.argument("option", nargs=1, required=False)
def cli(
    # Argument
    option: str,
):
    """Implements the 'apio docs options' command."""

    # -- Create the apio context. We don't really need it here but it also
    # -- reads the user preferences and configure the console's colors.
    ApioContext(scope=ApioContextScope.NO_PROJECT)

    # -- If option was specified, validate it.
    if option:
        if option not in project.OPTIONS:
            cerror(f"No such api.ini option: '{option}'")
            cout(
                "For the list of all apio.ini options, type "
                "'apio docs options'.",
                style=INFO,
            )
            sys.exit(1)

    # -- If printing all the options, print first the overview.
    if not option:
        docs_text(APIO_INI_DOC)

    # -- Determine options to print
    options = [option] if option else project.OPTIONS.keys()

    # -- Print the initial separator line.
    docs_rule()
    for opt in options:
        # -- Print option's title.
        is_required = opt in project.REQUIRED_OPTIONS
        req = "REQUIRED" if is_required else "OPTIONAL"
        styled_option = cstyle(opt.upper(), style=TITLE)
        cout()
        cout(f"{styled_option} ({req})")

        # -- Print the option's text.
        text = project.OPTIONS[opt]
        docs_text(text)
        docs_rule()
