#!/usr/bin/env python3

class Research:
    def file_reader(self):
        filename = 'data.csv'

        try:
            with open(filename, 'r') as file:
                return(file.read())
        except FileNotFoundError:
            return f"Error: file '{filename}' not exist!"


if __name__ == '__main__':
    research = Research()
    print(research.file_reader())