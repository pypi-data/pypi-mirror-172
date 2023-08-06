import osiotk as os
from .. import util as _util
from .. import cli as _cli
from ... import constants as _constants
from .system_arg import SystemArg


def __iter_config_kwargs(__src: str):
    for line in __src.splitlines(keepends=False):
        if "=" in line:
            kv = line.split("=", 1)
            yield (kv[0].strip(), kv[1].lstrip())


def parse_config_kwargs(__src: str):
    return {arg: value for (arg, value) in __iter_config_kwargs(__src)}


def config_str(__config, __str: str):
    result = str(__str)
    if "*" in result:
        for (key, value) in __config.items():
            formatted_value = str(value) if isinstance(value, bool) else value
            result = result.replace(f"*{key}*", formatted_value)
    return result


def parse_subconfig(
    __subconfig,
    kwargs: dict[str, str] = {},
    config: dict[str, dict[str, str]] = None,
    system_args: dict[str, SystemArg] = None,
):
    prefix = __subconfig.__prefix__
    config_keys = _util.get_fields(__subconfig)
    result = {config_key: None for config_key in config_keys}
    if config is not None:
        result = config[prefix].copy()
    if system_args is not None:
        missing_keys = (
            key
            for key in config_keys
            if result.get(key, None) is None and system_args.get(key,None) is None
        )
        print("missing keys:",list(missing_keys))
        for key in missing_keys:
            user_value = _cli.get_config_input(prefix=prefix, config_key=key)
            value = None if user_value is None else user_value
            result[key] = value

    else:
        defaults = _constants.CONFIG_DEFAULTS[prefix]
        for config_key in config_keys:
            value = kwargs.get(config_key)
            if value is None:
                for joiner in ("_", "."):
                    value = kwargs.get(prefix + joiner + config_key)
                    if value is not None:
                        result[config_key] = value
                        break
                if value is None:
                    result[config_key] = defaults.get(config_key)
            else:
                result[config_key] = value
    return result


def parse_config(__config_cls, src: str, is_path: bool = False):
    config_str = os.reads(src, is_abspath=False) if is_path else src
    kwargs = parse_config_kwargs(config_str)
    subconfigs = {
        subconfig.__prefix__: subconfig.init(
            kwargs=parse_subconfig(subconfig, kwargs=kwargs)
        )
        for subconfig in __config_cls.__subconfigs__
    }

    return __config_cls(**subconfigs)
