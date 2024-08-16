# Graveler-efficiency-python
Showing more efficient python code for the Graveler problem using multiprocessing and more efficient functions

I created the new_methods.py to find what methods work best for this problem.
The old method was just slightly modified for easier testing.
To test effiency I have, in the past, created a decorator that can test functions. This is found tin the timer.py. It begins with a set warmup to let the compiler warm up then tests a set number of times and gives averages.

p.s. You might have to pip install things like numpy if you don't already have them in the env
### Findings

- It was found that modification of the rolling function sped up the time by a lot.
- There is nearly no need for stopping the program at 177 as it is nearly impossible to acheive that but this would make things much  faster if this value was lowered
- A sequential approach works best with this small number of rolls
- If given a large number of rolls the multiprocessed version works the best and also multithreading runs about the same as the sequential approach

### Output
For the old_method.py

    ```
    Running the function main 11 times, 10 test runs with 1 iterations within each test run with 1 warmup runs.
    Used the arguments: () and {}
    Beginning warmup
    Max number of ones rolled: 92 in 100000 rolls.
    Warmup time: 7.073065 seconds

    Max number of ones rolled: 90 in 100000 rolls.
    ...
    [7.05898309999975, ...]
    Function main executed in: (min) 7.012906 seconds, (max) 7.156768 seconds, (mean) 7.050507 seconds
    ```

For the new_methods.py

    ```
        Type of pool: threaded
    Running the function main 11 times, 10 test runs with 1 iterations within each test run with 1 warmup runs.
    Used the arguments: (4, 1, 231, 177, 'threaded', None) and {}
    Beginning warmup
    Maximum number of 1's rolled: 86
    Warmup time: 3.901284 seconds

    Maximum number of 1's rolled: 94
    ...
    [4.4983202000003075, ...]
    Function main executed in: (min) 3.602992 seconds, (max) 5.960198 seconds, (mean) 4.456032 seconds

    Type of pool: multiprocessing
    Running the function main 11 times, 10 test runs with 1 iterations within each test run with 1 warmup runs.
    Used the arguments: (4, 1, 231, 177, 'multiprocessing', None) and {}
    Beginning warmup
    Maximum number of 1's rolled: 89
    Warmup time: 6.088534 seconds

    Maximum number of 1's rolled: 89
    ...
    [6.44723729999896, ...]
    Function main executed in: (min) 6.378194 seconds, (max) 6.652247 seconds, (mean) 6.469492 seconds

    Type of pool: sequential
    Running the function main 11 times, 10 test runs with 1 iterations within each test run with 1 warmup runs.
    Used the arguments: (4, 1, 231, 177, 'sequential', None) and {}
    Beginning warmup
    Maximum number of 1's rolled: 88
    Warmup time: 2.723743 seconds

    Maximum number of 1's rolled: 88
    ...
    [2.7102455999993253, ...]
    Function main executed in: (min) 2.586961 seconds, (max) 2.710246 seconds, (mean) 2.618996 seconds
    ```
