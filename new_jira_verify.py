def divide_by_zero():
    # Noncompliant: Zero division raises an exception immediately
    return 1 / 0

def broad_exception():
    try:
        x = 1
    except:  # Noncompliant: Broad exception catch
        pass
