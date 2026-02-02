import os
import json # Noncompliant: unused import

def check_complexity(value):
    # Noncompliant: Cognitive Complexity is too high
    if value < 0:
        if value > -10:
            if value != -5:
                if value != -4:
                    print("Deep nesting")
                    
def security_test():
    password = "secret_password_123" # Noncompliant: Hardcoded password
    print(password)
