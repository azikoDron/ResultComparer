from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Apps, Colours, TimeSeriesDB, save_data_to_db
from .forms import DateForm
from django.contrib import messages
from django.http import HttpResponseRedirect
import random

tmp_cache_data = {
    "start_date": "2024-05-08",
    "end_date": "",
    "start_date_time": "",
    "end_date_time": "",
    "metrics_type": "",
}


def index(request):
    # cards = {'available_cards': available_cards.keys()}
    cards = {'available_apps': Apps.objects.all(), "time_form": DateForm}
    return render(request, 'results/index.html', cards)
                            

def detail(request, app_id):
    return render(request, 'results/detail.html')


def show_timeseries_db_data(request, transaction_id="", save_data=False):
    db = TimeSeriesDB()
    form = DateForm()
    data = {}
    if request.method == "POST":

        try:
            form.initial["start_date"] = request.POST['start_date']
            form.initial["start_time"] = request.POST['start_time']
            form.initial["end_date"] = request.POST['end_date']
            form.initial["end_time"] = request.POST['end_time']
            form.initial["metric"] = request.POST['metric']
        except KeyError:
            print(KeyError)

    start_date_time = f"{form.initial['start_date']}T{form.initial['start_time']}:00:00Z"
    end_date_time = f"{form.initial['end_date']}T{form.initial['end_time']}:00:00Z"

    data = db.get_influx_data(start_time=start_date_time,
                                      end_time=end_date_time,
                                      transaction=transaction_id)
    if "save_button" in request.POST.keys():
        save_data_to_db(data["data"], "regress_1", form.initial["metric"])
    return render(request, 'results/detail.html', {"results": data["data"],
                                                           "time_interval": data["time_interval"],
                                                           "colours": Colours(),
                                                            "time_form": form,
                                                            "save_button": True})

def save_data(request):
    #   print("----------------------- SAVE DATA----------", request.POST)
    messages.info(request, 'Your password has been changed successfully!')
    return redirect("show_timeseries_db_data")
