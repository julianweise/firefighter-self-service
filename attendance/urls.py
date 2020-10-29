from django.urls import path

from attendance.views import OperationListView, OtherServiceListView, AttendanceListView, OperationDelete, \
    TrainingDelete, \
    OtherServiceDelete, OperationUpdateView, \
    OperationCreateView, TrainingListView, TrainingCreateView, TrainingUpdateView, OtherServiceCreateView, \
    OtherServiceUpdateView, TrainingParticipatedListView

urlpatterns = [
    path('all/', AttendanceListView.as_view(), name='attendance-list'),
    path('operation/', OperationListView.as_view(), name='operation-list'),
    path('operation/add/', OperationCreateView.as_view(), name='operation-add'),
    path('operation/<int:pk>/edit/', OperationUpdateView.as_view(), name='operation-update'),
    path('operation/<int:pk>/delete/', OperationDelete.as_view(), name='operation-delete'),
    path('training/', TrainingListView.as_view(), name='training-list'),
    path('training-participated/', TrainingParticipatedListView.as_view(), name='training-participated-list'),
    path('training/add/', TrainingCreateView.as_view(), name='training-add'),
    path('training/<int:pk>/edit/', TrainingUpdateView.as_view(), name='training-update'),
    path('training/<int:pk>/delete/', TrainingDelete.as_view(), name='training-delete'),
    path('other_service/', OtherServiceListView.as_view(), name='other_service-list'),
    path('other_service/add/', OtherServiceCreateView.as_view(), name='other_service-add'),
    path('other_service/<int:pk>/edit/', OtherServiceUpdateView.as_view(), name='other_service-edit'),
    path('other_service/<int:pk>/delete/', OtherServiceDelete.as_view(), name='other_service-delete'),
]
