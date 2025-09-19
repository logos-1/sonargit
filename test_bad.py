# test_bad.py
def bad_function(a, b):
    if a == 1:
        return a + b
    if a == 2:  # 중복된 조건문 (SonarQube 이슈 발생 가능)
        return a * b
    if a == 2:  # 완전히 똑같은 조건 (Dead code)
        return a - b

    password = "123456"  # 하드코딩된 비밀번호 (보안 이슈)
    print("Debug:", a, b)  # 디버그 프린트 (Code smell)

    return None


