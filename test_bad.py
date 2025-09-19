# test_bad.py
# 의도적으로 소나큐브 룰 위반

import os   # 사용하지 않는 import (unused import)

PASSWORD = "123456"  # 🔥 하드코딩된 비밀번호 (보안 이슈)

def add_numbers(a, b, c, d, e, f):  # 매개변수 너무 많음 (maintainability 이슈)
    result = a + b
    return result  # c, d, e, f 사용 안 함 (unused parameter 이슈)

def dangerous_eval(user_input):
    # 🔥 eval 사용은 보안 hotspot
    return eval(user_input)

def nested_loops(x):
    total = 0
    for i in range(5):
        for j in range(5):
            if i > 0:
                if j > 0:
                    if x > 0:
                        total += i * j * x   # 불필요하게 깊은 중첩 (cognitive complexity)
    return total

def mutable_default(value, data=[]):  # 가변 디폴트 파라미터
    data.append(value)
    return data

# 중복 코드 (duplicated blocks)
def copy_paste1():
    print("copy paste")
    print("copy paste")
    print("copy paste")

def copy_paste2():
    print("copy paste")
    print("copy paste")
    print("copy paste")

try:
    1 / 0
except:   # 🔥 너무 광범위한 예외 처리 (bare except)
    pass


