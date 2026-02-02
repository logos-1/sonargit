def index_out_of_bounds():
    # Noncompliant: Accessing list index out of range
    my_list = [1, 2, 3]
    return my_list[5]

def compare_to_self():
    # Noncompliant: Comparing a variable to itself
    x = 10
    if x == x:
        print("Always true")
