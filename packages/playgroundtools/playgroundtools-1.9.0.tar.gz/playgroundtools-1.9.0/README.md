# playgroundtools

[![PyPI](https://img.shields.io/pypi/v/playgroundtools)](https://pypi.org/project/playgroundtools/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/playgroundtools)](https://pypi.org/project/playgroundtools/)
[![Test](https://github.com/saibalusulapalem/playgroundtools/actions/workflows/test.yml/badge.svg)](https://github.com/saibalusulapalem/playgroundtools/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An interface for managing playground projects.

## Overview

This package is intended to provide a quick and easy way to set up Python "projects," each containing their own files, folders, virtual environment, and installed packages. This also includes the ability to run these projects (called **playgrounds**) and delete them. This can be done either through the CLI or through the interactive GUI (with limited capabilities). The exact configuration for the creation and execution of these playgrounds are found [here](https://github.com/saibalusulapalem/playgroundtools/blob/main/playgroundtools/config.json), in the package's configuration file.


For example, creating an `api` playground results in the following file structure:
```cmd
playground
│   .env
│   main.py
│   reset.py
│   settings.json
│
├───.venv
│       ...
│
├───api
│       config.py
│       crud.py
│       database.py
│       deps.py
│       models.py
│       schemas.py
│       __init__.py
│
└───requirements
        requirements.in
```

## Commands

`new`:
Creates a playground.
```shell
$ playground new [-h] [-i LIB [LIB ...]] [-v] -n NAME type
```
For example, to create an api project:
```shell
# We can specify a list of optional packages to install via pip by using the `-i` option
$ playground new api -n my_api -i requests -v  # verbosity can be set with the -v option
```

`run`:
Runs a playground.
```shell
$ playground run [-h] [-m MODULE] [-a ARGS [ARGS ...]] name
```
For example:
```shell
$ playground run console_app
```

`delete`:
Deletes a playground.
```shell
$ playground delete [-h] name
```
For example:
```shell
$ playground delete jupyter_tests
```

`config`:
Reads or modifies the configuration.
```shell
$ playground config [-h] [-k READ] {delete,set}
```
For example:
```shell
$ playground config set -k api.folders -v "[\"api\", \"api/routers\"]"
```

## Graphical User Interface

Invoking `playground-gui` will open the interactive GUI, allowing for the creation and deletion of playgrounds.

## Playground Settings
Settings for a playground can be configured via its `settings.json` file.
The available options are:
- `python`: a path that points to the Python installation used to run the playground.
- `module`: the module to run (by invocation of `-m {module}`)
- `args`: the arguments to pass to the module (`-m {module} {args ...}`)

## Configuration

To configure the installation of `playgroundtools`, utilize the `config` command in the CLI or manually edit the [config.json](https://github.com/saibalusulapalem/playgroundtools/blob/main/playgroundtools/config.json) file.

The available options are:
- `folders`: a list of folders that should be placed inside the playground upon creation.
- `files`: maps file names to lists containing the contents of the file by line.
- `lib`: the packages to be installed upon creation of the playground.
- `module`: the module to run when the playground is executed via `-m {module}`.
- `args`: the arguments to pass to the module upon execution (`-m {module} {args ...}`).

Keys and values can be interpolated using one of the strings below within curly brackets `{}` prepended by a `$` sign in the [config.json](https://github.com/saibalusulapalem/playgroundtools/blob/main/playgroundtools/config.json) file.
- `name`: the playground name.

### Using the CLI

`config delete`:
Deletes a key from the configuration.
```shell
$ playground config delete [-h] [-k KEY] [-f FILE]
```
For example:
```shell
$ playground config delete "package"
```
Keys from a custom config file can also be deleted:
```shell
$ playground config delete -f user_config.json
```

`config set`:
Sets a key in the configuration.
```shell
$ playground config set [-h] [-k KEY] [-v VALUE] [-f FILE]
```
For example:
```shell
$ playground config set -k "api.folders" -v "[\"api\", \"api/routers\", \"api/db\"]"
```
Configuration can also be added from a custom JSON file:
```shell
$ playground config set -f user_config.json
```

### Using JSON

The [config.json](https://github.com/saibalusulapalem/playgroundtools/blob/main/playgroundtools/config.json) file simply contains configurations for different types of playgrounds. The settings for each type are specified by the available options aforementioned.

For example, to create a `package` type, one could use:
```jsonc
{
    // ...
    "package": {
        "folders": [
            "${name}",
            "tests"
        ],
        "files": {
            "setup.cfg": [
                // File contents go here...
            ],
            "pyproject.toml": [
                // File contents go here...
            ],
            "setup.py": [
                // File contents go here...
            ]
            // ...
        },
        "lib": [
            "${name}",
            "black",
            "flake8",
            "isort",
            "build",
            "twine"
        ],
        "module": "${name}",
        "args": []
    }
}
```
