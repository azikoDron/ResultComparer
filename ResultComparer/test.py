import time
import datetime
import random

# print(str(datetime.datetime.now()).replace(" ", "T"))



print(time.strftime("%FT%H:%M:%S:00Z"))





def gen_test_data():
    data_list = []
    for i in range(10):
        data = {"time": time.strftime("%FT%H:%M:%S:00Z"),
                'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}",
                'transaction': f"tran{random.randint(1, 10)}"}
        data_list.append(data)
    return data_list