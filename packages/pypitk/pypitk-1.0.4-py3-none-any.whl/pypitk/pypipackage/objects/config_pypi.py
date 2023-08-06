from .pydantic_model import PydanticModel, Field


class PYPIConfig(PydanticModel):
    __prefix__ = "pypi"
    username: str = Field("")
    password: str = Field("")
    email: str = Field("")

    @classmethod
    def init(cls, kwargs: dict = None):
        result = cls(**({} if kwargs is None else kwargs))
        return result
