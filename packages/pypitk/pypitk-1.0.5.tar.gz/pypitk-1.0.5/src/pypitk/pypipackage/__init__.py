from .objects.config import Config
from .objects.paths import Paths
from .objects.content import Content
from .objects.commands import Commands
from .objects.pydantic_model import PydanticModel, Field


class PYPIPackage(PydanticModel):

    config: Config = Field()
    paths: Paths = Field()
    content: Content = Field()
    commands: Commands = Field()

    @classmethod
    def init(cls, __config: Config, pypitk_config: str = ""):
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
            return cls(config=config, paths=paths, content=content, commands=commands)
