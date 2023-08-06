
from .pypipackage.objects import pypipackage_builder as _package_builder
from .pypipackage.objects import pypipackage_updater as _package_updater
from .pypipackage.objects.system_args import SystemArgs
from . import constants as _constants

def __get_task(__system_args: SystemArgs,default:str="create"):
    return next(
        (arg.name for arg in __system_args if arg.name in _constants.CLI_COMMANDS),
        default,
    )

def parse_input(__system_args: SystemArgs = None):
    system_args = SystemArgs.init() if __system_args is None else __system_args
    task = __get_task(system_args)
    if task == "create":
        _package_builder.build_package(system_args)
    elif task == "update":
        _package_updater.update_package(system_args)
    elif task == "help":
        print("task=help")
