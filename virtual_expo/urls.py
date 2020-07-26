from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from virtual_expo import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'virtual_expo'

urlpatterns = [
    path('virtual-expo/crowd-counting', views.crowd_counting, name='events'),
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
