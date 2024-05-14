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



import datetime

def date_range(
        begin_time,
        end_time,
        step_time,
        in_date_fmt='%H:%M',
        out_date_fmt=None,
        upper_bound=False):
    if out_date_fmt is None:
        out_date_fmt = in_date_fmt

    begin_time = datetime.datetime.strptime(begin_time, in_date_fmt)
    end_time = datetime.datetime.strptime(end_time, in_date_fmt)

    delta_time = (end_time - begin_time)
    origin_time = datetime.datetime.strptime('0', '%S')
    step_time = (
        datetime.datetime.strptime(step_time, in_date_fmt) - origin_time)

    if upper_bound:
        upper_bound = step_time.seconds

    for i in range(0, delta_time.seconds + upper_bound, step_time.seconds):
       yield (
           begin_time +
           datetime.timedelta(seconds=i)).strftime(out_date_fmt)

my_date_range = list(date_range('09:30', '16:00', '00:01'))




def chart_colour_picker(length):
    hex_colours = ["#28ff00", "#fa0000", "#00defa", "#3700fa", "#fa9a00", "#03fa00", "#514b76", "#defa00", "#2200fa",
                   "#fa4c00", "#be00fa", "#fa0051", "#00b4fa", "#c400fa", "#5c5b45", "#4b764f", "#4b7276", "#764b6a",
                   "#843232", "#516000"]
    return random.choice(hex_colours)


for i in range(25):
    print(chart_colour_picker())