"""
Web Crawler for Link Following.

This script connects to a starting URL, parses the HTML to find a specific
link at a given position, and follows that link. It repeats this process
for a specified count to find the "secret" URL at the end of the chain.

Usage:
    python script.py -c <count> -pos <position> [url]

Example:
    python script.py -c 7 -pos 18 http://py4e-data.dr-chuck.net/known_by_Fikret.html

Dependencies:
    - requests
    - beautifulsoup4
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
EXIT_KEYBOARD_INTERRUPT: int = 130

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s : %(message)s',
)
logger = logging.getLogger(__name__)


def get_smart_session():
    """
    Creates a requests Session with automated retry logic.

    This session is configured to handle transient network errors (like 502, 
    503, 504) by retrying the request up to 3 times with a backoff factor.
    
    Returns
    -------
    requests.Session
        A configured session object ready for making HTTP requests.
    """
    # Create this once to keep the "pipe" to the server open
    #   makes script significantly faster
    session = requests.Session() 
    
    # Configure retry logic: retry 3 times, backoff (wait) between attempts
    # Uses exponential backoff. This means it waits longer after each failure to give the server breathing room.
    # We choose these (5..) because they are usually temporary. It wouldn't make sense to retry a 404 Not Found error
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    
    # When we "mount" it, we are telling the Session: "Whenever you connect to a URL that starts with
    # https://, use this specific adapter with our custom retry rules."
    # URL: https://example.com $\rightarrow$ Matches prefix 'https://' $\rightarrow$ Uses Custom Retry Adapter
    # session.mount(prefix, adapter) - prefix: str, adapter: Object
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session
           
                            
def _fetch_html(url: str, session: Session) -> str:  # in a function signature do not use constructor requests.Session()
    """
    Fetches the HTML content from the specified URL.

    Parameters
    ----------
    url : str
        The target URL to fetch.
    session : requests.Session
        The active session object to use for the request.

    Returns
    -------
    str
        The decoded HTML content of the page.

    Raises
    ------
    requests.RequestException
        If the HTTP request fails, times out, or returns a 4xx/5xx status code.
    """
    try:
        response = session.get(url, timeout=10)  # Faster call for each iteration
        response.raise_for_status()  # Raise an exception for HTTP errors (404, 500, etc.)
        return response.text  # Return the HTML content as a string (requests library automatically handles decoding)
    
    except requests.RequestException as e:
        logger.debug(f"Failed to fecth URL '{url}': {e}")
        raise


# Use tuple[] for type definition (a tuple containing a string and integers)
# tuple() Python thinks you are trying to call the function 'tuple' with two arguments
def input_validation(url: str, count: int, pos: int, session: Session) -> tuple[str, int, int]:
    """
    Validates input arguments and checks initial connectivity.

    This function ensures the numeric arguments are within valid ranges and
    verifies that the starting URL is reachable before the main loop begins.

    Parameters
    ----------
    url : str
        The starting URL.
    count : int
        Number of times to repeat the crawl.
    pos : int
        The position of the link to follow (1-based index).
    session : requests.Session
        The active session object.

    Returns
    -------
    tuple[str, int, int]
        A tuple containing the validated (url, count, pos).

    Raises
    ------
    ValueError
        If count or pos are less than the minimum allowed value.
    requests.RequestException
        If the initial URL cannot be fetched.
    """
    _fetch_html(url, session)  # cTest fetch to confirm URL is valid/reachable
    
    if count < MIN_NUMBER or pos < MIN_NUMBER:
        raise ValueError(
            f"One of the values '{count}' or '{pos}' is less than 1. Can't process program"
        )
        
    return url, count, pos


def crawl_links(url: str, count: int, pos: int, session: Session) -> str:
    """
    Follows a chain of links for a specified number of iterations.

    For each iteration, parses the HTML, finds the link at the specified
    position, and updates the URL for the next iteration.

    Parameters
    ----------
    url : str
        The starting URL.
    count : int
        The number of links to follow.
    pos : int
        The position of the link to select on each page (1-based).
    session : requests.Session
        The persistent HTTP session.

    Returns
    -------
    str
        The URL of the final page reached after the loop completes.

    Raises
    ------
    ValueError
        If no <a> tags are found or if the requested position is out of range.
    """
    for i in range(count):
        # session -> Reuse the same underlying connection (TCP handshake and SSL negotiation) 
        # for every URL in your list.
        html = _fetch_html(url, session)  # fetch_html() returns the HTML content as a string
        logger.debug(f"Iteration {i+1}: Fetched URL {url}")
        
        soup = BeautifulSoup(html, 'html.parser')
        
        tags = soup.find_all('a')
        if not tags:
            raise ValueError(f"No <a> tags found from URL: {url}")
       
        if pos > len(tags):
           raise ValueError(f"Requested position {pos} but only {len(tags)} links found at URL: {url}")

        # Convert 1-based position to 0-based index
        tag = tags[pos - 1]
        last_url = tag.get('href', '').strip() # if no 'href' function returns None.strip() -> AttributeError since None doesn't have strip()
        url = last_url
        
    return last_url
                     

def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the script.

    Parses command line arguments, sets up logging, and executes the
    crawling logic within a safe context.

    Parameters
    ----------
    argv : list[str] | None, optional
        Command line arguments. If None, uses sys.argv.

    Returns
    -------
    int
        Exit status code (0 for success, non-zero for errors).
    """
    parser = argparse.ArgumentParser(
        description="Extract URLs from <a> tags in HTML following a Count and Position"
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
        help=f"Enter position = what URL to fetch inside HTML. Position should be > {MIN_NUMBER}"
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
    
    # args.count/position are already integers due to type=int in add_argument
    url = args.url
    count = args.count
    pos = args.position    

    try:
        # 'with' block -> Context manager: it opens at the start and cleans up after itself when the script finishes
        with get_smart_session() as session:
            url, count_v, pos_v = input_validation(url, count, pos, session)
            last_url = crawl_links(url, count_v, pos_v, session)
        
    except KeyboardInterrupt:
        logger.info("Interrupet by User. Exiting")
        return EXIT_KEYBOARD_INTERRUPT
    
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
    