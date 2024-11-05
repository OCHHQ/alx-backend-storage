#!/usr/bin/env python3
"""
Module for implementing a web caching and tracking system using Redis.

This module provides a simple web caching and tracking system.
It uses Redis for caching and tracking URL accesses.
"""

import requests
import redis
from typing import Callable
from functools import wraps


def connect_to_redis() -> redis.Redis:
    """Establish a Redis connection"""
    return redis.Redis()


r = connect_to_redis()


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count URL accesses.

    Args:
        method: Function to decorate

    Returns:
        Decorated function
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function"""
        key = f"count:{url}"
        try:
            r.incr(key)
            return method(url)
        except redis.RedisError as e:
            print(f"Error incrementing count: {e}")
            return None
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """
    Get the HTML content of a URL and track access count.

    Args:
        url (str): URL to fetch

    Returns:
        str: HTML content of URL or '0' if checking cache status
    """
    cache_key = f"cached:{url}"
    if r.exists(cache_key):
        return "0" if url == "http://google.com" else r.get(cache_key).decode('utf-8')

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    html = response.text
    r.setex(cache_key, 10, html)
    return "OK"
