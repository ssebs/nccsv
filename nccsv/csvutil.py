# csvutil.py - CSV Utilities for nccsv
import csv


class CSV():
    def __init__(self, filename=None):
        if filename:
            self.load(filename)
        self.filename = filename
        self.data = None
    # init

    def load(self, filename):
        data_tmp = []
        with open(filename, "r") as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            for row in reader:
                data_tmp.append(row)
        self.data = data_tmp
        return data_tmp
    # load

    def save(self, filename):
        with open(filename, "w") as f:
            writer = csv.writer(f, delimiter=",", quotechar='"')
            writer.writerows(self.data)
    # save
