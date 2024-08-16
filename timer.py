from functools import wraps
from timeit import repeat
from typing import Any, Callable, Dict

import numpy as np
from memory_profiler import memory_usage
import gc


def repeat_timer_decorator_with_args(
    warmup: int, repeats: int, iterations: int, mem_test: bool = False
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to time a function with arguments

    :param warmup: number of warmup iterations
    :param repeats: number of test runs
    :param iterations: number of iterations within each test run
    :param mem_test: 
    :return: wrapper function to time the function with arguments

    :rtype: Callable[[Callable[..., Any]], Callable[..., Any]]

            The first part this (Callable[ ....) refers to a the
            return of a function (the main wrapper), this function
            then takes an input and has an output discribed by
            [Callable[..., Any]], Callable[..., Any]
            the first being the outer repeat_timer_decorator function
            with any number of arguments and the second being the
            inner wrapper function with any number of arguments and
            Any type output.

    """
    # stop garbage collection 

    def repeat_timer_decorator(func: Callable) -> Callable:
        """Inner decorator function to time the function with arguments

        :param func: function to time
        :return: wrapper function to time the function with arguments
                    to be returned by the outer decorator
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Dict[str, Any]) -> Any:
            """Wrapper function to time the function with arguments
            It uses the @wraps decorator to preserve the metadata
            of the original function. Like the name, docstring, etc.

            :param args: positional arguments for the function
            :param kwargs: keyword arguments for the function
            :return: None
            """
            print(
                f"Running the function {func.__name__} {iterations*repeats+warmup} times, "
                f"{repeats} test runs with {iterations} iterations within each test run with {warmup} warmup runs."
            )
            print(f"Used the arguments: {args} and {kwargs}")

            # warmup the interpreter
            if warmup > 0:
                print("Beginning warmup")
                warmup_time = repeat(lambda: func(*args, **kwargs), number=warmup, repeat=1)
                print(f"Warmup time: {np.mean(warmup_time):.6f} seconds")
                print()
                
            if mem_test:
                gc.disable
                print("Begining memory test")
                start_mem= memory_usage()[0]
                func(*args, **kwargs)
                end_mem = memory_usage()[0]
                print(f"Memory usage: {end_mem - start_mem:.6f} MiB")
                gc.enable

            times = repeat(lambda: func(*args, **kwargs), number=iterations, repeat=repeats)
            print(times)
            print(
                f"Function {func.__name__} executed in: (min) "
                f"{np.min(times):.6f} seconds, (max) {np.max(times):.6f} "
                f"seconds, (mean) {np.mean(times):.6f} seconds"
            )
            print()

        return wrapper
    return repeat_timer_decorator


# you will get no return from this function due to the wrapper
# if output is needed, you can return add a return in the wrapper(...)
@repeat_timer_decorator_with_args(warmup=1, repeats=8, iterations=1, mem_test=True)
def some_function() -> Any:
    """Function to time"""
    for _ in range(1000000):
        pass


# some_function()
