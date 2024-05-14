import time
import random
import re
import datetime



class InfluxConnect:
    pass
# DELETE
def gen_test_data(start_time="", end_time=""):    # delete
    data_dict = {}
    for i in range(10):
        data_dict[f"tran-{i}"] = [{"time": time.strftime("%FT%H:03:%S:00Z"),
                                  'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"},
                                  {"time": time.strftime("%FT%H:01:%S:00Z"),
                                   'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"},
                                   {"time": time.strftime("%FT%H:02:%S:00Z"),
                                   'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"}
                                 ]

        # data_list.append(data)
    return data_dict


def date_to_microseconds(date):
    """
    date: 2024-05-08T09:00:00:00Z
    return: 1715158800000
    """
    return int((datetime.datetime.fromisoformat(date) - datetime.datetime.fromisoformat(
        "1970-01-01T00:00:00:00Z")).total_seconds() * 1000)


def get_data_time_interval(timeseries_dict: dict):
    """
    return: sorted list of time without doubles
    """
    time_list = []
    for i, j in timeseries_dict.items():
        for k in j:
            for t in k.values():
                s = re.findall("[0-9]{2}:[0-9]{2}:[0-9]{2}", t)
                try:
                    time_list.append(s[0])  # ADD [0:5]
                except IndexError:
                    continue
    return sorted(list(set(time_list)))


def get_influx_data(start_time="", end_time="", percentile="95", transaction=""):     # fulfill
    if start_time and end_time:
        if transaction:
            data = gen_test_data(date_to_microseconds(start_time), date_to_microseconds(end_time), transaction)
        else:
            data = gen_test_data(date_to_microseconds(start_time), date_to_microseconds(end_time))
    else:
        data = gen_test_data()
    data_dict = {"data": data,
                 "time_interval": get_data_time_interval(data)}
    return data_dict
