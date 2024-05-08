from django.http import HttpResponse
from django.shortcuts import render
from .models import Apps
from .influx_db import get_influx_available_transactions, get_influx_data


def index(request):
    # cards = {'available_cards': available_cards.keys()}
    cards = {'available_apps': Apps.objects.all()}
    return render(request, 'results/index.html', cards)


def detail(request, app_id):
    if app_id == "Результаты НТ":
        return render(request, 'results/detail.html', {"results": get_influx_data()})
    else:
        data = Apps.objects.get(name=app_id)
        app_detail = {"app_detail": data}
        return render(request, 'results/detail.html', app_detail)


def show_influx_available_transactions(request):
    return render(request, 'results/detail.html', {"transactions": get_influx_available_transactions()})


def show_influx_data(request, transaction_id=""):
    return render(request, 'results/comparison.html', {"results": get_influx_data()})
