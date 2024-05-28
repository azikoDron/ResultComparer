from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:app_id>/', views.detail, name='detail'),
    path('detail/<str:app_id>/', views.detail, name='detail'),
    path('results/', views.show_timeseries_db_data, name='show_timeseries_db_data'),
    path('results/<str:transaction_id>/', views.show_timeseries_db_data, name='show_timeseries_db_data'),
    path('compare/<str:transaction_id>/', views.compare_test_results, name='compare_test_results'),
    path('save_data/', views.save_data, name='save_data'),
]