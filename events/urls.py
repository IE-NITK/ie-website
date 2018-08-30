from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView

app_name = 'events'

urlpatterns = [
	url(r'^events/$', TemplateView.as_view(template_name='events.html'), name='home')
]