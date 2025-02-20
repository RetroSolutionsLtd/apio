# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2018 FPGAwars
# -- Author Jesús Arroyo
# -- License GPLv2
# -- Derived from:
# ---- Platformio project
# ---- (C) 2014-2016 Ivan Kravets <me@ikravets.com>
# ---- License Apache v2
"""Utility functionality for apio click commands. """

import sys
from dataclasses import dataclass
from typing import List, Dict, Union
import click
from click.formatting import HelpFormatter
from apio.profile import Profile
from apio.common.styles import CMD_NAME
from apio.common.apio_console import (
    ConsoleCapture,
    cout,
    cerror,
    cstyle,
    docs_text,
)
from apio.utils import util


def fatal_usage_error(cmd_ctx: click.Context, msg: str) -> None:
    """Prints a an error message and command help hint, and exists the program
     with an error status.
    cmd_ctx: The context that was passed to the command.
    msg: A single line short error message.
    """
    # Mimicking the usage error message from click/exceptions.py.
    # E.g. "Try 'apio packages -h' for help."
    cout(cmd_ctx.get_usage())
    cout(
        f"Try '{cmd_ctx.command_path} {cmd_ctx.help_option_names[0]}' "
        "for help."
    )
    cout("")
    cerror(f"{msg}")
    sys.exit(1)


def _get_all_params_definitions(
    cmd_ctx: click.Context,
) -> Dict[str, Union[click.Option, click.Argument]]:
    """Return a mapping from param id to param obj, for all options and
    arguments that are defined for the command."""
    result = {}
    for param_obj in cmd_ctx.command.get_params(cmd_ctx):
        assert isinstance(param_obj, (click.Option, click.Argument)), type(
            param_obj
        )
        result[param_obj.name] = param_obj
    return result


def _params_ids_to_aliases(
    cmd_ctx: click.Context, params_ids: List[str]
) -> List[str]:
    """Maps param ids to their respective user facing canonical aliases.
    The order of the params is in the input list is preserved.

    For the definition of param ids see check_exclusive_params().

    The canonical alias of an option is it's longest alias,
    for example "--dir" for the option ["-d", "--dir"]. The canonical
    alias of an argument is the argument name as shown in the command's help,
    e.g. "PACKAGES" for the argument packages.
    """
    # Param id -> param obj.
    params_dict = _get_all_params_definitions(cmd_ctx)

    # Map the param ids to their canonical aliases.
    result = []
    for param_id in params_ids:
        param_obj: Union[click.Option, click.Argument] = params_dict[param_id]
        assert isinstance(param_obj, (click.Option, click.Argument)), type(
            param_obj
        )
        if isinstance(param_obj, click.Option):
            # For options we pick their longest alias
            param_alias = max(param_obj.aliases, key=len)
        else:
            # For arguments we pick its user facing name, e.g. "PACKAGES"
            # for argument packages.
            param_alias = param_obj.human_readable_name
        assert param_obj is not None, param_id
        result.append(param_alias)
    return result


def _is_param_specified(cmd_ctx, param_id) -> bool:
    """Determine if the param with given id was specified in the
    command line."""
    # Mapping: param id -> param obj.
    params_dict = _get_all_params_definitions(cmd_ctx)
    # Get the official status.
    param_src = cmd_ctx.get_parameter_source(param_id)
    is_specified = param_src == click.core.ParameterSource.COMMANDLINE
    # A special case for repeating arguments. Click considers the
    # empty tuple value to come with the command line but we consider
    # it to come from the default.
    is_arg = isinstance(params_dict[param_id], click.Argument)
    if is_specified and is_arg:
        arg_value = cmd_ctx.params[param_id]
        if arg_value == tuple():
            is_specified = False
    # All done
    return is_specified


def _specified_params(
    cmd_ctx: click.Context, param_ids: List[str]
) -> List[str]:
    """Returns the subset of param ids that were used in the command line.
    The original order of the list is preserved.
    For definition of params and param ids see check_exclusive_params().
    """
    result = []
    for param_id in param_ids:
        if _is_param_specified(cmd_ctx, param_id):
            result.append(param_id)
    return result


def check_at_most_one_param(
    cmd_ctx: click.Context, param_ids: List[str]
) -> None:
    """Checks that at most one of given params were specified in
    the command line. If more than one param was specified, exits the
    program with a message and error status.

    Params are click options and arguments that are passed to a command.
    Param ids are the names of variables that are used to pass options and
    argument values to the command. A safe way to construct param_ids
    is nameof(param_var1, param_var2, ...)
    """
    # The the subset of ids of params that where used in the command.
    specified_param_ids = _specified_params(cmd_ctx, param_ids)
    # If more 2 or more print an error and exit.
    if len(specified_param_ids) >= 2:
        canonical_aliases = _params_ids_to_aliases(
            cmd_ctx, specified_param_ids
        )
        aliases_str = util.list_plurality(canonical_aliases, "and")
        fatal_usage_error(
            cmd_ctx, f"{aliases_str} cannot be combined together."
        )


