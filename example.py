def complex_function(a, b):
    # 일부러 너무 단순하게 작성 (커버리지에서 if문 테스트 확인 가능)
    if a > b:
        return a - b
    return a + b


def no_docstring_function(a, b):
    return a * b


def unused_function(x):
    # 소나큐브에서 "사용되지 않는 코드" 이슈 잡힘
    return x / 0  # 일부러 division by zero (버그 코드)
