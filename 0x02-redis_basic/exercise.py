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

    Example:
        @count_calls
        def my_method():
            pass
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call counter and executes the method.

        Args:
            self: Instance of the class
            *args: Variable positional arguments
            **kwargs: Variable keyword arguments

        Returns:
            The result of the wrapped method
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    """Store history of I/O for a particular fuction


    REDIS COMMAND USED:
        RPUSH - Append Values to the end of a list
        LRANGE - Retrieves elements of the list (used in my main.py)

    REDIS LISTS:
        work like python list but store in REDIS
    """
    input = method.__qualname__ + ":inputs"
    outputs = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper that function as track to I/O using redis
        """
        #STORE I ARGUMENTS AS STRING IN REDIS LIST
        self._redis.rpush(input_list, str(args))

        #EXECUTE the wrapper function and store its output
        output = method(self, *args, **kwargs)

        #STORE O IN REDIS LIST
        self._redis.rpush(output_list, str(output))

        return output
    
    return wrapper


class Cache:
    """
    A cache class that provides interface to Redis operations.

    This class implements basic caching operations using Redis as the
    backend storage. It supports storing different data types and
    provides type conversion utilities for retrieval.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache instance.

        Creates a new Redis client connection and flushes the database
        to ensure a clean state.
        """
        self._redis = redis.Redis()
        self._redis.flushdb() 

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key.

        Args:
            data: The data to store, can be string, bytes, int, or float

        Returns:
            str: The key under which the data is stored

        Example:
            cache = Cache()
            key = cache.store("example")
         REDIS COMMAND USED:
            SET - store key_value pair in redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally convert it.

        Args:
            key: The key to look up in Redis
            fn: Optional conversion function to apply to the data

        Returns:
            The data from Redis, optionally converted by fn, or None if
            key doesn't exist

        Example:
            cache = Cache()
            data = cache.get("my_key", fn=int)

         REDIS COMMAND USED:
            GET: Retrieve value by key
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.

        Args:
            key: The key to look up in Redis

        Returns:
            Optional[str]: The string value, or None if key doesn't exist

        Example:
            cache = Cache()
            string_data = cache.get_str("my_key")
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        Args:
            key: The key to look up in Redis

        Returns:
            Optional[int]: The integer value, or None if key doesn't exist

        Example:
            cache = Cache()
            int_data = cache.get_int("my_key")
        """
        return self.get(key, int)
