from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from events import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'events'

urlpatterns = [
    path('events/', views.view_events, name='events'),
    path('smp2019/', views.smp2019, name='smp2019'),
    path('smp2020/', views.smp2020, name='smp2020'),
    path('hackverse/', views.hackverse, name='hackverse'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
