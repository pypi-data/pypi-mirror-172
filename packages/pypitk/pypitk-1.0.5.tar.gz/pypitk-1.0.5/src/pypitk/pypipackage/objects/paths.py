import osiotk as os
from .. import util as _util
from ... import constants as _constants
from .pydantic_model import PydanticModel, Field


class Paths(PydanticModel):

    pyproject_toml: str = Field("")
    readme: str = Field("")
    private: str = Field("")
    pypitk_config: str = Field("")

    @classmethod
    def init(cls, parentdir: str, package_name: str):
        parentdir = _util.format_package_path(package_name, path=parentdir)

        joinpath = lambda __name: _util.format_package_path(
            package_name, os.join_paths(parentdir, __name)
        )
        pyproject_toml = joinpath(_constants.FILENAME_PYPROJECT_TOML)
        readme = joinpath(_constants.FILENAME_README)
        private = joinpath(_constants.FILENAME_PRIVATE)
        pypitk_config = joinpath(_constants.FILENAME_PYPITK_CONFIG)
        return cls(
            pyproject_toml=pyproject_toml,
            readme=readme,
            private=private,
            pypitk_config=pypitk_config,
        )
