VAR_PACKAGE_NAME = "name"
VAR_PACKAGE_DESCRIPTION = "description"
VAR_PACKAGE_VERSION = "version"
VAR_PACKAGE_DIR = "package_dir"
VAR_PACKAGE_LICENSE = "license"
VAR_PACKAGE_PYTHON_VERSION = "python_version"

VAR_BUILD_AUTOINSTALL = "autoinstall"
VAR_BUILD_CONFIG_PATH = "config_path"
VAR_BUILD_BUILD_FILES = "build_files"
VAR_PYPI_USERNAME = "username"
VAR_PYPI_EMAIL = "email"
VAR_PYPI_PASSWORD = "password"

FILENAME_PYPROJECT_TOML = "pyproject.toml"
FILENAME_README = "README.md"
FILENAME_PRIVATE = "private.txt"
FILENAME_PYPITK_CONFIG = "pypitk_config.json"

FILENAMES_PACKAGE_CONTENT_PATHS = (
    "pyproject_toml",
    "readme",
    "private",
    "pypitk_config",
)
SUBDIR_STRUCTURE = f"""
pyproject.toml
MANIFEST.in
README.md
tests
    __init__.py
    test_*{VAR_PACKAGE_NAME}*.py
src
    __init__.py
    *{VAR_PACKAGE_NAME}*
        __init__.py
"""

TEMPLATE_README = """
## *name*

## Description:

    *description*

## Commands:

*commands*

"""

TEMPLATE_PRIVATE_COMMANDS = """
## Commands:

*commands*
"""


TEMPLATE_PYPROJECT_TOML = f"""
[tool.poetry]
name = "*{VAR_PACKAGE_NAME}*"
version = "*{VAR_PACKAGE_VERSION}*"
description = "*{VAR_PACKAGE_DESCRIPTION}*"
authors = ["*{VAR_PYPI_USERNAME}* <*{VAR_PYPI_EMAIL}*>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^*{VAR_PACKAGE_PYTHON_VERSION}*"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
COMMAND_BUILD_PUBLIC = "python3 -m poetry build"
COMMAND_INSTALL_PUBLIC = (
    f"python3 -m pip install *{VAR_PACKAGE_NAME}*==*{VAR_PACKAGE_VERSION}*"
)
COMMAND_PUBLISH_PUBLIC = "python3 -m poetry publish -u <username> -p <password>"
COMMAND_PUBLISH_PRIVATE = (
    f"python3 -m poetry publish -u *{VAR_PYPI_USERNAME}* -p *{VAR_PYPI_PASSWORD}*"
)
COMMAND_TEMPLATES = [
    {
        "id": "install_poetry",
        "description": "install poetry",
        "public": "python3 -m pip install poetry",
    },
    {
        "id": "build_package",
        "description": "build package",
        "public": COMMAND_BUILD_PUBLIC,
    },
    {
        "id": "publish_package",
        "description": "publish package",
        "public": COMMAND_PUBLISH_PUBLIC,
        "private": COMMAND_PUBLISH_PRIVATE,
    },
    {
        "id": "install_package",
        "description": "install package locally",
        "public": COMMAND_INSTALL_PUBLIC,
    },
    {
        "id": "build_publish",
        "description": "build and publish package",
        "public": f"{COMMAND_BUILD_PUBLIC};{COMMAND_PUBLISH_PUBLIC}",
        "private": f"{COMMAND_BUILD_PUBLIC};{COMMAND_PUBLISH_PRIVATE}",
    },
    {
        "id": "build_publish_install",
        "description": "build package; publish package; install package",
        "public": f"{COMMAND_BUILD_PUBLIC};{COMMAND_PUBLISH_PUBLIC};{COMMAND_INSTALL_PUBLIC}",
        "private": f"{COMMAND_BUILD_PUBLIC};{COMMAND_PUBLISH_PRIVATE};{COMMAND_INSTALL_PUBLIC}",
    },
    {
        "id": "test",
        "description": f"test *{VAR_PACKAGE_NAME}*",
        "public": "python3 -m pytest -rpP tests/",
    },
]


CONFIG_DEFAULTS = {
    "package": {
        VAR_PACKAGE_NAME: "pypi_package_defaultname",
        VAR_PACKAGE_VERSION: "1.0.0",
        VAR_PACKAGE_DESCRIPTION: "package_description",
        VAR_PACKAGE_PYTHON_VERSION: "3.7",
        VAR_PACKAGE_DIR: "/documents/pypi_packages/",
        VAR_PACKAGE_LICENSE: "MIT",
    },
    "pypi": {
        VAR_PYPI_USERNAME: "pypi_username",
        VAR_PYPI_PASSWORD: "pypi_password",
        VAR_PYPI_EMAIL: "pypi_email",
    },
    "build": {VAR_BUILD_AUTOINSTALL: "false", VAR_BUILD_BUILD_FILES: "true"},
}


CLI_COMMANDS = {"create", "update", "help"}

CLI_ENTRY_OPTIONS_PROMPT = """

    1. create
        description:
            create new package package

    2. update:
        description:
            update existing package

"""

CLI_HELP_PROMPT = """

"""

CLI_ENTRY_PROMPT = """

"""
