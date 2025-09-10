#!/usr/bin/env python3

import sys
import os

class Research:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self, has_header=True):
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"Error: file '{self.file_path}' does not exist!")

        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        data = []
        
        start_index = 0

        if (has_header):
            start_index += 1

        for line in lines[start_index:]:
            fields = line.strip().split(',')
            if len(fields) != 2 or not all(f in ['0', '1'] for f in fields):
                raise ValueError("Error: each line must contain two fields (0 or 1)!")
            data.append(list(map(int, fields)))  #преобразуем строки в целые числа

        return data

    class Calculations:
        @staticmethod
        def counts(data):
            head_count = sum(row[0] for row in data)
            tail_count = sum(row[1] for row in data)
            return head_count, tail_count

        @staticmethod
        def fractions(head_count, tail_count):
            total = head_count + tail_count
            if total == 0:  #защита от деления на ноль
                return 0, 0
            head_fraction = (head_count / total) * 100
            tail_fraction = (tail_count / total) * 100
            return head_fraction, tail_fraction

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./first_nest.py data.csv")
        sys.exit(1)

    file_path = sys.argv[1]
    research = Research(file_path)
    
    data = research.file_reader(has_header=True)
    print(data)
    
    calculations = Research.Calculations()  
    counts = calculations.counts(data) #кол-во 0 и 1
    print(counts[0], counts[1])
    
    fractions = calculations.fractions(*counts)  #получаем доли
    print(fractions[0], fractions[1])