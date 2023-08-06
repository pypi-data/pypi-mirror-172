import osiotk as _os
from .pydantic_model import PydanticModel,Field

def _key_parent(key:str):
    parts = None
    for delim in ("_","."):
        if delim in key:
            parts == key.split(delim,1)
            break
    if parts is None:
        parts = [key,""]
    return parts[0],parts[1]

    
    

class VarLine(PydanticModel):

    key:str = Field("")
    parent:str = Field("")
    value:str = Field("")
    is_varline:bool = Field(False)

    @classmethod
    def init(cls,line:str):

        if "=" in line:
            kv = line.split("=",1)
            key = kv[0].strip()
            value = kv[1].lstrip()
            key,parent = _key_parent(key=key)
            result = cls(key=key,value=value,parent=parent,is_varline=True)
        else:
            result = cls()
        return result


def parse(path:str="",src:str="",is_abspath:bool=False):
    src = src if src else _os.reads(path,is_abspath=is_abspath) if path else None
    varlines = [VarLine.init(line=line) for line in src.splitlines(keepends=False)]
    return [varline for varline in varlines if varline.is_varline]


    