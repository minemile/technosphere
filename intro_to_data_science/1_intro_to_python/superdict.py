import json
import csv
import os
import logging
import random


class SuperDictException(Exception):
    pass


class SuperDict(dict):

    def __init__(self, obj):
        data = {}
        if isinstance(obj, str):
            if not os.path.isfile(obj):
                raise SuperDictException("File {0} not found.".format(obj))
            if obj.endswith("json"):
                with open(obj) as json_file:
                    data = json.load(json_file)
            elif obj.endswith("csv"):
                with open(obj) as csv_file:
                    reader = csv.reader(csv_file, delimiter=',')
                    for row in reader:
                        if len(row) > 2:
                            logging.warning(
                                "row %s contains > 2 columns", row)
                            continue
                        data[row[0]] = row[1]
            else:
                raise SuperDictException(
                    "Invalid path {0}, SuperDict accepts only json, csv or dict initialization".format(obj))
        elif isinstance(obj, dict):
            data = obj
        else:
            raise SuperDictException("Invalid format {0}".format(type(obj)))
        super(SuperDict, self).__init__(data)

    def get_random_key(self):
        return random.choice(self.keys())

    def get_longest_key_length(self):
        return max(map(lambda x: len(x), self.iterkeys()))

    def get_key_starts_from(self, begins):
        return filter(lambda x: x.startswith(begins), self.iterkeys())

    def to_json(self, file_name):
        with open(file_name, 'w') as json_file:
            json.dump(self, json_file)

    def to_csv(self, file_name):
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(self.iteritems())

    def __add__(self, other):
        self.update(other)
        return self


if __name__ == "__main__":
    sd = SuperDict({"a": 1, "b": 2})
