# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- License GPLv2
"""Implementation of 'apio' report' command"""

import sys
from pathlib import Path
import click
from apio.managers.scons import SCons
from apio.commands import options
from apio.apio_context import ApioContext, ApioContextScope
from apio.common.proto.apio_pb2 import Verbosity
from apio.utils import cmd_util


# ---------- apio report

# -- Text in the markdown format of the python rich library.
APIO_REPORT_HELP = """
The command 'apio report' provides information on the utilization and timing \
of the design. It is useful for analyzing utilization bottlenecks and \
verifying that the design can operate at the desired clock speed.

Examples:[code]
  apio report            # Print report.
  apio report --verbose  # Print extra information.[/code]
"""


# pylint: disable=duplicate-code
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
@click.command(
    name="report",
    cls=cmd_util.ApioCommand,
    short_help="Report design utilization and timing.",
    help=APIO_REPORT_HELP,
)
@click.pass_context
@options.project_dir_option
@options.verbose_option
def cli(
    _: click.Context,
    # Options
    project_dir: Path,
    verbose: bool,
):
    """Analyze the design and report timing."""

    # -- Create the apio context.
    apio_ctx = ApioContext(
        scope=ApioContextScope.PROJECT_REQUIRED,
        project_dir_arg=project_dir,
    )

    # -- Create the scons manager.
    scons = SCons(apio_ctx)

    # -- Create the verbosity params.
    verbosity = Verbosity(pnr=verbose)

    # Run scons
    exit_code = scons.report(verbosity)

    # -- Done!
    sys.exit(exit_code)
