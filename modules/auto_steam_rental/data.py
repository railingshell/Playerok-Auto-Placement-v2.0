import os
from data import (
    Data as data,
    DataFile
)


ACCOUNTS = DataFile(
    name="accounts",
    path=os.path.join(os.path.dirname(__file__), "module_data", "accounts.json"),
    default=[]
)

RENTALS = DataFile(
    name="rentals",
    path=os.path.join(os.path.dirname(__file__), "module_data", "rentals.json"),
    default=[]
)

STATS = DataFile(
    name="stats",
    path=os.path.join(os.path.dirname(__file__), "module_data", "stats.json"),
    default={"rented": 0, "profit": 0, "refunded": 0}
)

DATA = [ACCOUNTS, RENTALS, STATS]


class Data:

    @staticmethod
    def get(name: str) -> dict | list:
        return data.get(name, DATA)

    @staticmethod
    def set(name: str, new: list | dict) -> dict:
        return data.set(name, new, DATA)
