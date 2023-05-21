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
    path('smp2021/', views.smp2021, name='smp2021'),
    path('smp2022/', views.smp2022, name='smp2022'),
    path('smp2023/', views.smp2023, name='smp2023'),
    path('hackverse/', views.hackverse, name='hackverse'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
