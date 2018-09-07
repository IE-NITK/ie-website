from django.shortcuts import render
from django.shortcuts import render
import sys
from django.core.management import call_command
from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.db.utils import IntegrityError

from accounts import views
from accounts.models import Account
from webadmin.forms import AddUserForm


def error_404_view(request, exception):
	return render(request, '404.html', locals())

def view_team(request):
	return render(request, 'events.html')


def view_archived_users(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    template_data['query'] = Account.objects.filter(archive=True)
    return render(request, 'ienitk/admin/archived_users.html', template_data)


def restore_user(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    if request.method == 'POST':
        if 'restore' in request.POST and 'pk' in request.POST:
            pk = request.POST['pk']
            try:
                user = Account.objects.get(pk=pk)
            except Exception:
                template_data['alert_danger'] = "Unable to delete the user. Please try again later"
                return HttpResponseRedirect('/admin/users')
            user.archive = False
            user.save()
            template_data['alert_success'] = "The user has been restored."
            return HttpResponseRedirect('/admin/users')
    return HttpResponseRedirect('/admin/users')


def users_view(request):
    # Authentication check
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    if request.method == 'POST':
        pk = request.POST['pk']
        role = request.POST['role']
        account = Account.objects.get(pk=pk)
        if account is not None:
            account.role = role
            account.save()
            template_data['alert_success'] = "Updated" + account.user.username + "'s role!"
    # Parse search sorting
    template_data['query'] = Account.objects.filter(archive=False).order_by('-role')
    return render(request, 'ienitk/admin/users.html', template_data)


def user_archive(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    if request.method == 'POST':
        if 'delete' in request.POST and 'pk' in request.POST:
            pk = request.POST['pk']
            try:
                user = Account.objects.get(pk=pk)
            except Exception:
                template_data['alert_danger'] = "Unable to archive the user. Please try again later"
                return
            user.archive = True
            user.save()
            template_data['alert_success'] = "The user has been archived."
            return HttpResponseRedirect('/admin/users')


def delete_user(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    if request.method == 'POST':
        if 'delete' in request.POST and 'pk' in request.POST:
            pk = request.POST['pk']
            try:
                user = Account.objects.get(pk=pk)
            except Exception:
                template_data['alert_danger'] = "Unable to delete the user. Please try again later"
                return
            user.delete()
            template_data['alert_success'] = "The user has been deleted."
            return HttpResponseRedirect('/admin/users')


def add_user(request):
    # Authentication check
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': "Register"})
    # Proceed with the rest of the view
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = views.register_user(
                form.cleaned_data['email'],
                form.cleaned_data['password_first'],
                form.cleaned_data['firstname'],
                form.cleaned_data['lastname'],
                False,
                form.cleaned_data['employee']
            )
            request.session['alert_success'] = "Successfully created new employee account"
            return HttpResponseRedirect('/admin/users/')
    else:
        form = AddUserForm()
    template_data['form'] = form
    return render(request, 'ienitk/admin/createuser.html', template_data)