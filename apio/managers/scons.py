"""DOC: TODO"""

# C0302: Too many lines in module (1032/1000) (too-many-lines)
# pylint: disable=C0302

# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2019 FPGAwars
# -- Author Jesús Arroyo
# -- License GPLv2

import traceback
import os
import sys
import time
import shutil
from functools import wraps
from datetime import datetime
from google.protobuf import text_format
from apio.common import apio_console
from apio.common.apio_console import cout, cerror, cstyle
from apio.common.styles import SUCCESS, ERROR, EMPH1, EMPH3
from apio.utils import util, pkg_util
from apio.common.apio_consts import BUILD_DIR
from apio.apio_context import ApioContext
from apio.managers.scons_filter import SconsFilter
from apio.managers import installer
from apio.common import rich_lib_windows
from apio.common.proto.apio_pb2 import (
    FORCE_PIPE,
    FORCE_TERMINAL,
    Verbosity,
    Environment,
    SconsParams,
    TargetParams,
    FpgaInfo,
    Project,
    Ice40FpgaInfo,
    Ecp5FpgaInfo,
    GowinFpgaInfo,
    ApioArch,
    GraphParams,
    LintParams,
    SimParams,
    ApioTestParams,
    UploadParams,
)

# -- Constant for the dictionary PROG, which contains
# -- the programming configuration
SERIAL_PORT = "serial_port"
FTDI_ID = "ftdi_id"
SRAM = "sram"
FLASH = "flash"


