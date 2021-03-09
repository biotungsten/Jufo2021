from itertools import product, combinations
import csv
import random

class CSV:
    def __init__(self, column_variables, column_constants, empty_value=""):
        self.columns = ["row_id"] + list(column_variables.keys()) + column_constants
        self.constant_count = len(column_constants)
        self.rows = product(*column_variables.values())
        self.empty_value = empty_value

    def generate_csv(self, path):
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.columns)
            for row in self.rows:
                row_id = "".join([str(n) for n in row])
                row = list(row)
                row = [row_id] + row + [self.empty_value]*self.constant_count
                writer.writerow(row)