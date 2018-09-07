from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from events import views

app_name = 'events'

urlpatterns = [
	url(r'^events/$', views.view_events, name='events')
]