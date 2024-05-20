from django.db import models
import random
from .influx_db import InfluxConnect
from .settings import TIMESERIES_DATABASES
import datetime
import re


class Apps(models.Model):
    name = models.CharField(max_length=40)
    about = models.CharField(max_length=240)

    def __str__(self):
        return self.name


class Colours:
    def chart_colour_picker(self):
        hex_colours = ["#28ff00", "#fa0000", "#00defa", "#3700fa", "#fa9a00", "#03fa00", "#514b76", "#defa00",
                       "#2200fa",
                       "#fa4c00", "#be00fa", "#fa0051", "#00b4fa", "#c400fa", "#5c5b45", "#4b764f", "#4b7276",
                       "#764b6a",
                       "#843232", "#516000"]
        return random.choice(hex_colours)


#   SAVE DATA MODEL
class TestID(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class TestTransactions(models.Model):
    name = models.CharField(max_length=120)
    members = models.ManyToManyField(TestID, through="TestMetrics")

    def __str__(self):
        return self.name


class TestMetrics(models.Model):
    test_id = models.ForeignKey(TestID, on_delete=models.CASCADE)
    transaction = models.ForeignKey(TestTransactions, on_delete=models.CASCADE)
    time = models.DateTimeField()
    mean = models.FloatField(null=True)
    type = models.CharField(max_length=6)

#   END SAVE DATA MODEl


def save_data_to_db(data, test_id, percentile):
    test_id = TestID.objects.create(name=test_id)
    for i, j in data.items():
        transaction = TestTransactions.objects.create(name=i)
        for k in j:
            dt = TestMetrics(
                test_id=test_id,
                transaction=transaction,
                time=k["time"],
                mean=k["mean"],
                type=percentile
            )
            dt.save()




class TimeSeriesDB:
    def __int__(self):
        if TIMESERIES_DATABASES["NAME"] == 'InfluxDB':
            self.db = InfluxConnect(TIMESERIES_DATABASES["HOST"], TIMESERIES_DATABASES["USER"],
                               TIMESERIES_DATABASES["PASS"], TIMESERIES_DATABASES["SCHEMA"])

    def get_influx_data(self, start_time="", end_time="", percentile="95", transaction=""):  # fulfill

        #  DEBUG MODE !!!!!!!!!!!
        from .influx_db import get_influx_data
        return get_influx_data(start_time, end_time, transaction=transaction)
        #  DEBUG MODE !!!!!!!!!!!


        #   PRODUCTION !!!!!!!!!!!!!!!
        # if start_time and end_time:
        #     if transaction:
        #         data = self.db.get_transaction_by_id(self.date_to_microseconds(start_time), self.date_to_microseconds(end_time), transaction)
        #     else:
        #         data = self.db.get_all_transactions(self.date_to_microseconds(start_time), self.date_to_microseconds(end_time))
        # else:
        #     # data = db.get_all_transactions()
        #     data = []
        # data_dict = {"data": data,
        #              "time_interval": self.get_data_time_interval(data)}
        # return data_dict

    @staticmethod
    def date_to_microseconds(date):
        """
        date: 2024-05-08T09:00:00:00Z
        return: 1715158800000
        """
        return int((datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S:%f") -
                    datetime.datetime.strptime("1970-01-01T00:00:00:00", "%Y-%m-%dT%H:%M:%S:%f")
                    ).total_seconds() * 1000)

    @staticmethod
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

