from typing import Dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Apps, save_test_data_to_db, get_test_id_list_from_db, \
    get_test_data_by_trn_from_db, get_all_test_data_grp_by_trn_from_db
from .forms import DateForm
from .influx_db import TimeSeriesDB
from .mods import Colours
from django.http import HttpResponseRedirect


# form = DateForm()
ts_db = TimeSeriesDB()
context = { "results": "",
            "time_interval": "",
            "colours": Colours(),
            "time_form": "",
            "save_button": True,
            "start_date_time": "",
            "end_date_time": "",
            "test_id": "",
           }


def index(request):
    # cards = {'available_cards': available_cards.keys()}
    cards = {'available_apps': Apps.objects.all(), "time_form": DateForm}
    return render(request, 'results/index.html', cards)
                            

def detail(request, app_id):
    return render(request, 'results/detail.html')


def show_timeseries_db_data(request, transaction_id="", save_data=False):
    global ts_db, context
    context["test_id_list"] = get_test_id_list_from_db()

    if request.method == "POST":
        try:
            context["time_form"] = DateForm()
            context["time_form"].initial["start_date"] = request.POST['start_date']
            context["time_form"].initial["start_time"] = request.POST['start_time']
            context["time_form"].initial["end_date"] = request.POST['end_date']
            context["time_form"].initial["end_time"] = request.POST['end_time']
            context["time_form"].initial["metric"] = request.POST['metric']
            context["start_date_time"] = f"{context['time_form'].initial['start_date']}T{context['time_form'].initial['start_time']}:00:00Z"
            context["end_date_time"] = f"{context['time_form'].initial['end_date']}T{context['time_form'].initial['end_time']}:00:00Z"
        except KeyError:
            print(KeyError)

    data = ts_db.get_influx_data(start_time=context["start_date_time"],
                                 end_time=context["end_date_time"],
                                 transaction=transaction_id)
    context["results"] = data["data"]
    context["time_interval"] = data["time_interval"]
    #   SAVE TEST RESULTS
    if "save_button" in request.POST.keys():
        if "TEST" in request.POST["save_button"]:
            test_id = str(request.POST["save_button"]).replace("TEST: ", "")
            save_test_data_to_db(data["data"], test_id, context["time_form"].initial["metric"])

    #   COMPARISON
    if "test_id" in request.POST.keys() and "compare_button" in request.POST.keys():
        if request.POST["test_id"]:
            return compare_test_results(request)

    return render(request, 'results/detail.html', context)


def compare_test_results(request, transaction_id=""):
        global context
        if request.method == "POST":
            print(request.POST)
            context["test_id"] = request.POST["test_id"]
        # SAVED DATA
        if transaction_id:
            context["saved_data"] = get_test_data_by_trn_from_db(context["test_id"], transaction=transaction_id)
        else:
            context["saved_data"] = get_all_test_data_grp_by_trn_from_db(request.POST["test_id"])
        # INFLUX DATA
        data = ts_db.get_influx_data(start_time=context["start_date_time"],
                                         end_time=context["end_date_time"],
                                         transaction=transaction_id)
        context["results"] = data["data"]

        return render(request, 'results/comparison.html', context)


def save_data(request):
    #   print("----------------------- SAVE DATA----------", request.POST)
    messages.info(request, 'Your password has been changed successfully!')
    return redirect("show_timeseries_db_data")
