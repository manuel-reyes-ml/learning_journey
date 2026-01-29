# Using Python´s built-in test library
import unittest
from unittest.mock import patch

from pathlib import Path
import sys

# Get the folder containing this file, in case you run the test from outside parent folder
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

# We import the function from the script
from span_number_sum import extract_numbers_from_spans, sum_span_numbers

# inheritates TestCase from unittest to use .assertEqual and others
class TestSpanParser(unittest.TestCase):
    
    def test_extract_numbers(self):
        # 1. Our fake input data
        fake_html = "<html><body><span>42</span> and <span>10</span></body></html>"
        
        # 2. Call the function (we convert the result to a list to check it easily)
        result = list(extract_numbers_from_spans(fake_html))
        
        # 3. Verify the result
        self.assertEqual(result, [42, 10])
        
class TestIntegration(unittest.TestCase):
    
    # @patch checks "span_number_sum.fetch_html" and replaces it with a Mock object
    @patch('span_number_sum.fetch_html')
    def test_sum_logic(self, mock_fetch):
        # 1. Setup the Stunt Double
        # We tell the mock: "When someone calls you, return this specific string"
        mock_fetch.return_value = "<html><span>99</span></html>"
        
        # 2. Call the main function (It uses the mock internally!)
        total = sum_span_numbers("http://fake-url.com")
        
        # 3. Verify
        # Since our fake HTML has "99", the sum should be 99.
        self.assertEqual(total, 99)
        
        # 4. Proof the Mock was used
        # We verify that our code tried to call fetch_html exactly once
        mock_fetch.assert_called_once_with("http://fake-url.com")