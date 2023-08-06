import sys as _sys
from typing import List
from .system_arg import SystemArg


class SystemArgs(dict[str, SystemArg]):
    def list(self, reverse: bool = False):
        result = list(self.values())
        result.sort(key=lambda system_arg: system_arg.index, reverse=reverse)
        return result

    def index(self, i: int):
        return self.list()[i]

    @classmethod
    def init(cls, args: List[str] = None):
        argv = _sys.argv if args is None else args
        return cls(
            {
                system_arg.name: system_arg
                for system_arg in (
                    SystemArg.init(kwargs=dict(index=index, arg=arg))
                    for (index, arg) in enumerate(argv)
                )
                if system_arg.name
            }
        )

    def __iter__(self):
        return iter(self.values())
