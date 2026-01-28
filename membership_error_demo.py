"""
SonarCloud Detection Demo: Membership protocol errors
Rule: python:S3403 (Membership tests should not be performed on "non-container" objects)
"""

# Case 1: Integer membership test
def check_int_membership():
    myint = 42
    # This raises TypeError at runtime because 'int' is not iterable
    if 42 in myint:
        print("This will never print and crash before reaching here")

# Case 2: Custom class without __contains__, __iter__, or __getitem__
class A:
    def __init__(self, values):
        self._values = values
    
    # Missing __contains__ or __iter__ methods

def check_class_membership():
    # This also raises TypeError
    if "mystring" in A(["mystring"]):
        print("Found it")

if __name__ == "__main__":
    check_int_membership()
    check_class_membership()