def check_exactly_one_param(
    cmd_ctx: click.Context, param_ids: List[str]
) -> None:
    """Checks that at exactly one of given params is specified in
    the command line. If more or less than one params is specified, exits the
    program with a message and error status.

    Params are click options and arguments that are passed to a command.
    Param ids are the names of variables that are used to pass options and
    argument values to the command. A safe way to construct param_ids
    is nameof(param_var1, param_var2, ...)
    """
    # The the subset of ids of params that where used in the command.
    specified_param_ids = _specified_params(cmd_ctx, param_ids)
    # If exactly one than we are good.
    if len(specified_param_ids) == 1:
        return
    if len(specified_param_ids) < 1:
        # -- User specified Less flags than required.
        canonical_aliases = _params_ids_to_aliases(cmd_ctx, param_ids)
        aliases_str = util.list_plurality(canonical_aliases, "or")
        fatal_usage_error(cmd_ctx, f"specify one of {aliases_str}.")
    else:
        # -- User specified more flags than allowed.
        canonical_aliases = _params_ids_to_aliases(
            cmd_ctx, specified_param_ids
        )
        aliases_str = util.list_plurality(canonical_aliases, "and")
        fatal_usage_error(
            cmd_ctx, f"{aliases_str} cannot be combined together."
        )


def check_at_least_one_param(
    cmd_ctx: click.Context, param_ids: List[str]
) -> None:
    """Checks that at least one of given params is specified in
    the command line. If none of the params is specified, exits the
    program with a message and error status.

    Params are click options and arguments that are passed to a command.
    Param ids are the names of variables that are used to pass options and
    argument values to the command. A safe way to construct param_ids
    is nameof(param_var1, param_var2, ...)
    """
    # The the subset of ids of params that where used in the command.
    specified_param_ids = _specified_params(cmd_ctx, param_ids)
    # If more 2 or more print an error and exit.
    if len(specified_param_ids) < 1:
        canonical_aliases = _params_ids_to_aliases(cmd_ctx, param_ids)
        aliases_str = util.list_plurality(canonical_aliases, "or")
        fatal_usage_error(
            cmd_ctx, f"at list one of {aliases_str} must be specified."
        )


class ApioOption(click.Option):
    """Custom class for apio click options. Currently it adds handling
    of deprecated options.
    """

    def __init__(self, *args, **kwargs):
        # Cache a list of option's aliases. E.g. ["-t", "--top-model"].
        self.aliases = [k for k in args[0] if k.startswith("-")]

        # Pass the rest to the base class.
        super().__init__(*args, **kwargs)


@dataclass(frozen=True)
class ApioSubgroup:
    """A class to represent a named group of subcommands. An apio command
    of type group, contains two or more subcommand in one or more subgroups."""

    title: str
    commands: List[click.Command]


def _format_apio_markdown_help_text(
    markdown_text: str, formatter: HelpFormatter
) -> None:
    """Format command's or group's help markdown text into a given
    click formatter."""

    # -- Style the metadata text.
    styled_text = None
    with ConsoleCapture() as capture:
        docs_text(markdown_text.rstrip("\n"), end="")
        styled_text = capture.value

    # -- Raw write to the output, with indent.
    lines = styled_text.split("\n")
    for line in lines:
        formatter.write(("  " + line).rstrip(" ") + "\n")


def _patch_partial_commands_names(ctx: click.Context):
    """Traverses the up the chain of command contexts and the partial command
    names in the info_name fields with the full name of the command. This
    causes help and error messages to use the full commands name of the path
    rather than partial names that the user may used. We don't patch the top
    context because it contains the the name used to invoke the program
    rather than the name of the Command object associated with it. This
    function is necessary for the support for partial command names we
    added below. There is no harm in calling this function multiple times.
    """
    c = ctx
    while c.parent is not None:
        # -- Replace the partial name with the full name.
        c.info_name = c.command.name
        # -- Go one context up.
        c = c.parent


