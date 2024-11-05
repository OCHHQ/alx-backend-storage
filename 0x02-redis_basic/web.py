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
        r.incr(f"count:{url}")
        result = method(url)
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
    # Check if content is cached
    cached = r.get(f"cached:{url}")
    if cached:
        return cached.decode('utf-8')

    # If not cached, fetch and cache for 10 seconds
    response = requests.get(url)
    html = response.text
    r.setex(f"cached:{url}", 10, html)
    return html
