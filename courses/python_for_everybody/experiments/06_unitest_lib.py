import unittest

# 1. The code we want to test
def add_numbers(a, b):
    return a + b

# 2. The Test Class
class TestMathOperations(unittest.TestCase):
    
    def test_simple_addition(self):
        result = add_numbers(2, 3)
        
        self.assertEqual(result, 5)