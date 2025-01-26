# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- Licence GPLv2
"""Implementation of 'apio system' command"""

import click
from rich.table import Table
from apio.common.apio_console import cprint
from apio.utils import util
from apio.apio_context import ApioContext, ApioContextScope
from apio.utils.cmd_util import ApioGroup, ApioSubgroup


# ------ apio system info

APIO_SYSTEM_INFO_HELP = """
The command ‘apio system info’ provides general information about your system
and Apio installation, which is useful for diagnosing Apio installation issues.

\b
Examples:
  apio system info       # Show platform id and info.

[Advanced] The default location of the Apio home directory, where preferences
and packages are stored, is in the .apio directory under the user’s home
directory. This location can be changed using the APIO_HOME_DIR environment
variable.

"""


@click.command(
    name="info",
    short_help="Show platform id and other info.",
    help=APIO_SYSTEM_INFO_HELP,
)
def _info_cli():
    """Implements the 'apio system info' command."""

    # Create the apio context.
    apio_ctx = ApioContext(scope=ApioContextScope.NO_PROJECT)

    # -- Define the table.
    table = Table(show_header=False, show_lines=True)
    table.add_column(no_wrap=True)
    table.add_column(no_wrap=True, style="cyan")

    # -- Add rows
    table.add_row("Apio version", util.get_apio_version() + "  ")
    table.add_row("Python version ", util.get_python_version() + "  ")
    table.add_row("Platform id ", apio_ctx.platform_id + "  ")
    table.add_row(
        "Python package ", str(util.get_path_in_apio_package("")) + "  "
    )
    table.add_row("Apio home ", str(apio_ctx.home_dir) + "  ")
    table.add_row("Apio packages ", str(apio_ctx.packages_dir) + "  ")

    # -- Render the table.
    cprint(table)


# ------ apio system platforms

APIO_SYSTEM_PLATFORMS_HELP = """
The command ‘apio system platforms’ lists the platform IDs supported by Apio,
with the effective platform ID of your system highlighted.

\b
Examples:
  apio system platforms   # List supported platform ids.

[Advanced] The automatic platform ID detection of Apio can be overridden by
defining a different platform ID using the APIO_PLATFORM environment variable.
"""


@click.command(
    name="platforms",
    short_help="List supported platforms ids.",
    help=APIO_SYSTEM_PLATFORMS_HELP,
)
def _platforms_cli():
    """Implements the 'apio system platforms' command."""

    # Create the apio context.
    apio_ctx = ApioContext(scope=ApioContextScope.NO_PROJECT)

    # -- Define the table.
    table = Table(show_header=False, show_lines=True)
    table.add_column(no_wrap=True)
    table.add_column(no_wrap=True)

    # -- Add rows.
    for platform_id, platform_info in apio_ctx.platforms.items():
        description = platform_info.get("description")

        # -- Mark the current platform.
        if platform_id == apio_ctx.platform_id:
            style = "green bold"
            marker = "* "
        else:
            style = None
            marker = "  "

        table.add_row(
            f"{marker}{platform_id} ", f" {description} ", style=style
        )

    # -- Render the table.
    cprint(table)


# ------ apio system

APIO_SYSTEM_HELP = """
The command group ‘apio system’ contains subcommands that provide information
about the system and Apio’s installation.
"""

# -- We have only a single group with the title 'Subcommands'.
SUBGROUPS = [
    ApioSubgroup(
        "Subcommands",
        [
            _platforms_cli,
            _info_cli,
        ],
    )
]


@click.command(
    name="system",
    cls=ApioGroup,
    subgroups=SUBGROUPS,
    short_help="Provides system info.",
    help=APIO_SYSTEM_HELP,
)
def cli():
    """Implements the 'apio system' command group."""

    # pass
