"""Shared utilities for the discovery system."""

import functools
import logging
import time


def setup_logging():
    """Configure logging for the discovery system."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )
    return logging.getLogger(__name__)


def retry_with_backoff(max_retries=3, backoff_factor=2, exceptions=(Exception,)):
    """
    Decorator to retry a function with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Factor to multiply delay between retries
        exceptions: Tuple of exceptions to catch and retry on
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = 1  # Start with 1 second delay
            logger = logging.getLogger(__name__)

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        # Last attempt, re-raise the exception
                        raise e

                    # Log the retry attempt
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= backoff_factor

        return wrapper
    return decorator