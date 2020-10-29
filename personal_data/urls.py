from django.urls import path

from . import views

urlpatterns = [
    path('', views.PersonalDataPersonalUpdateView.as_view(), name='personal-data-update'),
    path('all/', views.PersonalDataListView.as_view(), name='firefighter-list'),
    path('<int:pk>/', views.PersonalDataDetailView.as_view(), name='firefighter-detail'),
    path('add/', views.PersonalDataCreateView.as_view(), name='firefighter-add'),
    path('<int:pk>/update/', views.PersonalDataUpdateView.as_view(), name='firefighter-update'),
    path('<int:pk>/delete/', views.PersonalDataDeleteView.as_view(), name='firefighter-delete'),
    path('rank-assignment/create-for/<int:pk>', views.RankAssignmentCreateForFirefighterView.as_view(),
         name="promote-firefighter"),
    path('driver-license/create-for/<int:pk>', views.DriverLicenseCreateForFirefighterView.as_view(),
         name='license-create-for-firefighter'),
    path('honor-assignment/create-for/<int:pk>', views.HonorAssignmentCreateForFirefighterView.as_view(),
         name='honor-assignment-create-for-firefighter'),
    path('role-assignment/create-for/<int:pk>', views.RoleAssignmentCreateForFirefighterView.as_view(),
         name='role-assignment-create-for-firefighter'),
]
