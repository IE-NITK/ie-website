from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from teams import views

app_name = 'teams'

urlpatterns = [
	url(r'^teams/$', views.view_teams, name='teams')
]