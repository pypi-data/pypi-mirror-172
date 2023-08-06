import asyncio
import functools


def run_in_executor(_func):
    """Decorator to run blocking code."""

    @functools.wraps(_func)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_running_loop()
        func = functools.partial(_func, *args, **kwargs)
        return loop.run_in_executor(executor=None, func=func)

    return wrapped


def cancel_tasks():
    for task in asyncio.all_tasks():
        if task.done():
            continue

        task.cancel()
