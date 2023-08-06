# azcam-scripts

*azcam-scripts* is an *azcam* extension which adds general purpose scripting. These scripts are intended for command line use. Other azcam extensions may required to be installed for proper operation, depending on the script.

## Installation

`pip install azcam-scripts`

Or download from github: https://github.com/mplesser/azcam-scripts.git.

## Usage

Use `from azcam_scripts import xxx` to import module `xxx`. Scripts may then be executed by name as `xxx.xxx(10)`, for example, `get_temperatures.get_temperatures(10)`. A shortcut could be similar to `from azcam_scripts.get_temperatures import get_temperatures` and then execute with `get_temperatures(10)`.

In some cases the environment configuration process may bring all the script functions directly to the command line namespace. This is usually accomplished using the `azcam_scripts.load()` command.  In this case, use just `get_temperaturess(10, "templog.txt", 0)`.
