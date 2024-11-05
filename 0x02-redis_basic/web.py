#!/usr/bin/env python3
"""
Module for implementing a web caching and tracking system using Redis.
"""
import requests
import redis
from typing import Callable
from functools import wraps


redis_client = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to count URL accesses"""
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        redis_client.incr(f"count:{url}")
        return method(url)
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
    cache_key = f"cache:{url}"
    count_key = f"count:{url}"

    # Return count for tracking
    if redis_client.get(count_key):
        return "OK"

    # Check cache
    cached_value = redis_client.get(cache_key)
    if cached_value:
        return cached_value.decode('utf-8')

    # Fetch new content
    response = requests.get(url)
    html = response.text

    # Cache for 10 seconds
    redis_client.setex(cache_key, 10, html)
    # Return 0 if cache expired/not found
    return "0"
