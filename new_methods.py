import random
from itertools import repeat
import multiprocessing
from timer import repeat_timer_decorator_with_args
from typing import Tuple, Optional
from concurrent.futures import ThreadPoolExecutor



def _roll_dice(number_of_sides: int, number_of_rolls: int, side_to_count:int) -> int:
    """
    Rolling a dice with a given number of sides a given number of times
    and counting the number of ones rolled.

    :param number_of_sides: number of sides of the dice
    :param number_of_rolls: number of times the dice is rolled
    :param side_to_count: side to count when the dice is done being rolled

    :return: number of ones rolled given the arguments
    """
    # Roll the dice and count the number of ones rolled
    rolls = random.choices(range(1, number_of_sides + 1), k=number_of_rolls)
    # Return the number of ones rolled
    return rolls.count(side_to_count)

def _roll_dice_wrapper(wrapper_args: Tuple[int, int, int]) -> int:
    """
    Wrapper function for the _roll_dice function to allow for multiprocessing
    as the pool.imap_unordered function only accepts functions with one argument.

    :param wrapper_args: tuple of arguments for the _roll_dice function

    :return: result of the _roll_dice function
    """
    # Unpack the arguments and call the _roll_dice function
    return _roll_dice(*wrapper_args)


@repeat_timer_decorator_with_args(warmup=1, repeats=10, iterations=1, mem_test=False)
def main(number_of_sides: int, side_to_count: int, number_of_rolls: int, threshold: int, type_of_pool:str, max_number_of_processes: Optional[int]=None) -> None:
    """
    Main function to roll a dice with a given number of sides a given number of times
    and count the number of ones rolled. The function uses multiprocessing to speed up
    the process.

    :param number_of_sides: number of sides of the dice
    :param number_of_rolls: number of times the dice is rolled
    :param threshold: threshold to terminate the pool
    :param type_of_pool: type of pool to use
    :param max_number_of_processes: maximum number of processes to use for multiprocessing

    :return: None
    """
    results = []
    match type_of_pool:
        case "threaded":
            with ThreadPoolExecutor(max_workers=max_number_of_processes) as executor:
                # As I do not care about the order of the results, I use map for multithreading
                future_results = executor.map(_roll_dice_wrapper, repeat((number_of_sides, number_of_rolls, side_to_count), 100_000))
                
                for result in future_results:
                    # Append the result to the list of results
                    results.append(result)

                    # If the result is greater than the threshold, break the loop
                    if result > threshold:
                        break

            # Ensure all threads are cleaned up
            executor.shutdown(wait=True)
        case "multiprocessing":
            with multiprocessing.Pool(max_number_of_processes) as pool:
                # As I do not care about the order of the results, I use imap_unordered for multiprocessing
                for result in pool.imap_unordered(_roll_dice_wrapper, repeat((number_of_sides, number_of_rolls, side_to_count), 100_000)):
                    # Append the result to the list of results
                    results.append(result)

                    # If the result is greater than the threshold, terminate the pool
                    if result > threshold:
                        pool.terminate()
                        break

            # Ensure all processes are cleaned up
            pool.close()
            pool.join()
        case "sequential":
            for _ in range(100_000):
                result = _roll_dice_wrapper((number_of_sides, number_of_rolls, side_to_count))
                results.append(result)
                # If the result is greater than the threshold, break the loop
                if result > threshold:
                    break
        case _:
            raise ValueError("Invalid type of pool")
    # Print the max result, showing the maximum number of ones rolled
    print(f"Maximum number of {side_to_count}'s rolled: {max(results)}")

if __name__ == "__main__":
    number_of_sides = 4
    side_to_count = 1
    number_of_rolls = 231
    threshold = 177
    max_number_of_processes = None
    
    for type in ["threaded", "multiprocessing", "sequential"]:
        print(f"Type of pool: {type}")
        main(number_of_sides, side_to_count, number_of_rolls, threshold, type, max_number_of_processes)
