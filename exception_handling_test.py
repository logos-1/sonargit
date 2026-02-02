def exception_handling_test():
    """Test various non-compliant exception handling patterns"""
    
    try:
        # Some operation
        result = 1 + 1
    except SystemExit:  # Noncompliant: the SystemExit exception is not re-raised.
        pass

    try:
        # Another operation
        value = 42
    except BaseException:  # Noncompliant: BaseExceptions encompass SystemExit exceptions and should be re-raised.
        pass

    try:
        # Yet another operation
        data = "test"
    except:  # Noncompliant: exceptions caught by this statement should be re-raised or a more specific exception should be caught.
        pass
