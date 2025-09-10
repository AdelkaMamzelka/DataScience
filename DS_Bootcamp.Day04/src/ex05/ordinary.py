#!/usr/bin/env python3

import sys
import resource

def read_all_lines(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines

if __name__ == "__main__":
    usage_start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    utime_start = resource.getrusage(resource.RUSAGE_SELF).ru_utime
    stime_start = resource.getrusage(resource.RUSAGE_SELF).ru_stime

    filepath = sys.argv[1]
    lines = read_all_lines(filepath)

    utime_end = resource.getrusage(resource.RUSAGE_SELF).ru_utime
    stime_end = resource.getrusage(resource.RUSAGE_SELF).ru_stime
    usage_end = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    peak_memory_gb = (usage_end) / 1024 / 1024  # так как ru_maxrss в КБ
    total_time = (utime_end + stime_end) - (utime_start + stime_start)

    print(f"Peak Memory Usage = {peak_memory_gb:.3f} GB")
    print(f"User Mode Time + System Mode Time = {total_time:.2f}s")

    for line in lines:
        pass