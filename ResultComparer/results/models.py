from django.db import models
import random


class Apps(models.Model):
    name = models.CharField(max_length=40)
    about = models.CharField(max_length=240)

    def __str__(self):
        return self.name


#   SAVE DATA MODEL
class TestID(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class TestTransactions(models.Model):
    name = models.CharField(max_length=120)
    test_id = models.ManyToManyField(TestID, through="TestMetrics")

    def __str__(self):
        return self.name


class TestMetrics(models.Model):
    test_id = models.ForeignKey(TestID, on_delete=models.CASCADE)
    transaction = models.ForeignKey(TestTransactions, on_delete=models.CASCADE)
    time = models.DateTimeField()
    mean = models.FloatField(null=True)
    type = models.CharField(max_length=6)

#   END SAVE DATA MODEl


def save_test_data_to_db(data, test_id, percentile):
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


def get_test_id_list_from_db():
    return TestID.objects.all()


def get_all_test_data_from_db(test_id):
    test = TestID.objects.get(name=test_id)
    return test.testmetrics_set.all()


def get_all_test_data_grp_by_trn_from_db(test_id):
    data = {}
    test = TestID.objects.get(name=test_id)

    res = test.testmetrics_set.all()
    for i in res:
        try:
            data[i.transaction].append(i)
        except KeyError:
            data[i.transaction] = [i]
    # print(data)
    return data


def get_test_data_by_trn_from_db(test_id, transaction):
    data = {}
    test = TestID.objects.get(name=test_id)
    tr = TestTransactions.objects.filter(test_id=test, name=transaction)[0]
    res = tr.testmetrics_set.all()
    for i in res:
        try:
            data[i.transaction].append(i)
        except KeyError:
            data[i.transaction] = [i]
    return data



