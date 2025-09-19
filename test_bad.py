import os, sys, math   # 미사용 import (rule 위반)

PASSWORD = "123456"  # 하드코딩된 비밀번호 (security issue)

def VeryBadFunctionName():   # PEP8 네이밍 규칙 위반
    x = 1
    y = 2
    result = x + y
    unused_variable = 123  # 사용하지 않는 변수
    print("Debug:", result)  # print 사용 (logging rule 위반)

    # 복잡한 조건식
    if x == 1 and y == 2 or x == 3 and not (y == 4):
        print("Complex condition")

    try:
        risky = 10 / 0   # ZeroDivisionError
    except:
        pass   # broad exception, 아무 처리 안함 (rule 위반)

    if {'a':1}.has_key('a'):  # Python3에서 제거된 메서드 (deprecated)
        print("Should not happen")

    return result


class BadClass:
    def method(self):
        print("This is a bad class")  # print 사용


def unused_function():   # 호출되지 않는 함수
    secret = "hardcoded_api_key=XYZ123"  # 하드코딩된 비밀정보
    return secret

