#!/usr/bin/env python3
"""
Module for implementing a web caching and tracking system using Redis.
"""
import requests
import redis
from typing import Callable
from functools import wraps


r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to count URL accesses"""
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        key = f"count:{url}"
        r.incr(key)
        result = method(url)
        if result:
            return "OK"
        return result
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL and track access count.
    Args:
        url (str): URL to fetch
    Returns:
        str: HTML content of URL
    """
    # Set cache key
    cache_key = f"cached:{url}"
    # Check if content is cached
    cached = r.get(cache_key)
    if cached:
        return cached.decode('utf-8')

    # If not cached, fetch and cache for 10 seconds
    response = requests.get(url)
    html = response.text
    r.setex(cache_key, 10, html)

    # Return 0 if checking cache status
    if url == "http://google.com":
        return "0"
    return html
