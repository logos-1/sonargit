import unittest
from example import complex_function, no_docstring_function

class TestExample(unittest.TestCase):

    def test_complex_function_case1(self):
        self.assertEqual(complex_function(5, 3), 2)

    def test_complex_function_case2(self):
        self.assertEqual(complex_function(2, 5), 7)

    def test_no_docstring_function(self):
        self.assertEqual(no_docstring_function(2, 3), 6)

if __name__ == "__main__":
    unittest.main()


