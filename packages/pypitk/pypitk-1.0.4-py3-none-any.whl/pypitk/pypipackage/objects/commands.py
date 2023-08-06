from typing import Callable
from ... import constants as _constants
from .. import util as _util
from .pydantic_model import PydanticModel, Field
from .command import Command


class Commands(PydanticModel):

    install_poetry: Command = Field()
    build_package: Command = Field()
    publish_package: Command = Field()
    install_package: Command = Field()
    build_publish: Command = Field()
    build_publish_install: Command = Field()
    test: Command = Field()

    @classmethod
    def init(cls, config_str: Callable[[str], str]):
        result = {}
        for command in _constants.COMMAND_TEMPLATES.copy():
            command = Command.init(command=command, config_str=config_str)
            result[command.id] = command
        result = cls(**result)
        return result

    def __iter__(self):
        return (getattr(self, key) for key in _util.get_fields(self.__class__))

    @property
    def commands(self) -> list[Command]:
        return list(self)

    @property
    def public_commands(self) -> list[str]:
        return [
            command.public_command
            for command in self.commands
            if command.public_command
        ]

    @property
    def private_commands(self) -> list[str]:
        return [
            command.private_command
            for command in self.commands
            if command.private_command
        ]
