from typing import Callable
from .. import util as _util
from ... import constants as _constants
from .commands import Commands
from .pydantic_model import PydanticModel, Field


class Content(PydanticModel):

    readme: str = Field("")
    pyproject_toml: str = Field("")
    private: str = Field("")
    pypitk_config: str = Field("")
    private_install_locally_command: str = Field("")

    @classmethod
    def init(
        cls,
        name: str,
        description: str,
        pypitk_config: str,
        config_str: Callable[[str], str],
        commands: Commands,
    ):
        pyproject_toml = config_str(_constants.TEMPLATE_PYPROJECT_TOML)
        values = {
            "name": name.title(),
            "description": description,
            "commands": "\n\n".join(commands.public_commands),
        }

        readme = _util.format_template(_constants.TEMPLATE_README, values)
        private = _util.format_template(
            _constants.TEMPLATE_PRIVATE_COMMANDS,
            values,
        )

        build_public_install_private = commands.build_publish_install.private

        return cls(
            readme=readme,
            pyproject_toml=pyproject_toml,
            private=private,
            private_install_locally_command=build_public_install_private,
            pypitk_config=pypitk_config,
        )
