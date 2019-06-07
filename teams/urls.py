from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from teams import views

app_name = 'teams'

urlpatterns = [
	path('teams/', views.view_teams, name='teams')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)