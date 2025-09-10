#!/usr/bin/env python3

import timeit

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

def measure_time(func, emails_list, number):
    return timeit.timeit(lambda: func(emails_list), number=number)

def main():
    emails = our_emails()
    number = 90000000

    time_loop = measure_time(get_gmail_loop, emails, number)
    time_comp = measure_time(get_gmail_comprehension, emails, number)
    time_map = measure_time(get_gmail_map, emails, number)

    times = sorted(
        [
            (time_loop, 'loop'),
            (time_comp, 'comprehension'),
            (time_map, 'map')
        ],
        key=lambda x: x[0]
    )

    #какой метод лучше
    print(f"it is better to use a {times[0][1]}")

    #в порядке возр
    print(f"{times[0][0]:.8f} vs {times[1][0]:.8f} vs {times[2][0]:.8f}")

if __name__ == '__main__':
    main()