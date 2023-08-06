from typing import Callable
from .. import util as _util
from .pydantic_model import PydanticModel, Field


class Command(PydanticModel):
    id: str = Field("")
    description: str = Field("")
    public: str = Field("")
    private: str = Field("")
    public_command: str = Field("")
    private_command: str = Field("")

    @classmethod
    def init(cls, command: dict, config_str: Callable[[str], str]):
        if not "private" in command:
            command["private"] = command["public"]
        for key in command.keys():
            command[key] = config_str(command[key])
        result = Command(**command)
        result.private = result.private if result.private else result.public
        if not result.public_command:
            result.public_command = (
                _util.form_command(result.description, result.public)
                if result.public
                else ""
            )
        if not result.private_command:
            result.private_command = (
                _util.form_command(result.description, result.private)
                if result.private
                else ""
            )
        return result
