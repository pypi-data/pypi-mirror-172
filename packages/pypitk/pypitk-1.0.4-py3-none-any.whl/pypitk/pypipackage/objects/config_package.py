from .. import util as _util
from .pydantic_model import PydanticModel, Field


class PackageConfig(PydanticModel):

    __prefix__ = "package"
    name: str = Field("")
    parentdir: str = Field("")
    version: str = Field("")
    description: str = Field("")
    python_version: str = Field("")
    license: str = Field("")

    @classmethod
    def init(cls, kwargs: dict = None):
        result = cls(**({} if kwargs is None else kwargs))
        result.parentdir = _util.format_packagedir(result.parentdir, result.name)
        return result

    
