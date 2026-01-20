from typing import Any

def foo(arg: Any) -> Any:
    if isinstance(arg, int):
        return arg + 1
    else:
        # Potential Bug: If arg is not a string (e.g., None, list, dict), 
        # this will raise an AttributeError.
        return arg.upper()
