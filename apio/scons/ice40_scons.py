"""Scons script of ICE40 FPGAs."""

# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors Juan Gonzáles, Jesús Arroyo
# -- Licence GPLv2

# pylint: disable=too-many-locals
# pylint: disable=invalid-name
# pylint: disable=consider-using-f-string
# pylint: disable=too-many-statements
# -- Similar lines
# pylint: disable= R0801

import os
from SCons.Script import (
    Builder,
    GetOption,
    COMMAND_LINE_TARGETS,
    ARGUMENTS,
)
from apio.scons.scons_util import (
    TARGET,
    SConstructId,
    has_testbench_name,
    basename,
    get_constraint_file,
    create_construction_env,
    arg_bool,
    arg_str,
    get_programmer_cmd,
    make_verilog_src_scanner,
    make_verilator_config_builder,
    make_dot_builder,
    make_graphviz_builder,
    get_source_files,
    get_sim_config,
    get_tests_configs,
    make_waves_target,
    make_iverilog_action,
    make_verilator_action,
    get_report_action,
    set_up_cleanup,
    get_source_file_issue_action,
    vlt_path,
    unused,
)


def scons_handler():
    """Scons handler for ice40."""

    # # -- Uncomment for debugging of the scons subprocess using a remote
    # # -- debugger.
    # from apio.scons import scons_util
    # scons_util.wait_for_remote_debugger()

    # -- Create the environment
    env = create_construction_env(ARGUMENTS)

    # -- Get arguments.
    FPGA_SIZE = arg_str(env, "fpga_size", "")
    FPGA_TYPE = arg_str(env, "fpga_type", "")
    FPGA_PACK = arg_str(env, "fpga_pack", "")
    TOP_MODULE = arg_str(env, "top_module", "")
    VERBOSE_ALL = arg_bool(env, "verbose_all", False)
    VERBOSE_YOSYS = arg_bool(env, "verbose_yosys", False)
    VERBOSE_PNR = arg_bool(env, "verbose_pnr", False)
    TESTBENCH = arg_str(env, "testbench", "")
    FORCE_SIM = arg_bool(env, "force_sim", False)
    VERILATOR_ALL = arg_bool(env, "all", False)
    VERILATOR_NO_STYLE = arg_bool(env, "nostyle", False)
    VERILATOR_NOWARNS = arg_str(env, "nowarn", "").split(",")
    VERILATOR_WARNS = arg_str(env, "warn", "").split(",")
    GRAPH_SPEC = arg_str(env, "graph_spec", "")

    # -- Resources paths
    YOSYS_PATH = os.environ["YOSYS_LIB"] if "YOSYS_LIB" in os.environ else ""
    YOSYS_LIB_DIR = YOSYS_PATH + "/ice40"
    YOSYS_LIB_FILE = YOSYS_LIB_DIR + "/cells_sim.v"

    # -- Create scannenr to identify dependencies in verilog files.
    verilog_src_scanner = make_verilog_src_scanner(env)

    # -- Get a list of the synthesizable files (e.g. "main.v") and a list of
    # -- the testbench files (e.g. "main_tb.v")
    synth_srcs, test_srcs = get_source_files(env)

    # -- Get the PCF file name.
    PCF = get_constraint_file(env, ".pcf", TOP_MODULE)

    # -- Apio build/upload/report.
    # -- Builder (yosys, Synthesis).
    # -- (modules).v -> hardware.json.
    synth_builder = Builder(
        action='yosys -p "synth_ice40 {0} -json $TARGET" {1} $SOURCES'.format(
            ("-top " + TOP_MODULE) if TOP_MODULE else "",
            "" if VERBOSE_ALL or VERBOSE_YOSYS else "-q",
        ),
        suffix=".json",
        src_suffix=".v",
        source_scanner=verilog_src_scanner,
    )
    env.Append(BUILDERS={"Synth": synth_builder})

    # -- The name of the report file generated by nextpnr.
    PNR_REPORT_FILE: str = TARGET + ".pnr"

    # -- Apio report.
    # -- emmiter (nextpnr, Place and route).
    # -- hardware.json -> hardware.pnr.
    def pnr_emitter(target, source, env):
        """A scons emmiter function for the pnr builder. It declares that the
        nextpnr builder creates also a second file called 'hardware.pnr'."""
        unused(env)
        target.append(PNR_REPORT_FILE)
        return target, source

    # -- Apio build/upload/report.
    # -- builder (nextpnr, Place and route).
    # -- hardware.json -> hardware.asc, hardware.pnr.
    pnr_builder = Builder(
        action=(
            "nextpnr-ice40 --{0}{1} --package {2} --json $SOURCE "
            "--asc $TARGET --report {3} --pcf {4} {5}"
        ).format(
            FPGA_TYPE,
            FPGA_SIZE,
            FPGA_PACK,
            PNR_REPORT_FILE,
            PCF,
            "" if VERBOSE_ALL or VERBOSE_PNR else "-q",
        ),
        suffix=".asc",
        src_suffix=".json",
        emitter=pnr_emitter,
    )
    env.Append(BUILDERS={"PnR": pnr_builder})

    # -- Apio build/upload.
    # -- Builder (icepack, bitstream generator).
    # -- hardware.asc -> hardware.bin.
    bitstream_builder = Builder(
        action="icepack $SOURCE $TARGET", suffix=".bin", src_suffix=".asc"
    )
    env.Append(BUILDERS={"Bin": bitstream_builder})

    # -- Apio build/upload/report.
    # -- Targets.
    # -- (module).v -> hardware.json -> hardware.asc -> hardware.bin.
    synth_target = env.Synth(TARGET, [synth_srcs])
    pnr_target = env.PnR(TARGET, [synth_target, PCF])
    bin_target = env.Bin(TARGET, pnr_target)
    build_target = env.Alias("build", bin_target)

    if VERBOSE_YOSYS:
        env.AlwaysBuild(synth_target)
    if VERBOSE_PNR:
        env.AlwaysBuild(pnr_target)
    if VERBOSE_ALL:
        env.AlwaysBuild(synth_target, pnr_target, build_target)

    # -- Apio report.
    # -- Targets.
    # -- hardware.asc -> hardware.pnr -> (report)
    # pnr_report_target = env.PnrReport(TARGET, pnr_target)
    report_action = get_report_action(
        env, SConstructId.SCONSTRUCT_ICE40, VERBOSE_PNR
    )
    report_target = env.Alias("report", PNR_REPORT_FILE, report_action)
    env.AlwaysBuild(report_target)

    # -- Apio upload.
    # -- Targets.
    # -- hardware.bin -> FPGA.
    programmer_cmd: str = get_programmer_cmd(env)
    upload_target = env.Alias("upload", bin_target, programmer_cmd)
    env.AlwaysBuild(upload_target)

    # -- Apio sim/test
    # -- Builder helper (iverolog command generator).
    # -- (modules + testbench).v -> (testbench).out.
    def iverilog_tb_generator(source, target, env, for_signature):
        """Construct the action string for the iverilog_tb_builder builder
        for a given testbench target."""
        unused(source, for_signature)
        # Extract testbench name from target file name.
        testbench_file = str(target[0])
        assert has_testbench_name(env, testbench_file), testbench_file
        testbench_name = basename(env, testbench_file)

        # Construct the command line.
        action = [
            # -- Scan source files for issues.
            get_source_file_issue_action(env),
            # -- Perform the actual test or sim compilation.
            make_iverilog_action(
                env,
                verbose=VERBOSE_ALL,
                vcd_output_name=testbench_name,
                is_interactive=("sim" in COMMAND_LINE_TARGETS),
                extra_params=["-DNO_ICE40_DEFAULT_ASSIGNMENTS"],
                lib_files=[YOSYS_LIB_FILE],
            ),
        ]
        return action

    # -- Apio sim/test.
    # -- Builder (iverilog, verilog compiler).
    # -- (modules + testbench).v -> (testbench).out.
    iverilog_tb_builder = Builder(
        # Action string is different for sim and for
        generator=iverilog_tb_generator,
        suffix=".out",
        src_suffix=".v",
        source_scanner=verilog_src_scanner,
    )
    env.Append(BUILDERS={"IVerilogTestbench": iverilog_tb_builder})

    # -- Apio graph.
    # -- Builder (yosys, .dot graph generator).
    # -- hardware.v -> hardware.dot.
    dot_builder = make_dot_builder(
        env, TOP_MODULE, verilog_src_scanner, VERBOSE_ALL
    )
    env.Append(BUILDERS={"DOT": dot_builder})

    # -- Apio graph.
    # -- Builder  (dot, svg/pdf/png renderer).
    # -- hardware.dot -> hardware.svg/pdf/png.
    graphviz_builder = make_graphviz_builder(env, GRAPH_SPEC)
    env.Append(BUILDERS={"GRAPHVIZ": graphviz_builder})

    # -- Apio sim/test.
    # -- Builder (vvp, simulator).
    # -- (testbench).out -> (testbench).vcd.
    vcd_builder = Builder(
        action="vvp $SOURCE -dumpfile=$TARGET",
        suffix=".vcd",
        src_suffix=".out",
    )
    env.Append(BUILDERS={"VCD": vcd_builder})

    # -- Apio graph.
    # -- Targets.
    # -- (modules).v -> hardware.dot -> hardware.svg.
    dot_target = env.DOT(TARGET, synth_srcs)
    env.AlwaysBuild(dot_target)
    graphviz_target = env.GRAPHVIZ(TARGET, dot_target)
    env.AlwaysBuild(graphviz_target)
    graph_target = env.Alias("graph", graphviz_target)
    env.AlwaysBuild(graph_target)

    # -- Apio sim.
    # -- Targets.
    # -- (modules).v -> (testbench).out -> (testbench).vcd -> gtkwave
    if "sim" in COMMAND_LINE_TARGETS:
        sim_config = get_sim_config(env, TESTBENCH, synth_srcs)
        sim_out_target = env.IVerilogTestbench(
            sim_config.build_testbench_name, sim_config.srcs
        )
        if FORCE_SIM:
            env.AlwaysBuild(sim_out_target)
        sim_vcd_target = env.VCD(sim_out_target)
        if FORCE_SIM:
            env.AlwaysBuild(sim_vcd_target)
        waves_target = make_waves_target(env, sim_vcd_target, sim_config)
        env.AlwaysBuild(waves_target)

    # -- Apio test.
    # -- Targets.
    # -- (modules).v -> (testbenchs).out -> (testbenchs).vcd
    if "test" in COMMAND_LINE_TARGETS:
        tests_configs = get_tests_configs(
            env, TESTBENCH, synth_srcs, test_srcs
        )
        tests_targets = []
        for sim_config in tests_configs:
            test_out_target = env.IVerilogTestbench(
                sim_config.build_testbench_name, sim_config.srcs
            )
            env.AlwaysBuild(test_out_target)
            test_vcd_target = env.VCD(test_out_target)
            env.AlwaysBuild(test_vcd_target)
            test_target = env.Alias(
                sim_config.build_testbench_name,
                [test_out_target, test_vcd_target],
            )
            tests_targets.append(test_target)

        # Create a target for the test command that depends on all the test
        # targets.
        tests_target = env.Alias("test", tests_targets)
        env.AlwaysBuild(tests_target)

    # -- Apio lint.
    # -- Builder (plain text generator)
    # -- (none) -> hardware.vlt builder.
    verilator_config_builder = make_verilator_config_builder(
        env,
        (
            "`verilator_config\n"
            f'lint_off -rule COMBDLY     -file "{vlt_path(YOSYS_LIB_DIR)}/*"\n'
            f'lint_off -rule WIDTHEXPAND -file "{vlt_path(YOSYS_LIB_DIR)}/*"\n'
        ),
    )
    env.Append(BUILDERS={"VerilatorConfig": verilator_config_builder})

    # -- Apio lint.
    # -- Builder (verilator, verilog linter)
    # -- (modules + testbenches).v -> lint report to stdout builder.
    verilator_builder = Builder(
        action=[
            # -- Scan the source files for 'other' issues.
            get_source_file_issue_action(env),
            # -- Perform the lint.
            make_verilator_action(
                env,
                warnings_all=VERILATOR_ALL,
                warnings_no_style=VERILATOR_NO_STYLE,
                no_warns=VERILATOR_NOWARNS,
                warns=VERILATOR_WARNS,
                top_module=TOP_MODULE,
                extra_params=["-DNO_ICE40_DEFAULT_ASSIGNMENTS"],
                lib_files=[YOSYS_LIB_FILE],
            ),
        ],
        src_suffix=".v",
        source_scanner=verilog_src_scanner,
    )
    env.Append(BUILDERS={"Verilator": verilator_builder})

    # -- Apio lint.
    # -- Targets.
    # -- (modules).v -> lint report to stdout.
    lint_config_target = env.VerilatorConfig(TARGET, [])
    lint_out_target = env.Verilator(TARGET, synth_srcs + test_srcs)
    env.Depends(lint_out_target, lint_config_target)
    lint_target = env.Alias("lint", lint_out_target)
    env.AlwaysBuild(lint_target)

    # -- Handle the cleanu of the artifact files.
    if GetOption("clean"):
        set_up_cleanup(env)
