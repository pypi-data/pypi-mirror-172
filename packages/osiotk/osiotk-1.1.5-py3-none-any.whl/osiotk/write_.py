from . import paths as _paths
from json import dumps as _dumps


def string(
    __name: str,
    content: str,
    is_abspath: bool = False,
    errors: str = "ignore",
    encoding: str = "utf-8",
    exist_ok: bool = True,
):
    path = _paths.safepath(__name, is_abspath=is_abspath, exist_ok=exist_ok)
    with open(path, "w+", errors=errors, encoding=encoding) as file:
        file.write(content)
        file.close()


def bytes(
    __name: str,
    content: bytes,
    is_abspath: bool = False,
    errors: str = "ignore",
    encoding: str = "utf-8",
    exist_ok: bool = True,
):
    path = _paths.safepath(__name, is_abspath=is_abspath, exist_ok=exist_ok)
    with open(path, "w+", errors=errors, encoding=encoding) as file:
        file.write(content)
        file.close()


def json(
    __name: str,
    content,
    indent: int = 4,
    is_abspath: bool = False,
    exist_ok: bool = True,
):
    path = _paths.safepath(__name, is_abspath=is_abspath, exist_ok=exist_ok)
    s = _dumps(content, indent=indent)
    return string(path, content=s, is_abspath=True)


def data(
    __name: str,
    content,
    indent: int = 4,
    is_abspath: bool = False,
    errors: str = "ignore",
    encoding: str = "utf-8",
    exist_ok: bool = True,
):
    path = _paths.safepath(__name, is_abspath=is_abspath, exist_ok=exist_ok)
    if isinstance(content, str):
        result = string(
            path,
            content=content,
            is_abspath=True,
            errors=errors,
            encoding=encoding,
        )
    else:
        result = json(
            path, content=content, indent=indent, is_abspath=True, exist_ok=exist_ok
        )
    return result
