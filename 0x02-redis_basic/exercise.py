#!/usr/bin/env python3
"""
This module provides a Cache class for basic Redis operations.
"""

import redis
import uuid
from typing import Union, Callable, Optional


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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in Redis with a randomly generated key.
        Args:
            data (Union[str, bytes, int, float]): Data to store in Redis.
        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())  # Generate a unique key
        self._redis.set(key, data)  # Store data in Redis with the key
        return key

    def get(
            self,
            key: str,
            fn: Optional[callable] = None
    ) -> Optional[Union[str, bytes, int, float]]:
        """Here i am trying to understand
        Retrieve data from redis and optionally
        apply converstion function
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string from redis."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integar from radis"""
        return self.get(key, int)

    def count_calls(method: Callable) -> Callable:
    """Decorator that counts how many times a method is called."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Define the Redis key based on the method's qualified name
        key = method.__qualname__

        # Increment the count in Redis
        self._redis.incr(key)

        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper
