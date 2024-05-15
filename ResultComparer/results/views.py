from django.http import HttpResponse
from django.shortcuts import render
from .models import Apps, Colours, TimeSeriesDB
from .forms import DateForm
from django.http import HttpResponseRedirect
import random


def index(request):
    # cards = {'available_cards': available_cards.keys()}
    cards = {'available_apps': Apps.objects.all()}
    return render(request, 'results/index.html', cards)


def detail(request, app_id):
    return render(request, 'results/detail.html')


start_time = ""
end_time = ""


def show_timeseries_db_data(request, transaction_id=""):
    global start_time, end_time
    db = TimeSeriesDB()
    if request.method == "POST":
        start_time = f"{request.POST['start_date']}T{request.POST['start_time']}:00:00Z"
        end_time = f"{request.POST['end_date']}T{request.POST['end_time']}:00:00Z"
        # print("------------------------------------:  ", start_time, end_time)

        data = db.get_influx_data(start_time=start_time, end_time=end_time, transaction=transaction_id)
    else:
        data = db.get_influx_data(start_time=start_time, end_time=end_time, transaction=transaction_id)

    return render(request, 'results/detail.html', {"results": data["data"],
                                                           "time_interval": data["time_interval"],
                                                           "colours": Colours()})
