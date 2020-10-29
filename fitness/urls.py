from django.urls import path

from fitness.views import FitnessPersonalListView, FitnessCreateForFirefighterView

urlpatterns = [
    path('personal/', FitnessPersonalListView.as_view(), name='fitness-personal-list'),
    path('create-for/<int:pk>/', FitnessCreateForFirefighterView.as_view(), name='fitness-create-for-firefighter'),
]
