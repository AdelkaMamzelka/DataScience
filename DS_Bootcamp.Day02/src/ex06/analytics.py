# analytics.py

import os
import logging
from random import randint
from config import Telegram_URL
import requests

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
        logging.info(f"Initialized Research with file_path: {file_path}")

    def file_reader(self, has_header=True):
        logging.info("Reading file...")
        if not os.path.isfile(self.file_path):
            logging.error(f"File not found: {self.file_path}")
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
                logging.error("Invalid line format detected")
                raise ValueError("Error: each line must contain two fields (0 or 1)!")
            data.append(list(map(int, fields)))

        logging.info("File read successfully!")
        return data

    class Calculations:
        def __init__(self, data):
            self.data = data
            logging.info("Initialized Calculations class.")

        @staticmethod
        def counts(data):
            head_count = sum(row[0] for row in data)
            tail_count = sum(row[1] for row in data)
            logging.info(f"Counts - Heads: {head_count}, Tails: {tail_count}")
            return head_count, tail_count

        @staticmethod
        def fractions(head_count, tail_count):
            total = head_count + tail_count
            if total == 0:
                logging.warning("Attempted to calculate fractions with total count of 0")
                return 0, 0
            head_fraction = (head_count / total) * 100
            tail_fraction = (tail_count / total) * 100
            logging.info(f"Fractions - Heads: {head_fraction}%, Tails: {tail_fraction}%")
            return head_fraction, tail_fraction
        
    class Analytics(Calculations):
        def __init__(self, data):
            super().__init__(data)
            logging.info("Initialized Analytics class.")

        def predict_random(self, number_of_predictions):
            predictions = [[randint(0, 1), 1 - randint(0, 1)] for _ in range(number_of_predictions)]
            logging.info(f"Generated random predictions: {predictions}")
            return predictions
        
        def predict_last(self):
            last_prediction = self.data[-1] if self.data else []
            logging.info(f"Last prediction: {last_prediction}")
            return last_prediction

    def send_telegram_message(self, message):
        logging.info("Sending telegram message...")
        try:
            response = requests.get(Telegram_URL + message )
            if response.status_code == 200:
                logging.info("Telegram message sent successfully!")
            else:
                logging.error(f"Failed to send message: {response.text}")
        except Exception as e:
            logging.error(f"Exception occurred: {e}")