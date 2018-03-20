import pandas as pd
import csv
from itertools import groupby

FILE = "titanic.csv"


def pandas_mean_fare():
    titanic_dataframe = pd.read_csv(FILE)
    return titanic_dataframe.groupby(["Pclass"])['Fare'].mean()


def python_mean_fare():
    file_ = open(FILE, "r")
    titanic_data = list(csv.DictReader(file_))
    file_.close()
    for (p_class, values) in groupby(sorted(titanic_data,
                                key=lambda x: x["Pclass"]), lambda x: x["Pclass"]):
        sum_ = 0
        count_v = 0
        for value in values:
            sum_ += float(value["Fare"])
            count_v += 1
        print(p_class, sum_ / count_v)

def derangment():



n = [2, 3, 4]
