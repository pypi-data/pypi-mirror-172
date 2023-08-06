from typing import Callable, Iterable, TypeVar
from json import dumps as _dumps
from dataclasses import is_dataclass, asdict as _asdict

T = TypeVar("T")


def asdict(value):
    if isinstance(value, dict):
        result = value
    elif is_dataclass(value):
        try:
            result = _asdict(value)
        except BaseException:
            result = value
    else:
        try:
            result = value.json_dict()
        except BaseException:
            result = value
    return result


def __next_where(__iter: Iterable[T], where: Callable[[T], bool], default):
    for item in iter(__iter):
        if where(item):
            result = item
            break
    else:
        result = default
    return result


def __get_by_attr(__iter: Iterable[T], match_key: str, value):
    where = lambda item: getattr(item, match_key) == value
    return __next_where(__iter, where=where, default=None)


def next_where(__iter: Iterable[T], where: Callable[[T], bool], default=None):
    return __next_where(__iter, where=where, default=default)


def get_by_attr(__iter: Iterable[T], match_key: str, value):
    return __get_by_attr(__iter, match_key=match_key, value=value)


def format_template(__template: str, keymap: dict[str, str], delimiter: str = "*"):
    result = __template
    if delimiter in __template:
        for key, value in keymap.items():
            dkey = f"{delimiter}{key}{delimiter}"
            if dkey in result:
                result = result.replace(dkey, value)
    return result


def str_is_true(__str: str) -> bool:
    return __str.lower().strip() in (
        "t",
        "tr",
        "tru",
        "true",
    )


def get_fields(__cls) -> list[str]:
    result = []
    try:
        for field_key in ("__dataclass_fields__", "__fields__"):
            result = getattr(__cls, field_key, None)
            if result is not None:
                if isinstance(result, dict):
                    result = list(result.keys())
                else:
                    result = list(result)
                break
    except BaseException:
        result = None
    return result


def arginit(__cls, **kwargs):
    result = {}
    fields = get_fields(__cls)
    if fields is not None:
        for field in fields:
            value = kwargs.get(field, None)
            result[field] = value
    return __cls(**result)


def format_packagedir(__packagedir: str, package_name: str):
    result = __packagedir
    while result.endswith("/") and len(result) > 1:
        result = result[:-1]
    result += "/"
    if not result.endswith(package_name):
        result += package_name
    if result.startswith("~"):
        result = result[1:]
    if not result.startswith("/"):
        result = "/" + result
    return result


def format_package_name(__package_name: str):
    result = __package_name
    while "/" in result:
        name = result.split("/")[-1]
        if name:
            result = name
    return result


def format_package_path(__package_name: str, path: str):
    name_error = f"/{__package_name}/{__package_name}/"
    result = path
    if name_error in path:

        while name_error in result:
            result = result.replace(name_error, f"/{__package_name}/")
        while result.endswith(f"/{__package_name}/{__package_name}"):
            result = result.removesuffix(f"/{__package_name}")
    return result


def form_command(__name: str, command: str):
    return f"# {__name.title()}:\n#    {command}"


def __indented_str(__str: str, i: int, tabsize: int):
    if __str:
        idn = ((i * tabsize) * " ") if i else ""
        result = idn + __str.lstrip()
    else:
        result = ""
    return result


def format_str(__obj, i: int = 0, tabsize: int = 4):
    try:
        result = _dumps(__obj, indent=tabsize)
    except BaseException:
        result = str(__obj)

    if i:
        result = "\n".join(
            (
                __indented_str(line, i=i, tabsize=tabsize)
                for line in result.splitlines(keepends=False)
            )
        )
    return result
