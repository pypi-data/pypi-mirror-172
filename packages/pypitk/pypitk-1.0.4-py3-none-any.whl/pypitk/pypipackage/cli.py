from .. import constants
from . import util as _util


def __get_input(__message:str=""):
    try:
        result = input(__message)
    except BaseException:
        result = ""
    if not isinstance(result,str):
        result = ""
    return result

def get_config_input(prefix: str, config_key):
    value = constants.CONFIG_DEFAULTS[prefix][config_key]
    message = f"Enter value for {config_key}:: (default_value = {value})\n:"
    user_value = __get_input(message)
    return user_value if user_value else None


def emit_process_update(__message: str):
    print(f"PROCESS: {__message}")


def approve_config_kwargs(__config: dict):
    config_str = _util.format_str(__config)
    message = f"\nBuilding package with config:\n\n{config_str}\n\ncontinue? (y/n)\n:"
    result = __get_input(message).lower()
    if not isinstance(result,str) or not result:
        result = "y"
    return result
