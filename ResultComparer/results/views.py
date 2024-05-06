from django.http import HttpResponse
from django.shortcuts import render
from .models import Apps

def index(request):
    # cards = {'available_cards': available_cards.keys()}
    cards = {'available_apps': Apps.objects.all()}
    return render(request, 'results/index.html', cards)

def detail(request, app_id):
    # card_detail = available_cards.get(card_id)
    app_detail = {"app_detail": Apps.objects.get(name=app_id),
                   'available_apps': Apps.objects.all()}
    # return HttpResponse(f'This is {card_detail} card ')
    return render(request, 'results/detail.html', app_detail)


def show_available_options_in_main():
    return HttpResponse("Hello from django")