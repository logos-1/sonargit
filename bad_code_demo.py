import os
import sys  # Unused import

def calculate_area(radius):
    if radius < 0:
        # Problem 1: Bare Exception (S112)
        raise Exception("Radius cannot be negative")
    
    # Problem 2: Magic number
    area = 3.14159 * radius * radius
    return area

def save_data(data):
    try:
        f = open("data.txt", "w")
        f.write(data)
        # Problem 3: Forget to close the file or use 'with' statement
    except:
        # Problem 4: Empty except block (S108)
        pass

def login():
    # Problem 5: Hardcoded credentials (S2068)
    user = "admin"
    password = "supersecretpassword123"
    print(f"Logging in as {user}")

if __name__ == "__main__":
    print(calculate_area(5))
    # Problem 6: Unreachable code (if we return early, but not here)
    # Just to add more complexity for SonarCloud
