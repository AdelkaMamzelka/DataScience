#!/usr/bin/env python3

import timeit
import random
from collections import Counter

def generate_list():
    return [random.randint(0, 100) for _ in range(1_000_000)]

def count_numbers(lst):
    counts = {}
    for num in lst:
        counts[num] = counts.get(num, 0) + 1
    return counts

def top_numbers(lst):
    counts = count_numbers(lst)
    #сорт по убыванию знач
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

def count_numbers_counter(lst):
    return dict(Counter(lst))

def top_numbers_counter(lst):
    counter = Counter(lst)
    return counter.most_common(10)

def measure_time(func, lst, number):
    return timeit.timeit(lambda: func(lst), number=number)

def main():
    lst = generate_list()
    number = 10 

    time_count = measure_time(count_numbers, lst, number)
    time_top = measure_time(top_numbers, lst, number)

    time_count_counter = measure_time(count_numbers_counter, lst, number)
    time_top_counter = measure_time(top_numbers_counter, lst, number)

    print(f"my function: {time_count:.7f}")
    print(f"Counter: {time_count_counter:.7f}")
    print(f"my top: {time_top:.7f}")
    print(f"Counter's top: {time_top_counter:.7f}")

if __name__ == '__main__':
    main()