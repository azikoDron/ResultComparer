from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Apps, Colours, TimeSeriesDB, save_test_data_to_db, get_test_id_list_from_db, get_all_test_data_from_db
from .forms import DateForm
from django.contrib import messages
from django.http import HttpResponseRedirect
import random

form = DateForm()
ts_db = TimeSeriesDB()

def index(request):
    # cards = {'available_cards': available_cards.keys()}
    cards = {'available_apps': Apps.objects.all(), "time_form": DateForm}
    return render(request, 'results/index.html', cards)
                            

def detail(request, app_id):
    return render(request, 'results/detail.html')


def show_timeseries_db_data(request, transaction_id="", save_data=False):
    global form, ts_db
    context = {"results": "",
               "time_interval": "",
               "colours": Colours(),
               "time_form": form,
               "save_button": True,
               "test_id_list": get_test_id_list_from_db()
               }

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

    data = ts_db.get_influx_data(start_time=start_date_time,
                                end_time=end_date_time,
                                transaction=transaction_id)
    context["results"] = data["data"]
    context["time_interval"] = data["time_interval"]
    #   SAVE TEST RESULTS
    if "save_button" in request.POST.keys():
        if "TEST" in request.POST["save_button"]:
            test_id = str(request.POST["save_button"]).replace("TEST: ", "")
            save_test_data_to_db(data["data"], test_id, form.initial["metric"])
    #   COMPARISON
    if "test_id" in request.POST.keys():
        if request.POST["test_id"]:
            return compare_test_results(request)

    return render(request, 'results/detail.html', context)


def compare_test_results(request, transaction_id=""):
        context = {}
        context["test_data_from_db"] = get_all_test_data_from_db(request.POST["test_id"])
        return render(request, 'results/comparison.html', context)


def save_data(request):
    #   print("----------------------- SAVE DATA----------", request.POST)
    messages.info(request, 'Your password has been changed successfully!')
    return redirect("show_timeseries_db_data")
