"""
Function-level caching for indicator execution.

This module provides utilities to wrap indicator functions with a caching layer
to avoid redundant calculations when indicators call other indicators internally.
"""

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

import pandas as pd

F = TypeVar("F", bound=Callable[..., Any])


def _make_cache_key(event_log: pd.DataFrame, args: tuple, kwargs: dict) -> tuple:
    """
    Create a cache key from function arguments.

    Uses DataFrame's id (memory address) as a proxy for the DataFrame.
    This works well within a single execution context where the same
    DataFrame object is reused.

    Args:
        event_log: The event log DataFrame
        args: Positional arguments (excluding event_log)
        kwargs: Keyword arguments

    Returns:
        Tuple that can be used as a cache key

    """
    # Use id of event_log since DataFrames aren't hashable
    event_log_id = id(event_log)

    # Convert kwargs to sorted tuple for consistent hashing
    kwargs_tuple = tuple(sorted(kwargs.items()))

    return (event_log_id, args, kwargs_tuple)


def create_cached_wrapper(func: F, cache: dict) -> F:
    """
    Wraps a function to use a shared cache dictionary.

    The wrapper checks if the result is already cached before calling
    the original function. Only caches functions where the first argument
    is a pandas DataFrame (assumed to be event_log).

    Args:
        func: The function to wrap
        cache: Shared dictionary to store cached results

    Returns:
        Wrapped function that uses the cache

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract event_log (should be first positional arg)
        if not args:
            # No arguments, just call the function
            return func(*args, **kwargs)

        event_log = args[0]

        # Only cache if first arg is a DataFrame
        if not isinstance(event_log, pd.DataFrame):
            return func(*args, **kwargs)

        # Create cache key from all arguments
        cache_key = (func.__module__, func.__name__, _make_cache_key(event_log, args[1:], kwargs))

        # Check cache
        if cache_key in cache:
            return cache[cache_key]

        # Calculate and cache
        result = func(*args, **kwargs)
        cache[cache_key] = result
        return result

    return wrapper


def wrap_module_functions(module, cache: dict) -> dict:
    """
    Wraps all functions in a module with caching.

    Iterates through all functions in a module and replaces them with
    cached versions. Returns the original functions so they can be
    restored later.

    Args:
        module: The module containing functions to wrap
        cache: Shared cache dictionary

    Returns:
        Dictionary mapping function names to their original (unwrapped) versions

    """
    originals = {}

    for name, obj in inspect.getmembers(module):
        # Skip private functions
        if name.startswith("_"):
            continue

        # Only wrap functions defined in this module
        if inspect.isfunction(obj) and obj.__module__ == module.__name__:
            originals[name] = obj
            wrapped = create_cached_wrapper(obj, cache)
            setattr(module, name, wrapped)

    return originals


def unwrap_module_functions(module, originals: dict) -> None:
    """
    Restores original (unwrapped) functions to a module.

    This is important for cleanup to ensure functions return to their
    normal state after execution completes.

    Args:
        module: The module to restore
        originals: Dictionary mapping function names to original functions

    """
    for name, original_func in originals.items():
        setattr(module, name, original_func)
