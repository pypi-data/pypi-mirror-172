from .pydantic_model import PydanticModel, Field


class SystemArg(PydanticModel):
    index: int = Field(0)
    arg: str = Field("")
    type: str = Field("")
    name: str = Field("")
    value: str = Field("")

    @classmethod
    def init(cls, kwargs: dict = None):
        result = cls(**({} if kwargs is None else kwargs))
        result.value = result.arg
        if "=" in result.arg:
            nv = result.arg.split("=", 1)
            result.name, result.value = nv[0], nv[1]
        else:
            result.name = result.arg
        return result
