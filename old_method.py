import random
import math
from itertools import repeat
from timer import repeat_timer_decorator_with_args

@repeat_timer_decorator_with_args(warmup=1, repeats=10, iterations=1, mem_test=False)
def main():
    items = [1,2,3,4]
    numbers = [0,0,0,0]
    rolls = 0
    maxOnes = 0

    while numbers[0] < 177 and rolls < 100_000:
        numbers = [0,0,0,0]
        for i in repeat(None, 231):
            roll = random.choice(items)
            numbers[roll-1] = numbers[roll-1] + 1
        rolls = rolls + 1
        if numbers[0] > maxOnes:
            maxOnes = numbers[0]
    print(f"Max number of ones rolled: {maxOnes} in {rolls} rolls.")

if __name__ == '__main__':
    main()
    