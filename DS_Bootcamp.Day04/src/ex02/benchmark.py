#!/usr/bin/env python3

import timeit
import sys

def our_emails():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com']
    emails *= 5
    return emails

def get_gmail_loop(emails_list):
    result = []
    for email in emails_list:
        if email.endswith('@gmail.com'):
            result.append(email)
    return result

def get_gmail_comprehension(emails_list):
    return [email for email in emails_list if email.endswith('@gmail.com')]

def get_gmail_map(emails_list):
    return list(filter(lambda email: email.endswith('@gmail.com'), map(lambda email: email, emails_list)))

def get_gmail_filter(emails_list):
    return list(filter(lambda email: email.endswith('@gmail.com'), emails_list))

def measure_time(func, emails_list, number):
    return timeit.timeit(lambda: func(emails_list), number=number)

def main():
    if len(sys.argv) != 3:
        print("Usage: ./benchmark.py <function_name> <number>")
        print("Function options: loop, list_comprehension, map, filter")
        sys.exit(1)

    func_name = sys.argv[1]
    number = int(sys.argv[2])

    emails = our_emails()

    if func_name == 'loop':
        elapsed = measure_time(get_gmail_loop, emails, number)
    elif func_name == 'list_comprehension':
        elapsed = measure_time(get_gmail_comprehension, emails, number)
    elif func_name == 'map':
        elapsed = measure_time(get_gmail_map, emails, number)
    elif func_name == 'filter':
        elapsed = measure_time(get_gmail_filter, emails, number)
    else:
        print("Unknown function name. Choose from: loop, list_comprehension, map, filter")
        sys.exit(1)

    print(elapsed)

if __name__ == '__main__':
    main()