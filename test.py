# 너무 긴 함수, 복잡도 높음, 사용하지 않는 변수, 불필요한 주석 포함

def complex_function(a, b, c):
    # 불필요한 주석
    result = 0
    unused_var = 42
    if a > 0:
        if b > 0:
            if c > 0:
                result = a + b + c
            else:
                result = a + b - c
        else:
            result = a - b + c
    else:
        if b > 0:
            result = -a + b + c
        else:
            result = -a - b + c
    return result

def no_docstring_function(x):
    return x * 2
