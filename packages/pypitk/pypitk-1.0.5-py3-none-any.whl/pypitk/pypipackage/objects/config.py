from collections import defaultdict
import osiotk as _os
from . import config_src
from .. import util as _util
from .. import cli as _cli
from ... import constants as _constants
from .config_build import BuildConfig
from .config_package import PackageConfig
from .config_pypi import PYPIConfig
from . import config_parser as _config_parser
from .system_args import SystemArgs
from .pydantic_model import PydanticModel, Field


class Config(PydanticModel):

    package: PackageConfig = Field()
    pypi: PYPIConfig = Field()
    build: BuildConfig = Field()

    __subconfigs__ = (PackageConfig, PYPIConfig, BuildConfig)

    def __getitem__(self, key):
        return getattr(self, key)

    def json(self):
        return {
            subconfig.__prefix__: getattr(self, subconfig.__prefix__).json_dict()
            for subconfig in self.__class__.__subconfigs__
        }

    def __str__(self):
        return _util.format_str(self.json())

    def __contains__(self, key):
        return True if self[key] else False

    def __setitem__(self, __key, value):
        setattr(self, __key, value)

    def items(self):
        for subconfig in (self.package, self.pypi, self.build):
            for key, value in _util.asdict(subconfig).items():
                if not key in ("subdir_structure",):
                    yield (key, value)

    def config_str(self, __str: str):
        return _config_parser.config_str(self, __str)

    @classmethod
    def fields(cls):
        fields = []
        for subclass in cls.__subconfigs__:
            subclass_fields = _util.get_fields(subclass)
            if subclass_fields is not None:
                fields.extend(subclass_fields)
        return fields

    @classmethod
    def init_from_pypitk_config(cls,path:str="",src:str="",is_abspath:bool=False):
        subconfigs = (BuildConfig,PackageConfig,PYPIConfig)
        varlines = config_src.parse(path=path,src=src,is_abspath=is_abspath)
        unknowns = set()
        varline_map = {varline.key:varline for varline in varlines}
        results = defaultdict(dict[str,str])
        for varline in varlines:
            if varline.parent:
                results[varline.parent][varline.key] = varline.value
            else:
                unknowns.add(varline.key)
        for key in unknowns:
            varline = varline_map[key]
            found = False
            for subconfig in subconfigs:
                if found is None and key in subconfig.fields():
                    value = varline.value
                    found = True
                    results[subconfig.__prefix__][key] = value
        for subconfig in subconfigs:
            kwargs = results.get(subconfig.__prefix__,None)
            results[subconfig.__prefix__] = subconfig.init(kwargs=kwargs)
        result = cls.init(kwargs=results)
        return result
                


    @classmethod
    def init(
        cls,
        kwargs: dict = None,
        src_path: str = None,
        pypitk_config: str = None,
        system_args: SystemArgs = None,
    ):
    
        if kwargs:
            config = cls(**kwargs)
        elif src_path is not None:
            config = cls.init_from(src_path, is_abspath=True)
        else:
            config = {}
            if pypitk_config is not None and pypitk_config:
                config = _config_parser.parse_config(cls, src=pypitk_config)
            else:
                config = {
                    subconfig.__prefix__: _config_parser.parse_subconfig(
                        subconfig, system_args=system_args
                    )
                    for subconfig in cls.__subconfigs__
                }
            if _cli.approve_config_kwargs(config) != "y":
                config = None
        if config is None or not config:
            result = None
        else:
            result = config if isinstance(config, cls) else cls(**config)
            result.build.subdir_structure = result.config_str(
                _constants.SUBDIR_STRUCTURE
            )
            result.package.parentdir = _util.format_package_path(
                result.package.name, result.package.parentdir
            )
        return result
