#!/usr/bin/env python3
"""
Module for implementing a web caching and tracking system using Redis.
"""
import requests
import redis
from functools import wraps
from typing import Callable


def count_access(method: Callable) -> Callable:
    """Decorator to count URL accesses"""
    @wraps(method)
    def wrapper(url: str) -> str:
        r = redis.Redis()
        r.incr(f"count:{url}")
        return method(url)
    return wrapper


def cache_page(method: Callable) -> Callable:
    """Decorator to cache page content"""
    @wraps(method)
    def wrapper(url: str) -> str:
        r = redis.Redis()
        # Check if content is cached
        cached = r.get(f"cached:{url}")
        if cached:
            return cached.decode('utf-8')
        # Get and cache content if not found
        html = method(url)
        r.setex(f"cached:{url}", 10, html)
        return html
    return wrapper


@count_access
@cache_page
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL and implement caching and access tracking.
    Args:
        url (str): The URL to fetch
    Returns:
        str: The HTML content of the page
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Example usage with slowwly
    url = ("http://slowwly.robertomurray.co.uk/delay/3000/url/"
           "http://www.google.com")
    # First call - should be slow
    print(get_page(url))
    print(f"Count: {redis.Redis().get(f'count:{url}')}")
    # Second call should be fast (cached)
    print(get_page(url))
    print(f"Count: {redis.Redis().get(f'count:{url}')}")
