#!/usr/bin/env python3

import sys
import resource

def read_lines_generator(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            yield line

if __name__ == "__main__":
    utime_start = resource.getrusage(resource.RUSAGE_SELF).ru_utime
    stime_start = resource.getrusage(resource.RUSAGE_SELF).ru_stime
    usage_start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    filepath = sys.argv[1]
    gen = read_lines_generator(filepath)
    for line in gen:
        pass

    utime_end = resource.getrusage(resource.RUSAGE_SELF).ru_utime
    stime_end = resource.getrusage(resource.RUSAGE_SELF).ru_stime
    usage_end = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    peak_memory_gb = (usage_end) / 1024 / 1024
    total_time = (utime_end + stime_end) - (utime_start + stime_start)

    print(f"Peak Memory Usage = {peak_memory_gb:.3f} GB")
    print(f"User Mode Time + System Mode Time = {total_time:.2f}s")