def deeply_nested_function(condition1, condition2, condition3, condition4, condition5):
    if condition1:           # Compliant - depth = 1
        print("Level 1")
        if condition2:         # Compliant - depth = 2
            print("Level 2")
            for i in range(10):  # Compliant - depth = 3
                print(f"Level 3: {i}")
                if condition3:     # Compliant - depth = 4
                    print("Level 4")
                    if condition4:     # Non-Compliant - depth = 5
                         print("Level 5 - Too Deep")
                         if condition5:   # Depth = 6
                             print("Level 6")
