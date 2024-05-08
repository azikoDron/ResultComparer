import time
import random


def gen_test_data():    # delete
    data_list = []
    for i in range(10):
        data = {"time": time.strftime("%FT%H:%M:%S:00Z"),
                'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}",
                'transaction': f"tran{random.randint(1, 10)}"}
        data_list.append(data)
    return data_list


def get_influx_data(ercentile="95", tansaction=""):     # fulfill
    return gen_test_data()


def get_influx_available_transactions():
    transactions =[]
    for i in gen_test_data():
        transactions.append(i["transaction"])
    return transactions

print(get_influx_available_transactions())

