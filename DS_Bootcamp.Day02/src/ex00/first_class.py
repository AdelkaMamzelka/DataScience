#!/usr/bin/env python3

class Must_read:
    def __init__(self):
        filename = 'data.csv'

        try:
            with open(filename, 'r') as file:
                print(file.read())
        except FileNotFoundError:
            print(f"Error: file '{filename}' not exist!")


if __name__ == '__main__':
    Must_read()