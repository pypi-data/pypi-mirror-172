import osiotk as _os
from pydantic import BaseModel, Field


class PydanticModel(BaseModel):
    @classmethod
    def fields(cls):
        return iter(cls.__fields__.keys())

    def __json(self, indent: int = 4):
        return self.json(indent=indent)

    def json_dict(self):
        result = {}
        for field_id in self.__class__.__fields__.keys():
            value = getattr(self, field_id)
            if isinstance(value, PydanticModel):
                value = value.json_dict()
            result[field_id] = value
        return result

    @classmethod
    def save(cls, value, path: str, is_abspath: bool = False, indent: int = 4):
        if isinstance(value, cls):
            content = value.__json(indent=indent)
            _os.writes(path, content=content, is_abspath=is_abspath)

    def save_to(self, __path: str, is_abspath: bool = False, indent: int = 4):
        return self.__class__.save(
            value=self, path=__path, is_abspath=is_abspath, indent=indent
        )

    @classmethod
    def init_from(cls, __path: str, is_abspath: bool = False):
        path = _os.abspath(__path, is_abspath=is_abspath)
        response = cls.parse_file(path=path)
        return response

    def __str__(self):
        return self.__json(indent=4)
