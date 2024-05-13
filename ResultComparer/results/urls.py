from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:app_id>/', views.detail, name='detail'),
    path('detail/<str:app_id>/', views.detail, name='detail'),
    path('results/', views.show_influx_data, name='show_influx_data'),
    path('results/<str:transaction_id>/', views.show_influx_data, name='show_influx_data'),
]