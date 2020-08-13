from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from webadmin import views
from django.urls import path

app_name = 'webadmin'

urlpatterns = [
    path('sitemap/', views.sitemap, name='sitemap'),
    path('team/', views.view_team, name='team'),
    path('admin/users/', views.users_view, name='admin/users'),
    path('admin/archive_user', views.user_archive, name='admin/archive_user'),
    path('admin/archived_users', views.view_archived_users, name='admin/archived_users'),
    path('admin/restore_users', views.restore_user, name='admin/restore_users'),
    path('admin/delete_user', views.delete_user, name='admin/delete_user'),
    path('admin/adduser/', views.add_user, name='admin/adduser'),
    path('candidates/', views.candidates_view, name='candidates'),
    path('all_candidates/', views.all_candidates_view, name='all_candidates'),
    path('download_responses_csv/', views.download_basic_responses_csv, name = 'download_responses_csv')
]
