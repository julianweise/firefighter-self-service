from django.urls import path

from event.views import EventCreateView, CourseEventCreateView, EventListView

urlpatterns = [
    path('event/', EventListView.as_view(), name='event-list'),
    path('event/add', EventCreateView.as_view(), name='event-create'),
    path('event/delete', EventListView.as_view(), name='event-delete'),
    path('event/update', EventListView.as_view(), name='event-update'),
    path('course-event/add', CourseEventCreateView.as_view(), name='course-event-create'),
]
