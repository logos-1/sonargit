# test_bad.py (추천 넣을 위치)

def insecure_password_check(password):
    if password == "123456":  # 하드코딩된 비밀번호 → 보안 이슈
        return True
    return False

def duplicate_logic(x):
    if x > 10:
        return "big"
    else:
        return "small"

def duplicate_logic_copy(x):  # 중복 코드 → Code Smell
    if x > 10:
        return "big"
    else:
        return "small"

def unused_variable_example():
    x = 100   # 사용하지 않는 변수 → 이슈
    return 42


