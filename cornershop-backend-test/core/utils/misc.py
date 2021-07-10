import json
from typing import Any, Iterable, Tuple, Union


def print_json(
    *args: Union[Iterable[Any], Iterable[Tuple[Any]]], indent: int = 4, **kwargs
) -> None:
    """Utility function to print JSON representation of Python args

    Args:
        args Union[List[str], List[Tuple[str]]]: This can be an iterable
        of anything or an iterable of tuples containing information in
        the format (title, data).
    """
    if not kwargs.get("default"):
        kwargs["default"] = str
    print("*" * 72)
    for i, arg in enumerate(args, 1):
        if isinstance(arg, Tuple) and len(arg) == 2:
            title, data = arg
        else:
            title, data = f"Argument {i}", arg
        print(title)
        print(json.dumps(data, indent=indent, **kwargs))
    print("*" * 72)
