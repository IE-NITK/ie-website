
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views
from . import views_home
from . import views_profile


app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', views_home.login_view, name='index'),
    url(r'^setup/$', views_home.setup_view, name='setup'),
    url(r'^register/$', views_home.register_view, name='register'),
    url(r'^logout/$', views_home.logout_view, name='logout'),
    url(r'^profile/$', views_profile.profile_view, name='profile'),
    url(r'^profile/update/$', views_profile.profile_update, name='profile/update'),
    url(r'^profile/password/$', views_profile.password_view, name='profile/password'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)