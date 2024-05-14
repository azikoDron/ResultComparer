from django.http import HttpResponse
from django.shortcuts import render
from .models import Apps, Colours
from .influx_db import get_influx_data
from .forms import DateForm
from django.http import HttpResponseRedirect
import random


def index(request):
    # cards = {'available_cards': available_cards.keys()}
    cards = {'available_apps': Apps.objects.all()}
    return render(request, 'results/index.html', cards)


def detail(request, app_id):
    # if app_id == "Результаты НТ":
    #     return render(request, 'results/detail.html', {"results": get_influx_data()})
    # else:
    #     data = Apps.objects.get(name=app_id)
    #     app_detail = {"app_detail": data}
    #     return render(request, 'results/detail.html', app_detail)
    return render(request, 'results/detail.html')


def show_timeseries_db_data(request, transaction_id=""):
    if request.method == "POST":
        start_time = f"{request.POST['start_date']}T{request.POST['start_time']}:00:00Z"
        end_time = f"{request.POST['end_date']}T{request.POST['end_time']}:00:00Z"
        # print("------------------------------------:  ", start_time, end_time)

        data = get_influx_data(start_time=start_time, end_time=end_time, transaction=transaction_id)

        return render(request, 'results/comparison.html', {"results": data["data"],
                                                           "time_interval": data["time_interval"],
                                                           "colours": Colours()})
