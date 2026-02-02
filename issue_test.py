def exception_test():
    try:
        pass
    except SystemExit:  # Noncompliant: the SystemExit exception is not re-raised.
        pass

    try:
        pass
    except BaseException:  # Noncompliant: BaseExceptions encompass SystemExit exceptions and should be re-raised.
        pass

    try:
        pass
    except:  # Noncompliant: exceptions caught by this statement should be re-raised or a more specific exception should be caught.
        pass

def buggy_function():
    # Noncompliant: The 'pass' statement in this loop does nothing.
    for i in range(10):
        pass

def buggy_function():
    # Noncompliant: The 'pass' statement in this loop does nothing.
    for i in range(10):
        pass
