from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path

from . import views
from . import views_home
from . import views_profile
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
  path('login/', views_home.login_view, name='index'),
  path('setup/', views_home.setup_view, name='setup'),
  path('register/', views_home.register_view, name='register'),
  path('activate/<uidb64>/<token>/', views_home.activate, name='activate'),
  path('logout/', views_home.logout_view, name='logout'),
  path('profile/', views_profile.profile_view, name='profile'),
  path('profile/update/', views_profile.profile_update, name='profile/update'),
  path('profile/password/', views_profile.password_view, name='profile/password'),
  path('profile/apply/', views_profile.apply, name='profile/apply'),
  path('profile/status/', views_profile.status, name='status'),
  # path('scriptroundone/', views_profile.scriptroundone, name='scriptroundone' ),
  # path('scriptroundone/submission_scriptroundone/',views_profile.submission_scriptroundone,name="submission_scriptroundone"),
  path('beta-testing/round-1',views_profile.test_round_1,name='round_1_test'),
  path('profile/update_counter/', views_profile.update_esc_counter, name = 'update_esc_counter')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
