from typing import Any

def foo(arg: Any) -> Any:
    if isinstance(arg, int):
        return arg + 1
    else:
        # Noncompliant: arg could be anything other than int, e.g. None or a list, which has no upper() method.
        return arg.upper()
