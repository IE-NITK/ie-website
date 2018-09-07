from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from webadmin import views

app_name = 'webadmin'

urlpatterns = [
	url(r'^team/$', views.view_team, name='team'),
	url(r'^admin/users/$', views.users_view, name='admin/users'),
    url(r'^admin/archive_user', views.user_archive, name='admin/archive_user'),
    url(r'^admin/archived_users', views.view_archived_users, name='admin/archived_users'),
    url(r'^admin/restore_users', views.restore_user, name='admin/restore_users'),
    url(r'^admin/delete_user', views.delete_user, name='admin/delete_user'),
    url(r'^admin/adduser/$', views.add_user, name='admin/adduser'),
]
