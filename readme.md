# Simple Timer Script
---
This is a simple Python script that prints the current time to the terminal every minute using the Linux crontab scheduler.

## The Timer Function
The timer() function in the timer.py script prints the current time to the terminal:


```python
import datetime

def timer():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"The time is now {current_time}")
```

## Scheduling with Crontab
To run the timer() function automatically every minute, we'll use the Linux crontab scheduler.

Open the crontab editor by running the following command in the terminal:

```bash
$ crontab -e
```

Add the following line to the crontab file:

```bash
* * * * * /path/to/python /path/to/timer.py >> /home/username/timer/cron.log 2>&1
```

This will run the timer.py script every minute (the * * * * *  represents the schedule: minute, hour, day of month, month, day of week).

Output is logged into the cron.log in this directory. The 2>&1 part in the cron job command is used to redirect the standard error (2) to the same location as the standard output (1).

Here's a breakdown of what it means:
- 2> - This redirects the standard error stream (file descriptor 2) to a different location.
- &1 - This tells the shell to redirect the standard error stream to the same location as the standard output stream (file descriptor 1).

The combined 2>&1 means that any error messages that would normally be printed to the standard error stream will be redirected to the same file or location as the standard output.

This is commonly used in cron jobs to capture both the standard output (normal program output) and the standard error (error messages) in the same log file. This can be helpful for debugging and troubleshooting cron jobs, as you can see any error messages along with the regular output.

Save and exit the crontab editor. Now, the timer() function will run every minute, and any output or feeback from I/O streams will be captured in the log.
Once you are satisfied and more confident with the outcome or your app is at a stage where you would like a more customized/developed logging, you can reduce the cron to:

```bash
* * * * * /path/to/python /path/to/timer.py
```

so you no longer need to maintain the cron.log any further. It does help in a pinch though, if you need to debug/understand why it isn't working for you.

In our example, once we felt more confident with the cron scheduler. Our priority shifted to logging the actual events that transpire during the program.
While cron.log keeps track of what's happening to the scheduled item, the example below is a better representation of logging the events that transpire throughout the duration of the applications' execution via python's native logging module:

```python
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
```

## Running the Script Manually
You can also run the timer.py script manually by navigating to the script's directory and running the following command:

```bash
python timer.py
```

This will execute the timer() function and print the current time to the terminal.

## Conclusion
This simple Python script, combined with the Linux crontab scheduler, provides an easy way to get the current time printed to the terminal every minute. This can be useful for monitoring purposes or as a starting point for more complex time-based automation tasks.