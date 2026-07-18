import os
from data import (
    Data as data,
    DataFile
)


PROFILES = DataFile(
    name="profiles",
    path=os.path.join(os.path.dirname(__file__), "module_data", "profiles.json"),
    default={}
)

PURCHASES = DataFile(
    name="purchases",
    path=os.path.join(os.path.dirname(__file__), "module_data", "purchases.json"),
    default=[]
)

STATS = DataFile(
    name="stats",
    path=os.path.join(os.path.dirname(__file__), "module_data", "stats.json"),
    default={"sold": 0, "profit": 0, "refunded": 0}
)

DATA = [PROFILES, PURCHASES, STATS]


class Data:

    @staticmethod
    def get(name: str) -> dict | list:
        return data.get(name, DATA)

    @staticmethod
    def set(name: str, new: list | dict) -> dict:
        return data.set(name, new, DATA)
