import ast
import os
from typing import Callable, TypeVar

T = TypeVar("T")
NODEFAULT = object()


def getenv(
    name: str,
    *,
    default: str = NODEFAULT,
    coalesce: Callable[[str], T] = lambda value: value
) -> T:
    """ Get environment variable value, try to safety parse it and apply coalesce
        function (identity as default).
    """
    value = os.environ[name] if default is NODEFAULT else os.getenv(name, default)
    try:
        value = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        pass
    return coalesce(value)
