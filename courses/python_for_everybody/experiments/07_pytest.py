# Test functions using Pytest (Professional Standard)

# 1. Function to test (maybe from math.py)
def add(a, b):
    return a + b

# 2. Standalone custom function using standard Python logic for Pytest to run test
def test_add():
    # Just use 'assert'. Pytest handles the rest.
    assert add(2, 3) == 5
    
# 3. Import Pytest library to use parametrize
import pytest

# 4.  Generate 4 tests with different inputs and expected values
@pytest.mark.parametrize("input_a, input_b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_scenarios(input_a, input_b, expected):
    assert add(input_a, input_b) == expected
    
# 5. Use pytest.param to identify each test in the output (include -v, --verbose in CLI)
@pytest.mark.parametrize("input_a, input_b, expected", [
    pytest.param(2, 3, 5, id="positive_numbers"),
    pytest.param(0, 0, 0, id="zeros"),
    pytest.param(-1, 1, 0, id="negative_plus_positive"),
    pytest.param(100, 200, 300, id="large_numbers"),
])
def test_add_scenarios_param(input_a, input_b, expected):
    assert add(input_a, input_b) == expected    