"""iewebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', TemplateView.as_view(template_name='index.html'), name='home'),
                  path('ie-stories/', TemplateView.as_view(template_name='ie-stories.html'), name='ie-stories'),
                  path('workshop/', TemplateView.as_view(template_name='sixth-sense-workshop.html'), name='workshop'),
                  path('flappy/', TemplateView.as_view(template_name='flappy.html'), name='flappy'),
                  path('enigma/', TemplateView.as_view(template_name='enigma.html'), name="enigma"),
                  path('', include('webadmin.urls', namespace="webadmin")),
                  path('', include('sig.urls', namespace="sig")),
                  path('', include('events.urls', namespace="events")),
                  path('', include('accounts.urls', namespace="accounts")),
                  path('', include('teams.urls', namespace="teams")),
                  path('', include('alumni.urls', namespace="alumni")),
                  path('', include('virtual_expo.urls', namespace="virtual_expo")),
                  path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(),
                       name='password_reset_complete')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
