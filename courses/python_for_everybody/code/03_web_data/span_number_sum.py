"""
HTML Span Number Sum Script - Extract and sum all integers from <span> tags in HTML.

Usage:
    python span_number_sum.py
    python span_number_sum.py http://py4e-data.dr-chuck.net/comments_42.html
    python span_number_sum.py http://py4e-data.dr-chuck.net/comments_2357632.html
"""

from __future__ import annotations
from typing import Iterator

import itertools
import re
import argparse
import sys
import urllib.request
import urllib.error
from bs4 import BeautifulSoup

DEFAULT_URL: str = 'http://py4e-data.dr-chuck.net/comments_42.html'
NUMBER_PATTERN: str = r'[0-9]+'  # 'r' -> raw string = no escape characters


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
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
            return html
    except urllib.error.URLError as e:
        raise urllib.error.URLError(f"Failed to fetch URL {url}: {e.reason}") from e
    except urllib.error.HTTPError as e:
        raise urllib.error.HTTPError(
            url, e.code, f"HTTP error {e.code}: {e.reason}", e.headers, None
        ) from e


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
    
    pattern = re.compile(NUMBER_PATTERN)  # Compile regex pattern for better performance
    
    for span in span_tags:
        text = span.get_text()  # Get text content from span tag
        if text.strip() == '':  # Skip empty spans
            continue
        for match in pattern.finditer(text.strip()):  # Use finditer() to yield one by one
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
    args = parser.parse_args(argv)
    
    url = args.url
    
    try:
        total_ints = sum_span_numbers(url)
        
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
        
    except KeyboardInterrupt:
        print("\nInterrupted by User. Exiting.\n", file=sys.stderr)
        return 130
    
    else:
        # This only runs if try block doesn't raise an exception
        print(f"\nTotal of integers in span tags: {total_ints}\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())  # Exit with return code from main() - more conventional than raise SystemExit(main())
