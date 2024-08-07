#!/usr/bin/env python3

import os
import logging
import datetime
from functools import wraps
from dotenv import dotenv_values

# Configure logging
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stdout.log')
logging.basicConfig(
    filename=filename,
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


# Logger decorator
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from datetime import datetime, timezone
        called_at = datetime.now(timezone.utc)
        logging.info(f"Running {func.__name__!r} function. Logged at {called_at}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"Function {func.__name__!r} executed successfully. Logged at {called_at}")
            return result
        except Exception as e:
            logging.error(f"Error in function {func.__name__!r} at {called_at}: {e}")
            raise
    return wrapper


CONFIG = dotenv_values(".env")
if not CONFIG:
    CONFIG = os.environ

@logger
def get_timestamp():
    logging.info('Now capturing time ...')
    now = datetime.datetime.now()
    print(f"The current time is: {str(now)}")


if __name__ == "__main__":
    try:
        get_timestamp()
        logging.info('Test completed successfully')
    except Exception as e:
        logging.error(f"Test failed dramatically: {e}")