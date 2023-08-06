from . import base as _base
from typing import Callable
from json import loads as _loads

def __or_none(func):
    def inner(*a,**b):
        try:
            result = func(*a,**b)
        except Exception:
            result = None
        return result
    return inner

@__or_none
def string(__name: str, is_abspath: bool = False):
    path = _base.abspath(__name, is_abspath)
    result = None
    with open(path, mode="r") as file:
        result = str(file.read())
    return result

@__or_none
def bytes(__name: str, is_abspath: bool = False):
    path = _base.abspath(__name, is_abspath)
    with open(path, mode="rb") as file:
        result = file.read()
    return result

@__or_none
def json(__name: str, is_abspath: bool = False):
    return _loads(string(__name, is_abspath=is_abspath))

@__or_none
def lines(
    __name: str,
    is_abspath: bool = False,
    keepends: bool = False,
    where: Callable[[str], bool] = None,
):
    s = string(__name, is_abspath)
    result = s.splitlines(keepends=keepends)
    if where is not None:
        result = [line for line in result if where(line)]
    return result
