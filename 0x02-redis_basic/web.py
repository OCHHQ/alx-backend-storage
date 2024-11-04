#!/usr/bin/env python3
"""
web cache and tracker module
As the name name implies : this module implement a craching
system for fetching web pages.its tracks the number of accesses
for each URL and caches the conent for a short duration to reduce
repeated requests
"""
import requests
import redis
from typing import Callable
from functools import wraps

# connect to radis
cache = redis.Redis()


def track_access(method: Callable) -> Callable:
    """
    Here is implement a decorator to tarack numbers
    of time a URL is accessed.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        # here track the numbers of accesses
        cache.incr(f"count:{url}")
        return method(url)

    return wrapper


def cache_result(method: Callable) -> Callable:
    """
    Decorator to cache the result of fetching
    a URL for 10 seconds
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        # check if url is ready cached
        cached_content = cache.get(f"cache:{url}")
        if cached_content:
            return cached_cntent.decode("utf-8")

        # if not cached fetched the content and store within 10-seconds expiry
        content = method(url)
        cache.setx(f"cache:{url}", 10, content)
        return content

    return wrapper


@track_access
@cache_result
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL and return it
    Uses requests to fetch the content

    Args:
        url(str): The URL to fetch.
    Returns:
        str: The HTML content of the url
    """
    response = requests.get(url)
    return response.text
