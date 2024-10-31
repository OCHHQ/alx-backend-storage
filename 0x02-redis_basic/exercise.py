#!/usr/bin/env python3
"""
This module provides a Cache class for basic Redis operations.
"""

import redis
import uuid
from typing import Union


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
