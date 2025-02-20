# Apio Developers Information

This file is intended for APIO developers.

## Pre commit tests
Before submitting a new commit, make sure to run successfully the following command
in the root directory of the repository.:

```shell
make check
```

For complete tests with several python versions run the command below. 

```shell
make check-all
```

For quick tests that that don't load lengthy packages from the internet
run the command below. It will skip all the tests that require internet 
connection.

```shell
make test
```

For running the linters only, run

```shell
make lint
```

## Test coverage

When running any of the commands below, a test coverage is generated in the
``htmlcov``, to view it open ``htmlcov/index.html`` it with a browser. The ``htmldev`` directory is not checked in the apio repository.

```
make test          // Partial coverage by offline tests
make check         // Full coverage
make check-all     // Full coverage by the last python env run.
```



## Running an individual APIO test

Run from the repo root. Replace with the path to the desire test. Running ``pytest`` alone runs all the tests.

```shell
pytest test/code_commands/test_build.py
```

## Using APIO_DEBUG to print debug information

To print internal debugging information define the environment variable ``APIO_DEBUG`` before running the apio command. The value of ``APIO_DEBUG`` doesn't matter as long as it's defined. Currently the the debugging information is mostly for commands that invoke scons.

Linux and Mac OSX:
```
export APIO_DEV=
```

Windows:
```
set APIO_DEV=
```

## Running apio in a debugger

Set the debugger to run apio main module ``apio/main.py`` main and pass to it the apio arguments. You can run in the project directory or
to add the flag ``--project_dir`` with a path to the project directory.

Example of an equivalent manual command:
```
python apio/main.py build --project_dir test-examples/alhambra-ii/01-LEDs-buttons
```


## Running apio in the Visual Studio Code debugger.

The ``apio`` repository contains at its root the file ``.vscode/launch.jsonc`` with debug
target for most of the ``apio`` commands. Make sure to open the root folder of the repository for VSC to recognize the targets file. To select the debug target, click on the debug icon on the left sidebar and this will display above a pull down menu with the available debug target and a start icon.

[NOTE] This method doesn't not work for debugging the SConstruct scripts since they are run as subprocesses of the apio process. For debugging SConstruct scripts see the next section.

The debug target can be viewed here https://github.com/FPGAwars/apio/blob/develop/.vscode/launch.jsonc


## Debugging SConstruct scripts (subprocesses) with Visual Studio Code.

To debug the scons scripts, which are run as apio subprocesses, we use a different method or remote debugging. 
To activate, define the system env var ``APIO_SCONS_DEBUGGER`` (the value doesn't matter), run apio from the command line, and once it reports that it waits for a debugger, run the VCS ``Attach remote`` debug target to connect to the SConstruct process.


## Using the dev repository for apio commands.

You can tell pip to youse your apio dev repository for apio commands instead of the standard apio release. This allows quick edit/test cycles where you the modify code in your apio dev repository and  immediately test it by running ``apio`` commands in the console..

To use the local repo run this in the repo's root directory:
```
pip uninstall apio
pip install -e .
make
```

To return back to the release package run this (in any directory):
```
pip uninstall apio
pip install apio
```
The command ``apio system -i`` (not released yet as of Sep 2024) shows the source directory of the apio package used. For example:

```
$ apio system -i
Platform: darwin_arm64
Package:  /Users/user/projects/apio_dev/repo/apio
```

### Manage python environment with Conda

This section is a tip if you don't have python installed or you want to have independent versions of python isolated by apps or environments.
Conda is a powerful tool for this, and it is multi-platform, providing you a way to work in all operating systems in the same way.

To install Conda:

[https://docs.anaconda.com/miniconda/install/#quick-command-line-install](https://docs.anaconda.com/miniconda/install/#quick-command-line-install)

Once you installed Conda type in your shell:
```
conda create --name apio python=3.13
conda activate apio
```
After this, you could install apio like the parent section explains.