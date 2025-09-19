import unittest
from example import complex_function, no_docstring_function

class TestExample(unittest.TestCase):
    def test_complex_function(self):
        self.assertEqual(complex_function(1, 2, 3), 6)
        self.assertEqual(complex_function(-1, 2, 3), 4)

    def test_no_docstring_function(self):
        self.assertEqual(no_docstring_function(3), 6)

if __name__ == '__main__':
    unittest.main()