class ApioGroup(click.Group):
    """A customized click.Group class that allows apio customized help
    format."""

    def __init__(self, *args, **kwargs):
        # -- Remember if apply_theme was set to True for this command.
        # -- This is used to setup the color preferences before
        # -- the apio top level cli is invoked.
        self._apply_theme = kwargs.pop("apply_theme", False)

        # -- Consume the 'subgroups' arg.
        self._subgroups: List[ApioSubgroup] = kwargs.pop("subgroups")
        assert isinstance(self._subgroups, list)
        assert isinstance(self._subgroups[0], ApioSubgroup)

        # -- Pass the rest of the arg to init the base class.
        super().__init__(*args, **kwargs)

        # -- Register the commands of the subgroups as subcommands of this
        # -- group.
        for subgroup in self._subgroups:
            for cmd in subgroup.commands:
                self.add_command(cmd=cmd, name=cmd.name)

    # @override
    def format_help_text(
        self, ctx: click.Context, formatter: HelpFormatter
    ) -> None:
        """Overrides the parent method that formats the command's help text."""
        _format_apio_markdown_help_text(self.help, formatter)

    # @override
    def format_options(
        self, ctx: click.Context, formatter: HelpFormatter
    ) -> None:
        """Overrides the parent method which formats the options and sub
        commands."""

        # -- Call the grandparent method which formats the options without
        # -- the subcommands.
        click.Command.format_options(self, ctx, formatter)

        # -- Format the subcommands, grouped by the apio defined subgroups
        # -- in self._subgroups.
        formatter.write("\n")

        # -- Get a flat list of all subcommand names.
        cmd_names = [
            cmd.name
            for subgroup in self._subgroups
            for cmd in subgroup.commands
        ]

        # -- Find the length of the longest name.
        max_name_len = max(len(name) for name in cmd_names)

        # -- Generate the subcommands short help, grouped by subgroup.
        for subgroup in self._subgroups:
            assert isinstance(subgroup, ApioSubgroup), subgroup
            formatter.write(f"{subgroup.title}:\n")
            # -- Print the commands that are in this subgroup.
            for cmd in subgroup.commands:
                # -- We pad for field width and then apply color.
                styled_name = cstyle(
                    f"{cmd.name:{max_name_len}}", style=CMD_NAME
                )
                formatter.write(
                    f"  {ctx.command_path} {styled_name}  {cmd.short_help}\n"
                )
            formatter.write("\n")

    # @override
    def get_help(self, ctx: click.Context) -> str:
        """Overrides a super method to add blank line at the end of the help
        text."""
        # -- Special case for the help of the top level apio command since its
        # -- help is generated before any call to get_command().
        if self._apply_theme:
            Profile.apply_color_preferences()

        _patch_partial_commands_names(ctx)
        return super().get_help(ctx) + "\n"

    # @override
    def get_command(self, ctx, cmd_name) -> click.Command:
        """Overrides the method that matches a token in the command line to
        a sub-command. This alternative implementation allows to specify also
        a prefix of the command name, as long as it matches exactly one
        sub command. For example 'pref' or 'p' for 'preferences'.

        Returns the Command or Group (a subclass of Command) of the matching
        sub command or None if not match.
        """

        # -- This is triggered when starting to process the top level apio cli
        # -- command. It sets the colors based on user preferences.
        if self._apply_theme:
            Profile.apply_color_preferences()

        # -- This 'fix' partial command names into their full names,
        # -- to have more intuitive help and usage messages.
        _patch_partial_commands_names(ctx)

        # -- First priority is for exact match. For this we use the click
        # -- default implementation from the parent class.
        cmd: click.Command = click.Group.get_command(self, ctx, cmd_name)
        if cmd is not None:
            return cmd

        # -- Here when there was no exact match, we will try partial matches.
        sub_cmds = self.list_commands(ctx)
        matches = [x for x in sub_cmds if x.startswith(cmd_name)]
        # -- Handle no matches.
        if not matches:
            return None
        # -- Handle multiple matches.
        if len(matches) > 1:
            ctx.fail(f"Command prefix '{cmd_name}' is ambagious: {matches}.")
            # cout(f"Command '{cmd_name}' is ambagious: {matches}", style=INFO)
            return None
        # -- Here when exact match. We are good.
        cmd = click.Group.get_command(self, ctx, matches[0])
        return cmd


class ApioCommand(click.Command):
    """A customized click.Command class that allows apio customized help
    format and proper handling of command shortcuts."""

    # @override
    def format_help_text(
        self, ctx: click.Context, formatter: HelpFormatter
    ) -> None:
        """Overrides the parent method that formats the command's help text."""
        _format_apio_markdown_help_text(self.help, formatter)

    # @override
    def get_help(self, ctx: click.Context) -> str:
        """Overrides a super method to add blank line at the end of the help
        text."""
        _patch_partial_commands_names(ctx)
        return super().get_help(ctx) + "\n"

    # @override
    def parse_args(self, ctx: click.Context, args: List[str]) -> List[str]:
        """Called when the final command was identified but before parsing
        its args. We use it to patch any partial command name (e.b. 'bu')
        to its full command name (e.g. 'build') to have the full names in
        case the help text or a usage error will be printed."""
        # -- Patch names.
        _patch_partial_commands_names(ctx)
        # -- Call the parent implementation.
        return click.Command.parse_args(self, ctx, args)
