#!/usr/bin/env python3
   
import os
from random import randint


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

        if has_header:
            start_index += 1

        for line in lines[start_index:]:
            fields = line.strip().split(',')
            if len(fields) != 2 or not all(f in ['0', '1'] for f in fields):
                raise ValueError("Error: each line must contain two fields (0 or 1)!")
            data.append(list(map(int, fields)))  # преобразуем строки в целые числа

        return data


class Analytics(Research):
    def __init__(self, data):
        super().__init__(data)
        self.data = data  # добавлено для доступа к data

    def counts(self):
        head_count = sum(row[0] for row in self.data)
        tail_count = sum(row[1] for row in self.data)
        return head_count, tail_count

    def fractions(self, head_count, tail_count):
        total = head_count + tail_count
        if total == 0:  # защита от деления на ноль
            return 0, 0
        head_fraction = (head_count / total) * 100
        tail_fraction = (tail_count / total) * 100
        return head_fraction, tail_fraction

    def predict_random(self, number_of_predictions):
        return [[randint(0, 1), 1 - randint(0, 1)] for _ in range(number_of_predictions)]

    def predict_last(self):
        return self.data[-1] if self.data else []

    def save_file(self, data, filename, extension):
        with open(f"{filename}.{extension}", "w") as file:
            file.write(data)