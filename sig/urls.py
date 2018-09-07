from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from sig import views

app_name = 'sig'

urlpatterns = [
	url(r'^sig/$', views.view_sig, name='sig')
]