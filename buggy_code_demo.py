"""
This file contains intentional code quality issues for SonarCloud demonstration
"""
import os
import sys


# Issue 1: Hardcoded credentials (Security Hotspot)
DATABASE_PASSWORD = "admin123"  # Security: Hardcoded password
API_KEY = "sk-1234567890abcdef"  # Security: Hardcoded API key


# Issue 2: Unused imports and variables
import random  # Unused import
unused_variable = "This variable is never used"


# Issue 3: Too many nested if statements (Cognitive Complexity)
def complex_decision_maker(a, b, c, d, e):
    """Function with high cognitive complexity"""
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        if a > b:
                            if b > c:
                                if c > d:
                                    if d > e:
                                        return "Too deep!"
                                    else:
                                        return "Deep"
                                else:
                                    return "Nested"
                            else:
                                return "Complex"
    return "Default"


# Issue 4: Commented-out code (Code Smell)
# def old_function():
#     print("This is old code")
#     return None
# 
# def another_old_function():
#     pass


# Issue 5: Function with too many parameters (Code Smell)
def function_with_many_params(param1, param2, param3, param4, param5, 
                               param6, param7, param8, param9, param10):
    """Function with too many parameters"""
    return param1 + param2 + param3 + param4 + param5


# Issue 6: Duplicate code blocks
def calculate_total_a(items):
    total = 0
    for item in items:
        if item > 0:
            total += item
        else:
            total += 0
    return total


def calculate_total_b(items):
    total = 0
    for item in items:
        if item > 0:
            total += item
        else:
            total += 0
    return total


# Issue 7: Empty exception catch (Bug)
def risky_operation():
    try:
        result = 10 / 0
        return result
    except:  # Empty except clause - catches everything
        pass


# Issue 8: Print statements instead of logging (Code Smell)
def process_data(data):
    print("Starting data processing")  # Should use logging
    print(f"Processing {len(data)} items")
    for item in data:
        print(f"Item: {item}")
    print("Done processing")


# Issue 9: SQL Injection vulnerability (Security)
def get_user_data(username):
    """Vulnerable to SQL injection"""
    query = f"SELECT * FROM users WHERE username = '{username}'"  # SQL Injection risk
    # execute_query(query)
    return query


# Issue 10: Magic numbers (Code Smell)
def calculate_discount(price):
    if price > 100:
        return price * 0.15  # Magic number
    elif price > 50:
        return price * 0.10  # Magic number
    else:
        return price * 0.05  # Magic number


# Issue 11: Comparison to None should use 'is' (Bug)
def check_value(value):
    if value == None:  # Should use 'is None'
        return False
    return True


# Issue 12: Mutable default argument (Bug)
def append_to_list(item, my_list=[]):  # Mutable default argument
    my_list.append(item)
    return my_list


if __name__ == "__main__":
    # More hardcoded credentials
    SECRET_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
    
    print("This code has many issues!")
    # Some commented code
    # print("Another print")
    # print("Yet another print")
