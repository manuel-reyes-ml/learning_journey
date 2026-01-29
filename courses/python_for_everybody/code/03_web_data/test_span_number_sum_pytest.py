from unittest.mock import patch

from span_number_sum import extract_numbers_from_spans, sum_span_numbers

def test_extract_numbers():
    # 1. Our fake input data
    fake_html = "<html><body><span>42</span> and <span>10</span></body></html>"
        
    # 2. Call the function (we convert the result to a list to check it easily)
    result = list(extract_numbers_from_spans(fake_html))
        
    # 3. Verify the result
    assert result == [42, 10]

# @patch checks "span_number_sum.fetch_html" and replaces it with a Mock object
@patch('span_number_sum.fetch_html')
def test_sum_logic(mock_fetch):
    # 1. Setup the mock
    # We tell the mock: "When someone calls you, return this specific string"
    mock_fetch.return_value = "<html><span>99</span></html>"
        
    # 2. Call the real function (It uses the mock internally!)
    total = sum_span_numbers("http://fake-url.com")
        
    # 3. Verify
    # Since our fake HTML has "99", the sum should be 99.
    assert total == 99
        
    # 4. Proof the Mock was used
    # We verify that our code tried to call fetch_html exactly once
    mock_fetch.assert_called_once_with("http://fake-url.com")