from django.urls import path

from statistics.views import StatisticsAllListView

urlpatterns = [
    path('all/', StatisticsAllListView.as_view(), name='statistics-all')
]
