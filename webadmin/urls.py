from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from webadmin import views

app_name = 'webadmin'

urlpatterns = [
	url(r'^team/$', views.view_team, name='team')
]
