from django.urls import path

from overview.views import OverviewView

urlpatterns = [
    path('', OverviewView.as_view(), name='overview'),
]
