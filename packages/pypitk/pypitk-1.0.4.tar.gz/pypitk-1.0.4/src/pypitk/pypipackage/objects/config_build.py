from .. import util as _util
from .pydantic_model import PydanticModel, Field


class BuildConfig(PydanticModel):
    __prefix__ = "build"

    autoinstall: bool = Field(False)
    subdir_structure: str = Field("")
    build_files: bool = Field(True)

    @classmethod
    def init(cls, kwargs: dict = None):
        if kwargs is not None:
            result = cls(
                **{key: "" if value is None else value for key, value in kwargs.items()}
            )
        else:
            result = cls()
        if isinstance(result.autoinstall, str):
            result.autoinstall = _util.str_is_true(result.autoinstall)
        if isinstance(result.build_files, str):
            result.build_files = _util.str_is_true(result.build_files)
        return result
