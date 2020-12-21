"""firefighter_self_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('overview/', include('overview.urls')),
                  path('personal-data/', include('personal_data.urls')),
                  path('equipment/', include('equipment.urls')),
                  path('attendance/', include('attendance.urls')),
                  path('fitness/', include('fitness.urls')),
                  path('events/', include('event.urls')),
                  path('qualification/', include('qualification.urls')),
                  path('accounts/login/', auth_views.LoginView.as_view()),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('', RedirectView.as_view(url='overview/', permanent=True))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
