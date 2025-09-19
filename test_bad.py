# test_bad.py

# 1. 사용하지 않는 변수
def unused_variable():
    a = 123  # 사용 안 함
    b = 456  # 사용 안 함
    return None

# 2. 너무 긴 함수
def long_function():
    print("start")
    for i in range(100):  # 불필요하게 긴 반복
        print("spam", i)
    print("end")

# 3. 하드코딩된 비밀번호
def hardcoded_password():
    password = "1234"  # 보안 규칙 위반
    print("Password is:", password)

# 4. 중복된 코드
def duplicate1():
    print("duplicate")
    print("duplicate")
    print("duplicate")

def duplicate2():
    print("duplicate")
    print("duplicate")
    print("duplicate")

