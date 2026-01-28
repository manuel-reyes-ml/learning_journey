"""
HTML Span Number Sum Script - Extract and sum all integers from <span> tags in HTML.

Usage:
    python span_number_sum.py [URL]
    python span_number_sum.py --verbose
"""

from __future__ import annotations
from typing import Iterator

import itertools
import re
import argparse
import logging
import sys

# Try/Except import for external dependencies
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    sys.exit(f"Error: Missing dependency. Please install via pip.\nDetails: {e}")

# Configuration
DEFAULT_URL: str = 'http://py4e-data.dr-chuck.net/comments_42.html'
# Pre-compiling regex at the module level is more efficient than compiling it on every iteration
NUMBER_PATTERN = re.compile(r'[0-9]+')  # 'r' -> raw string = no escape characters

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def fetch_html(url: str) -> str:
    """
    Fetch HTML content from a URL using urllib.
    
    Args:
        url (str): URL to fetch HTML from.
    Returns:
        str: HTML content as a decoded string.
    Raises:
        urllib.error.URLError: If URL is invalid or network error occurs.
        urllib.error.HTTPError: If HTTP error occurs (404, 500, etc.).
    """
    try:
        with requests.get(url, timeout=10) as response:
            response.raise_for_status() # Raise an exception for HTTP errors (404, 500, etc.)
    except requests.RequestException as e:
        # We log the specific error here for debugging purposes
        logger.debug(f"Failed to fetch URL {url}: {e.reason}")
        raise
    else:
        return response.text # Return the HTML content as a string (requests library automatically handles decoding)


def extract_numbers_from_spans(html: str) -> Iterator[int]:
    """
    Extract integers from all <span> tags in HTML.
    Parse HTML, find all span tags, extract text, and find numbers using regex.
    
    Args:
        html (str): HTML content as string.
    Yields:
        int: Integer extracted from span tag text.
    """
    soup = BeautifulSoup(html, 'html.parser')
    span_tags = soup.find_all('span')
    
    for span in span_tags:
        text = span.get_text(strip=True)  # strip=True removes leading and trailing whitespace automatically
        if not text:  # Skip empty spans
            continue
        
        # finditer is excellent for memory efficiency when dealing with large amounts of data
        for match in NUMBER_PATTERN.finditer(text):
            yield int(match.group())  # Use group() to get the actual matched string from match object


def sum_span_numbers(url: str) -> int:
    """
    Fetch HTML from URL, extract numbers from span tags, and compute sum.
    
    Args:
        url (str): URL to fetch HTML from.
    Returns:
        int: Sum of all integers extracted from span tags.
    Raises:
        urllib.error.URLError: If URL fetch fails.
        urllib.error.HTTPError: If HTTP error occurs.
        ValueError: If no integers found in span tags.
    """
    html = fetch_html(url) # fetch_html() returns the HTML content as a string
    numbers = extract_numbers_from_spans(html) 
    
    try:
        first = next(numbers)  # Get the first number
    except StopIteration:
        # This happens when there are no more items to iterate over
        raise ValueError(f"No integers found in span tags from URL: {url}")
    else:
        # This only runs if try block doesn't raise an exception
        return sum(itertools.chain([first], numbers))  # Put the first number in front of the rest and add them all


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the HTML span number sum script.
    
    Args:
        argv (list[str] | None, optional): Command line arguments. Defaults to None.
    Returns:
        int: Return code (0 on success, 1 on failure, 130 on keyboard interrupt).
    Raises:
        urllib.error.URLError: If URL is invalid or network error occurs.
        urllib.error.HTTPError: If HTTP error occurs.
        ValueError: If no integers found in span tags.
    """
    parser = argparse.ArgumentParser(
        description="Extract numbers from <span> tags in HTML and add them to get a total."
    )
    parser.add_argument(
        "url",
        nargs='?',
        default=DEFAULT_URL,
        help=f"URL to fetch HTML from (default: {DEFAULT_URL})"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output",
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        
    logger.info(f"Fetching data from URL: {args.url}")
    
    url = args.url
    
    try:
        total_ints = sum_span_numbers(url)
        
    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        return 1
        
    except ValueError as e:
        logger.error(f"No integers found in span tags: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Interrupted by User. Exiting.")
        return 130
    
    else:
        # This only runs if try block doesn't raise an exception
        print(f"\nTotal of integers in span tags: {total_ints}\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())  # Exit with return code from main() - more conventional than raise SystemExit(main())