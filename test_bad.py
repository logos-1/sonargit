# 불필요한 import (사용하지 않음)
import math
import os

# 전역 변수 남발
BAD_GLOBAL = []

def insecure_function(password):
    # 하드코딩된 비밀번호 (보안 이슈)
    if password == "123456":
        print("Weak password check!")  

    # 사용하지 않는 변수
    unused_var = 42

    # 중첩 루프 (복잡도 증가)
    for i in range(10):
        for j in range(10):
            for k in range(10):
                print(i, j, k)

    # 예외를 포괄적으로 처리 (비추)
    try:
        result = 1 / 0
    except Exception as e:
        print("Something went wrong")

    # 리소스를 닫지 않음 (파일 누수 가능성)
    f = open("test.txt", "w")
    f.write("hello world")

    # SQL 인젝션 가능성 (문자열 직접 삽입)
    query = "SELECT * FROM users WHERE name = '" + password + "'"
    print(query)

    return True


def duplicate_code(a, b):
    # 중복 코드 (SonarQube가 싫어함)
    if a > b:
        return a - b
    else:
        return b - a


