class MyClass:
    def send_request(request):  # Noncompliant: the "self" parameter is missing.
        print("send_request")

class ClassWithStaticMethod:
    def static_method(param):  # Noncompliant: the "@staticmethod" decorator is missing.
        print(param)

ClassWithStaticMethod().static_method(42)  # The method is available on the instance but calling it will raise a TypeError.
