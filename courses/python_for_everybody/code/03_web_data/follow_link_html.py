"""
"""

from __future__ import annotations

import argparse
from urllib3.util import Retry
import logging
import sys

try:
    import requests
    from requests.adapters import HTTPAdapter
    from requests import Session
    from bs4 import BeautifulSoup
except ImportError as e:
    sys.exit(f"Error: Missing dependency. Please install via pip.\nDetails: {e}")


DEFAULT_URL: str = "http://py4e-data.dr-chuck.net/known_by_Fikret.html"
MIN_NUMBER: int = 1

EXIT_SUCCESS: int = 0
EXIT_ERROR: int = 1
EXIT_KEYBOARD_INTERRUP: int = 130

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s : %(message)s',
)
logger = logging.getLogger(__name__)

def get_smart_session():
    # Create this once to keep the "pipe" to the server open
    #   makes script significantly faster
    session = requests.Session() 
    
    # Configure retry logic: retry 3 times, backoff (wait) between attempts
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session
                            
def _fetch_html(url: str, session: Session) -> str:  # in a function signature do not use constructor requests.Session()
    """
    """
    try:
        response = session.get(url, timeout=10)  # Faster call for each iteration
        response.raise_for_status()  # Raise an exception for HTTP errors (404, 500, etc.)
        return response.text  # Return the HTML content as a string (requests library automatically handles decoding)
    
    except requests.RequestException as e:
        logger.debug(f"Failed to fecth URL '{url}': {e}")
        raise

def input_validation(url: str, count: int, pos: int, session: Session) -> tuple(str, int, int):
    """
    """
    _fetch_html(url, session)  # confirm if argument URL works to start the program
    
    if count < MIN_NUMBER or pos < MIN_NUMBER:
        raise ValueError(
            f"One of the values '{count}' or '{pos}' is less than 1. Can't process program"
        )
        
    return url, count, pos

def crawl_links(url: str, count: int, pos: int, session: Session) -> str:
    """
    """
    for _ in range(count): # Using '_' for variables that we don't use
        # session -> Reuse the same underlying connection (TCP handshake and SSL negotiation) 
        # for every URL in your list.
        html = _fetch_html(url, session)  # fetch_html() returns the HTML content as a string
        logger.debug(f"Fetched URL {url}")
        
        soup = BeautifulSoup(html, 'html.parser')
        
        tags = soup.find_all('a')
        if not tags:
            raise ValueError(f"No <a> tags found from URL: {url}")
       
        if pos > len(tags):
           raise ValueError(f"Requested position {pos} but only {len(tags)} links found at URL: {url}")

        tag = tags[pos - 1]
        last_url = tag.get('href').strip()
        url = last_url
        
    return last_url
                     

def main(argv: str | None = None) -> int:
    """
    """
    parser = argparse.ArgumentParser(
        description="Extract URLs from <a> tags in HTML followint a Count and Position"
    )
    parser.add_argument(
        "url",  # Positional arguments are 'required' by default
        nargs="?", # Zero or one argument - if zero 'defaul' kicks in
        default=DEFAULT_URL,
        help=f"Enter URL to start crawling from (default: {DEFAULT_URL})"
    )
    parser.add_argument(
        "-c", "--count",
        type=int,  # Converts the input string to an integer automatically
        required=True,
        help=f"Enter count = how many links to fetch. Count should be > {MIN_NUMBER}"
    )
    parser.add_argument(
        "-pos", "--position", # '-x, --x' flags act like an 'optional choice', if empty argparse assignes  None
        type=int,
        required=True,  # Force for the user to provide the argument
        help=f"Enter position = What URL to fetch inside HTML. Position should be > {MIN_NUMBER}"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output"
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose enabled")
    
    url = args.url
    count_str = args.count
    pos_str = args.position    

    try:
        # 'with' block -> Context manager: it opens at the start and cleans up after itself when the script finishes
        with get_smart_session() as session:
            url, count_int, pos_int = input_validation(url, count_str, pos_str, session)
            last_url = crawl_links(url, count_int, pos_int, session)
        
    except KeyboardInterrupt:
        logger.info("Interrupet by User. Exiting")
        return EXIT_KEYBOARD_INTERRUP
    
    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        return EXIT_ERROR
    
    except ValueError as e:
        logger.error(f"Input failed: {e}")
        return EXIT_ERROR
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return EXIT_ERROR

    else:
        print(f"Last URL Retrieved: {last_url}\n")
        return EXIT_SUCCESS
    
    
if __name__ == "__main__":
    sys.exit(main())
    