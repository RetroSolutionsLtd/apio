# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- Licence GPLv2
"""Implementation of 'apio' report' command"""

import sys
from pathlib import Path
import click
from apio.managers.scons import SCons
from apio import cmd_util
from apio.commands import options
from apio.apio_context import ApioContext


# ---------------------------
# -- COMMAND
# ---------------------------
HELP = """
The report command reports the utilization and timing of the design.
It is useful to analyzer utilization bottle neck and to verify that
the design can run at a desired clock speed.
The commands is typically used in the root directory
of the project that contains the apio.ini file.

\b
Examples:
  apio report
  epio report --verbose

"""


# pylint: disable=duplicate-code
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
@click.command(
    "report",
    short_help="Report design utilization and timing.",
    help=HELP,
    cls=cmd_util.ApioCommand,
)
@click.pass_context
@options.project_dir_option
@options.verbose_option
def cli(
    _: click.core.Context,
    # Options
    project_dir: Path,
    verbose: bool,
):
    """Analyze the design and report timing."""

    # -- Create the apio context.
    apio_ctx = ApioContext(project_dir=project_dir, load_project=True)

    # -- Create the scons manager.
    scons = SCons(apio_ctx)

    # Run scons
    exit_code = scons.report(
        {
            "verbose_pnr": verbose,
        }
    )

    # -- Done!
    sys.exit(exit_code)
