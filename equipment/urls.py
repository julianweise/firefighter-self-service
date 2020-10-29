from django.urls import path

from .views import PersonalEquipmentView, PagerDetailView, KeyDetailView, LockerDetailView

urlpatterns = [
    path('personal/', PersonalEquipmentView.as_view(), name='equipment-personal'),
    path('pager/<int:pk>/', PagerDetailView.as_view(), name='pager-detail'),
    path('key/<int:pk>/', KeyDetailView.as_view(), name='key-detail'),
    path('locker/<int:pk>/', LockerDetailView.as_view(), name='locker-detail')
]
