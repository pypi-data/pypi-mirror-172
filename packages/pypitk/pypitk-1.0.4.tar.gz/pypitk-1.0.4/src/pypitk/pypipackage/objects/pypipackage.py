import osiotk as _os
from ... import constants as _constants
from .. import util as _util
from .pydantic_model import PydanticModel, Field
from .config import Config
from .paths import Paths
from .content import Content
from .commands import Commands
from .system_args import SystemArgs


def _config_from_json_path(__path: str, is_abspath: bool = False):
    try:
        jsondata = _os.readjson(__path, is_abspath=is_abspath)
        result = Config.init(
            kwargs={
                subconfig.__prefix__: subconfig(kwargs=jsondata[subconfig.__prefix__])
                for subconfig in Config.__subconfigs__
            }
        )
    except BaseException:
        result = Config.init_from(__path, is_abspath=is_abspath)
    return result


def _config_from_rawpath(__config: str, system_args:SystemArgs=None,is_abspath:bool=False):
    config_path = system_args.get(_constants.VAR_BUILD_CONFIG_PATH, None)
    pypitk_config = None
    if config_path is not None:
        result = Config.init_from_pypitk_config(path=config_path.value,is_abspath=is_abspath)
        del system_args[_constants.VAR_BUILD_CONFIG_PATH]
    else:
        result = (
            Config.init(pypitk_config=pypitk_config, system_args=system_args)
            if __config is None
            else __config
        )
    return result


def _init_config(__config:Config=None,existing_config_path:str=None,system_args: SystemArgs = SystemArgs()):
    if (__config is None and existing_config_path):
        config = _config_from_json_path(existing_config_path, is_abspath=False)
    else:
        config = _config_from_rawpath(__config, system_args=system_args,is_abspath=True)
    return config


class PYPIPackage(PydanticModel):

    config: Config = Field()
    paths: Paths = Field()
    content: Content = Field()

    @classmethod
    def __init_from_config(cls, __config: Config, pypitk_config: str = ""):
        config = __config
        config_str = config.config_str
        if config is not None:
            paths = Paths.init(
                parentdir=config.package.parentdir, package_name=config.package.name
            )
            commands = Commands.init(config_str=config_str)
            content = Content.init(
                name=config.package.name,
                description=config.package.description,
                config_str=config_str,
                pypitk_config=pypitk_config,
                commands=commands,
            )
            result = cls(config=config, paths=paths, content=content, commands=commands)
        else:
            result = None
        return result

    def __post_init_package(self):
        self.config.package.name = _util.format_package_name(self.config.package.name)
        for content_path_key in _constants.FILENAMES_PACKAGE_CONTENT_PATHS:
            path = getattr(self.paths, content_path_key)
            formatted_path = _util.format_package_path(self.config.package.name, path)
            setattr(self.paths, content_path_key, formatted_path)
        self.config.package.parentdir = _util.format_package_path(
            self.config.package.name, self.config.package.parentdir
        )
        

    @classmethod
    def init(
        cls,
        __config: Config = None,
        existing_package_path: str = None,
        existing_config_path: str = None,
        system_args: SystemArgs = SystemArgs(),
    ):
        if existing_package_path:
            result = cls.init_from(existing_package_path)
        else:
            config = _init_config(__config,existing_config_path=existing_config_path,system_args=system_args)
            if isinstance(config,Config):
                result = cls.__init_from_config(config)
            else:
                print("CONFIG ERROR:",type(config))
                result = None
        if result is not None and isinstance(result,cls):
            result.__post_init_package()
        return result

        
