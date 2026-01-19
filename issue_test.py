def check_value(value):
    if value < 0:
        raise BaseException("Value cannot be negative") # Noncompliant: this will be difficult for consumers to handle
