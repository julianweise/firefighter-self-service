from django.urls import path

from qualification.views import QualificationPersonalListView, QualificationCreateForFirefighterView

urlpatterns = [
    path('personal/', QualificationPersonalListView.as_view(), name='qualification-personal'),
    path('create-for/<int:pk>/', QualificationCreateForFirefighterView.as_view(),
         name='qualification-create-for-firefighter'),
]
