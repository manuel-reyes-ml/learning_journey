# Test functions using Pytest (Professional Standard)

# 1. Function to test (maybe from math.py)
def add(a, b):
    return a + b

# 2. Standalone custom function using standard Python logic for Pytest to run test
def test_add():
    # Just use 'assert'. Pytest handles the rest.
    assert add(2, 3) == 5
    