# W0703: Catching too general exception Exception (broad-except)
# pylint: disable=W0703
# pylint: disable=W0150
#
# -- Based on
# -- https://stackoverflow.com/questions/5929107/decorators-with-parameters
def on_exception(*, exit_code: int):
    """Decorator for functions that return int exit code. If the function
    throws an exception, the error message is printed, and the caller see the
    returned value exit_code instead of the exception.
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as exc:
                if util.is_debug():
                    traceback.print_tb(exc.__traceback__)

                if str(exc):
                    cerror(str(exc))
                return exit_code

        return wrapper

    return decorator


class SCons:
    """Class for managing the scons tools"""

    def __init__(self, apio_ctx: ApioContext):
        """Initialization."""
        # -- Cache the apio context.
        self.apio_ctx = apio_ctx

        # -- Change to the project's folder.
        os.chdir(apio_ctx.project_dir)

    @on_exception(exit_code=1)
    def clean(self) -> int:
        """Runs a scons subprocess with the 'clean' option. Returns process
        exit code, 0 if ok."""

        scons_params = self.construct_scons_params()

        # --Clean the project: run scons -c (with additional arguments)
        return self._run("-c", scons_params=scons_params, uses_packages=False)

    @on_exception(exit_code=1)
    def graph(self, graph_params: GraphParams, verbosity: Verbosity) -> int:
        """Runs a scons subprocess with the 'graph' target. Returns process
        exit code, 0 if ok."""

        # -- Construct scons params with graph command info.
        scons_params = self.construct_scons_params(
            target_params=TargetParams(graph=graph_params),
            verbosity=verbosity,
        )

        # -- Run the scons process.
        return self._run(
            "graph",
            scons_params=scons_params,
            uses_packages=True,
        )

    @on_exception(exit_code=1)
    def lint(self, lint_params: LintParams) -> int:
        """Runs a scons subprocess with the 'lint' target. Returns process
        exit code, 0 if ok."""

        # -- Construct scons params with graph command info.
        scons_params = self.construct_scons_params(
            target_params=TargetParams(lint=lint_params)
        )

        # -- Run the scons process.
        return self._run("lint", scons_params=scons_params, uses_packages=True)

    @on_exception(exit_code=1)
    def sim(self, sim_params: SimParams) -> int:
        """Runs a scons subprocess with the 'sim' target. Returns process
        exit code, 0 if ok."""

        # -- Construct scons params with graph command info.
        scons_params = self.construct_scons_params(
            target_params=TargetParams(sim=sim_params)
        )

        # -- Run the scons process.
        return self._run(
            "sim",
            scons_params=scons_params,
            uses_packages=True,
        )

    @on_exception(exit_code=1)
    def test(self, test_params: ApioTestParams) -> int:
        """Runs a scons subprocess with the 'test' target. Returns process
        exit code, 0 if ok."""

        # -- Construct scons params with graph command info.
        scons_params = self.construct_scons_params(
            target_params=TargetParams(test=test_params)
        )

        # -- Run the scons process.
        return self._run(
            "test",
            scons_params=scons_params,
            uses_packages=True,
        )

    @on_exception(exit_code=1)
    def build(self, verbosity: Verbosity) -> int:
        """Runs a scons subprocess with the 'build' target. Returns process
        exit code, 0 if ok."""

        # -- Construct the scons params object.
        scons_params = self.construct_scons_params(verbosity=verbosity)

        # -- Run the scons process.
        return self._run(
            "build",
            scons_params=scons_params,
            uses_packages=True,
        )

    @on_exception(exit_code=1)
    def report(self, verbosity: Verbosity) -> int:
        """Runs a scons subprocess with the 'report' target. Returns process
        exit code, 0 if ok."""

        # -- Construct the scons params object.
        scons_params = self.construct_scons_params(verbosity=verbosity)

        # -- Run the scons process.
        return self._run(
            "report", scons_params=scons_params, uses_packages=True
        )

    @on_exception(exit_code=1)
    def upload(self, upload_params: UploadParams) -> int:
        """Runs a scons subprocess with the 'time' target. Returns process
        exit code, 0 if ok.
        """

        # -- Construct the scons params.
        scons_params = self.construct_scons_params(
            target_params=TargetParams(upload=upload_params)
        )

        # -- Execute Scons for uploading!
        exit_code = self._run(
            "upload",
            scons_params=scons_params,
            uses_packages=True,
        )

        return exit_code

    def construct_scons_params(
        self,
        *,
        target_params: TargetParams = None,
        verbosity: Verbosity = None,
    ) -> SconsParams:
        """Populate and return the SconsParam proto to pass to the scons
        process."""

        # -- Create a shortcut.
        apio_ctx = self.apio_ctx

        # -- Create an empty proto object that will be populated.
        result = SconsParams()

        # -- Populate the timestamp. We use to to make sure scons reads the
        # -- correct version of the scons.params file.
        ts = datetime.now()
        result.timestamp = ts.strftime("%d%H%M%S%f")[:-3]

        # -- Get the project data. All commands that invoke scons are expected
        # -- to be in a project context.
        assert apio_ctx.has_project, "Scons encountered a missing project."
        project = apio_ctx.project

        # -- Get the project's board. It should be prevalidated when loading
        # -- the project, but we sanity check it again just in case.
        board = project["board"]
        assert board is not None, "Scons got a None board."
        assert board in apio_ctx.boards, f"Unknown board name [{board}]"

        # -- Get the project fpga id from the board info.
        fpga_id = apio_ctx.boards.get(board).get("fpga")
        assert fpga_id, "construct_scons_params(): fpga assertion failed."
        assert (
            fpga_id in apio_ctx.fpgas
        ), f"construct_scons_params(): unknown fpga {fpga_id} "
        fpga_config = apio_ctx.fpgas.get(fpga_id)
        fpga_arch = fpga_config["arch"]

        # -- Populate the common values of FpgaInfo.
        result.fpga_info.MergeFrom(
            FpgaInfo(
                fpga_id=fpga_id,
                part_num=fpga_config["part_num"],
                size=fpga_config["size"],
            )
        )

        # - Populate the architecture specific values of result.fpga_info.
        if fpga_arch == "ice40":
            result.arch = ApioArch.ICE40
            result.fpga_info.ice40.MergeFrom(
                Ice40FpgaInfo(
                    type=fpga_config["type"], pack=fpga_config["pack"]
                )
            )
        elif fpga_arch == "ecp5":
            result.arch = ApioArch.ECP5
            result.fpga_info.ecp5.MergeFrom(
                Ecp5FpgaInfo(
                    type=fpga_config["type"],
                    pack=fpga_config["pack"],
                    speed=fpga_config["speed"],
                )
            )
        elif fpga_arch == "gowin":
            result.arch = ApioArch.GOWIN
            result.fpga_info.gowin.MergeFrom(
                GowinFpgaInfo(family=fpga_config["type"])
            )
        else:
            cerror(f"Unexpected fpga_arch value {fpga_arch}")
            sys.exit(1)

        # -- We are done populating The FpgaInfo params..
        assert result.fpga_info.IsInitialized(), result

        # -- Populate the optional Verbosity params.
        if verbosity:
            result.verbosity.MergeFrom(verbosity)
            assert result.verbosity.IsInitialized(), result

        # -- Populate the Environment params.
        assert apio_ctx.platform_id, "Missing platform_id in apio context"
        oss_vars = apio_ctx.all_packages["oss-cad-suite"]["env"]["vars"]

        result.environment.MergeFrom(
            Environment(
                platform_id=apio_ctx.platform_id,
                is_windows=apio_ctx.is_windows,
                terminal_mode=(
                    FORCE_TERMINAL
                    if apio_console.is_terminal()
                    else FORCE_PIPE
                ),
                theme_name=apio_console.theme(),
                is_debug=util.is_debug(),
                yosys_path=oss_vars["YOSYS_LIB"],
                trellis_path=oss_vars["TRELLIS"],
            )
        )
        assert result.environment.IsInitialized(), result

        # -- Populate the Project params.
        result.project.MergeFrom(
            Project(
                board_id=project["board"],
                top_module=project["top-module"],
                yosys_synth_extra_options=apio_ctx.project.get(
                    "yosys-synth-extra-options", None
                ),
            )
        )
        assert result.project.IsInitialized(), result

        # -- Populate the optional command specific params.
        if target_params:
            result.target.MergeFrom(target_params)
            assert result.target.IsInitialized(), result

        # -- If windows, populate the rich library workaround parameters.
        if apio_ctx.is_windows:
            result.rich_lib_windows_params.MergeFrom(
                rich_lib_windows.get_workaround_params()
            )

        # -- All done.
        assert result.IsInitialized(), result
        return result

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    def _run(
        self,
        scons_command: str,
        *,
        scons_params: SconsParams = None,
        uses_packages: bool,
    ):
        """Invoke an scons subprocess."""

        # -- Pass to the scons process the name of the sconstruct file it
        # -- should use.
        scons_dir = util.get_path_in_apio_package("scons")
        scons_file_path = scons_dir / "SConstruct"
        variables = ["-f", f"{scons_file_path}"]

        # -- Pass to the scons process the timestamp of the scons params we
        # -- pass via a file. This is for verification purposes only.
        variables += [f"timestamp={scons_params.timestamp}"]

        # -- If the apio packages are required for this command, install them
        # -- if needed.
        if uses_packages:
            installer.install_missing_packages_on_the_fly(self.apio_ctx)

        # -- We set the env variables also for a command such as 'clean'
        # -- which doesn't use the packages, to satisfy the required env
        # -- variables of the scons arg parser.
        pkg_util.set_env_for_packages(self.apio_ctx)

        if util.is_debug():
            cout("\nSCONS CALL:", style=EMPH3)
            cout(f"* command:       {scons_command}")
            cout(f"* variables:     {variables}")
            cout(f"* uses packages: {uses_packages}")
            cout(f"* scons params: \n{scons_params}")
            cout()

        # -- Get the terminal width (typically 80)
        terminal_width, _ = shutil.get_terminal_size()

        # -- Read the time (for measuring how long does it take
        # -- to execute the apio command)
        start_time = time.time()

        # -- Board name string in color
        styled_board_id = cstyle(scons_params.project.board_id, style=EMPH1)

        # -- Print information on the console
        cout(f"Processing board {styled_board_id}")

        # -- Print a horizontal line
        cout("-" * terminal_width)

        # -- Create the scons debug options. See details at
        # -- https://scons.org/doc/2.4.1/HTML/scons-man.html
        debug_options = (
            ["--debug=explain,prepare,stacktrace", "--tree=all"]
            if util.is_debug()
            else []
        )

        # -- Command to execute: scons -Q apio_cmd flags
        scons_command = (
            ["scons"] + ["-Q", scons_command] + debug_options + variables
        )

        # -- An output filter that manipulates the scons stdout/err lines as
        # -- needed and write them to stdout.
        scons_filter = SconsFilter(
            colors_enabled=apio_console.is_colors_enabled()
        )

        # -- Write the scons parameters to a temp file in the build
        # -- directory. It will be cleaned up as part of 'apio cleanup'.
        # -- At this point, the project is the current directory, even if
        # -- the command used the --project-dir option.
        os.makedirs(BUILD_DIR, exist_ok=True)
        with open(BUILD_DIR / "scons.params", "w", encoding="utf8") as f:
            f.write(text_format.MessageToString(scons_params))

        # -- Execute the scons builder!
        result = util.exec_command(
            scons_command,
            stdout=util.AsyncPipe(scons_filter.on_stdout_line),
            stderr=util.AsyncPipe(scons_filter.on_stderr_line),
        )

        # -- Is there an error? True/False
        is_error = result.exit_code != 0

        # -- Calculate the time it took to execute the command
        duration = time.time() - start_time

        # -- Summary
        summary_text = f" Took {duration:.2f} seconds "

        # -- Half line
        half_line = "=" * int(((terminal_width - len(summary_text) - 10) / 2))

        # -- Status message
        status = (
            cstyle(" ERROR ", style=ERROR)
            if is_error
            else cstyle("SUCCESS", style=SUCCESS)
        )

        # -- Print the summary line.
        cout(f"{half_line} [{status}]{summary_text}{half_line}")

        # -- Return the exit code
        return result.exit_code
