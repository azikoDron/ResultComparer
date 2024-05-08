from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:app_id>/detail', views.detail, name='detail'),
    path('<str:app_id>/detail', views.detail, name='detail'),
    path('<str:transaction_id>/results', views.show_influx_data, name='show_influx_data'),
]