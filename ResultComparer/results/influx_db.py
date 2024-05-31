import time
import random
import re
import datetime



class InfluxConnect:

    def __init__(self, test1, test2, test3, test4):
        pass

    def get_transaction_by_id(self, start_time="", end_time="", transaction=""):
        data_dict = {}
        for i in range(1):
            data_dict[f"tran-{i}"] = [
                {"time": time.strftime("%FT%H:03:%SZ"),
                 'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"},
                {"time": time.strftime("%FT%H:01:%SZ"),
                 'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"},
                {"time": time.strftime("%FT%H:02:%SZ"),
                 'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"}
            ]
        return data_dict

    def get_all_transactions(self, start_time="", end_time="" ):  # delete
        data_dict = {}
        for i in range(10):
            data_dict[f"tran-{i}"] = [
                {"time": time.strftime("%FT%H:03:%SZ"),
                 'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"},
                {"time": time.strftime("%FT%H:01:%SZ"),
                 'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"},
                {"time": time.strftime("%FT%H:02:%SZ"),
                 'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"}
            ]

        return data_dict

