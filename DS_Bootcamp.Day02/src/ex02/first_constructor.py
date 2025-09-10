#!/usr/bin/env python3

import sys
import os

class Research:
    def __init__(self, file_path):
        self.file_path= file_path    

    def file_reader(self):
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"Error: file '{self.file_path}' does not exist!")

        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
            if len(lines) < 1:
                raise ValueError("Error: file is empty or has no header!")
            
            header = lines[0].strip().split(',')
            if len(header) != 2:
                raise ValueError("Error: header must contain exactly two fields!")
            
            for line in lines[1:]:
                fields = line.strip().split(',')
                if len(fields) != 2 or not all(f in ['0', '1'] for f in fields):
                    raise ValueError("Error: each line must contain two fields (0 or 1)!")
                
            return ''.join(lines)
        except Exception as e:
            return str(e)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./first_constructor.py data.csv!")
        sys.exit(1)

    file_path = sys.argv[1]
    research = Research(file_path)
    print(research.file_reader())