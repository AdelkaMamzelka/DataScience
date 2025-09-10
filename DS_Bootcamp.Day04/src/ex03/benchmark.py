#!/usr/bin/env python3

import timeit
import sys
from functools import reduce

def sum_squares_loop(n):
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total

def sum_squares_reduce(n):
    return reduce(lambda acc, i: acc + i * i, range(1, n + 1), 0)

def measure_time(func, number, n):
    return timeit.timeit(lambda: func(n), number=number)

def main():
    if len(sys.argv) != 4:
        print("Usage: ./benchmark.py <function_name> <number> <n>")
        print("Function options: loop, reduce")
        sys.exit(1)

    func_name = sys.argv[1]
    number = int(sys.argv[2])
    n = int(sys.argv[3])

    if func_name == 'loop':
        elapsed = measure_time(sum_squares_loop, number, n)
    elif func_name == 'reduce':
        elapsed = measure_time(sum_squares_reduce, number, n)
    else:
        print("Unknown function name. Choose from: loop, reduce")
        sys.exit(1)

    print(elapsed)

if __name__ == '__main__':
    main()