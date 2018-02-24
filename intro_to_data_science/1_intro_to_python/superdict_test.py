import unittest
from superdict import SuperDict, SuperDictException
import random
import os
import csv
import json


class TestSuperDict(unittest.TestCase):

    def test_valid_initialization(self):
        with open("data.csv", "w") as csv_file, open("data.json", "w") as json_file:
            writer = csv.writer(csv_file, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows([["a", "1"], ["b", "2"], ["a", "3"]])
            json.dump({"a": "1", "b": "2", "a": "3"}, json_file)

        for sd in (SuperDict("data.csv"), SuperDict("data.json"), SuperDict({"a": "3", "b": "2"})):
            self.assertEqual(sd, {"a": "3", "b": "2"})

        os.remove("data.csv")
        os.remove("data.json")

    def test_invalid_initialization(self):
        self.assertRaises(SuperDictException, SuperDict, set())
        self.assertRaises(SuperDictException, SuperDict, "thrash.json")

    def test_dict_methods(self):
        sd = SuperDict({"a": 1, "b": 2})
        sd1 = SuperDict({"a": 3, "b": 4})

        self.assertEqual(sd["a"], 1)
        self.assertEqual(sd.items(), [("a", 1), ("b", 2)])
        self.assertEqual(sd.keys(), ["a", "b"])
        self.assertEqual(sd.values(), [1, 2])
        self.assertEqual(len(sd), 2)

    def test_new_methods(self):
        random.seed(47)
        sd = SuperDict({"a": 1, "bz": 2})
        sd1 = SuperDict({"a": 3, "c": 4, "bx": 5})

        self.assertEqual(sd.get_random_key(), "a")
        self.assertEqual(sd.get_longest_key_length(), 2)
        self.assertEqual(sd + sd1, {"a": 3, "bz": 2, "c": 4, "bx": 5})
        self.assertEqual(sd.get_key_starts_from("b"), ["bx", "bz"])


if __name__ == '__main__':
    unittest.main()
