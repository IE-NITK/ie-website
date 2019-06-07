from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from alumni import views

app_name = 'alumni'

urlpatterns = [
	url(r'^alumni/$', views.view_alumni, name='alumni')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)