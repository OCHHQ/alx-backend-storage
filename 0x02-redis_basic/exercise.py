#!/usr/bin/env python3
"""
Redis Cache Module

This module implements a basic caching system using Redis.
It provides functionality for storing and retrieving data
with optional type conversion and tracking method calls.
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times a method is called.

    Args:
        method: The method to be decorated

    Returns:
        Callable: The wrapped method that includes call counting functionality
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call counter and executes the method.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.

    Args:
        method: The method to be decorated

    Returns:
        Callable: The wrapped method that tracks inputs and outputs
    """
    inputs = method.__qualname__ + ":inputs"
    outputs = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that tracks inputs and outputs using Redis lists.
        """
        # Store the input arguments
        self._redis.rpush(inputs, str(args))

        # Execute the wrapped function and store its output
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(output))

        return output

    return wrapper


class Cache:
    """
    A cache class that provides interface to Redis operations.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally convert it.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.
        """
        return self.get(key, int)
