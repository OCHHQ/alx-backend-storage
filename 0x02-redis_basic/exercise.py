#!/usr/bin/env python3
"""
This module provides a Cache class for basic Redis operations.
"""

import redis
import uuid
import functools
from typing import Union, Callable, Optional

def count_calls(method: Callable) -> Callable:
    """Decorator that counts how many times a method is called."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Use the method's qualified name as the Redis key
        key = method.__qualname__

        # Increment the call count in Redis
        self._redis.incr(key)

        # Execute the original method
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Cache class to interact with Redis.
    Uses Redis to store, retrieve, and manage data.
    """

    def __init__(self):
        """
        Initializes the Cache instance.
        Creates a Redis client and clears any
        existing data in the Redis instance.
        """
        self._redis = redis.Redis()  # Create Redis client
        self._redis.flushdb()  # Clear the Redis database

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a random key and return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @count_calls
    def get(
            self,
            key: str,
            fn: Optional[Callable] = None
    ) -> Optional[Union[str, bytes, int, float]]:
        """Retrieve data from Redis and optionally apply conversion function."""
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    @count_calls
    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string from Redis."""
        return self.get(key, lambda x: x.decode('utf-8'))

    @count_calls
    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer from Redis."""
        return self.get(key, int)
