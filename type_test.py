def func(var: str):
    pass

func(42)  # Noncompliant: 42 is not of type str.

round("not a number")  # Noncompliant: the builtin function round requires a number as first parameter.
