import time
import random
import re
from datetime import datetime
from dateutil import tz
from .settings import TIMESERIES_DATABASES


class InfluxConnect:

    def __init__(self, test1, test2, test3, test4):
        pass

    def get_transaction_by_id(self, start_time="", end_time="", transaction=""):
        data_dict = {}
        for i in range(1):
            data_dict[f"tran-{i}"] = []
            for j in range(30):
                data_dict[f"tran-{i}"].append({"time": time.strftime(f"%FT%H:{str(j/10).replace('.','')}:%SZ"),
                 'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"})
        return data_dict

    def get_all_transactions(self, start_time="", end_time="" ):  # delete
        data_dict = {}
        for i in range(10):
            data_dict[f"tran-{i}"] = []
            for j in range(30):
                data_dict[f"tran-{i}"].append({"time": time.strftime(f"%FT%H:{str(j / 10).replace('.', '')}:%SZ"),
                                               'mean': f"{random.randint(10, 500)}.{random.randint(100, 9999999999999)}"})
        return data_dict


class TimeSeriesDB:
    def __init__(self):

        if TIMESERIES_DATABASES["NAME"] == 'InfluxDB':
            self.db = InfluxConnect(TIMESERIES_DATABASES["HOST"], TIMESERIES_DATABASES["USER"],
                               TIMESERIES_DATABASES["PASS"], TIMESERIES_DATABASES["SCHEMA"])

    def get_influx_data(self, start_time="", end_time="", percentile="95", transaction=""):  # fulfill
        if start_time and end_time:
            if transaction:
                data = self.db.get_transaction_by_id(self.date_to_microseconds(start_time), self.date_to_microseconds(end_time), transaction)
            else:
                data = self.db.get_all_transactions(self.date_to_microseconds(start_time), self.date_to_microseconds(end_time))
        else:
            # data = db.get_all_transactions()
            data = []
        data_dict = {"data": data,
                     "time_interval": self.get_data_time_interval(data)}
        return data_dict

    @staticmethod
    def date_to_microseconds(date):
        """
        date: 2024-05-08T09:00:00:00Z
        return: 1715158800000
        """
        return int(((datetime.strptime(date.replace("Z", ""), "%Y-%m-%dT%H:%M:%S:%f") -
                    datetime.strptime("1970-01-01T00:00:00:00", "%Y-%m-%dT%H:%M:%S:%f")
                    ).total_seconds() - 10800) * 1000)

    @staticmethod
    def get_data_time_interval(timeseries_dict: dict):
        """
        return: sorted list of time without doubles
        """
        time_list = []
        for i, j in timeseries_dict.items():
            for k in j:
                t = str(k['time']).replace("T", " ").replace("Z", "")
                t = TimeSeriesDB.convert_timezone(t)
                s = re.findall("[0-9]{2}:[0-9]{2}:[0-9]{2}", str(t).replace("+03:00", ""))
                try:
                    time_list.append(s[0])  # ADD [0:5]
                except IndexError:
                    continue
        return sorted(list(set(time_list)))

    @staticmethod
    def convert_timezone(date_time):
        """
        '2011-01-21 02:37:21', '%Y-%m-%d %H:%M:%S'
        """
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Moscow')
        utc = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)
        utc = utc.replace(tzinfo=from_zone)
        return utc.astimezone(to_zone)
