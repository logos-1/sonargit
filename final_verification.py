def unused_variable_test():
    # Noncompliant: unused variable
    unused_var = "This is never used"
    return 42

def always_true_condition():
    # Noncompliant: condition is always true
    if True:
        print("This always runs")
