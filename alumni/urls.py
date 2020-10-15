from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from alumni import views

app_name = 'alumni'

urlpatterns = [
	path('alumni/', views.view_alumni, name='alumni'),
	path('alumni/<int:year>', views.view_alumni, name='alumni')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)