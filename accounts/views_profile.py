from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import datetime
from .forms import PasswordForm, ProfileForm, SIGForm
from .models import Account, Status
from . import views
from django.http import Http404

def profile_view(request):
    # Authentication check
    authentication_result = views.authentication_check(request)
    if authentication_result is not None:
        return authentication_result
    # Get template data from session
    template_data = views.parse_session(request)
    # Proceed with rest of the view
    return render(request, 'ienitk/profile.html', template_data)


def password_view(request):
    # Authentication check
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    # Get template data from session
    template_data = views.parse_session(request, {'form_button': "Change password"})
    # Proceed with rest of the view
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['password_current'])
            if user is None:
                form.mark_error('password_current', 'Incorrect Password')
            else:
                user = request.user
                user.set_password(form.cleaned_data['password_first'])
                user.save()
                form = PasswordForm()  # Clean the form when the page is redisplayed
                template_data['alert_success'] = "Your password has been changed"
    else:
        form = PasswordForm()
    template_data['form'] = form
    return render(request, 'ienitk/profile/password.html', template_data)


def profile_update(request):
    # Authentication check.
    authentication_result = views.authentication_check(request)
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request, {'form_button': "Update profile"})
    # Proceed with the rest of the view
    profile = request.user.account.profile
    if request.method == 'POST':
        if request.user.account.role != Account.ACCOUNT_MEMBER:
            form = ProfileForm(request.POST)
        else:
            form = ProfileForm(request.POST)
        if form.is_valid():
            form.assign(profile)
            profile.save()
            template_data['alert_success'] = "Your profile has been updated!"
    else:
        if request.user.account.role != Account.ACCOUNT_MEMBER:
            form = ProfileForm(profile.get_populated_fields())
        else:
            form = ProfileForm(profile.get_populated_fields())
    template_data['form'] = form
    return render(request, 'ienitk/profile/update.html', template_data)


def apply(request):
    authentication_result = views.authentication_check(request,[Account.ACCOUNT_ADMIN, Account.ACCOUNT_CANDIDATE])
    if authentication_result is not None: return authentication_result
    template_data = views.parse_session(request, {'form_button': "Submit"})

    account = Account.objects.get(pk=request.user.id)

    stat = Status.objects.filter(user=account).first()

    
    if stat is None:
        if request.method == 'POST':
            form = SIGForm(request.POST)
            if form.is_valid():
                i = 0
                if i == 0:
                    views.register_SIG(
                        form.cleaned_data['SigMain1'],
                        account,
                        datetime.datetime.now(),
                        "WR"
                    )
                    i = i + 1
                if i == 1:
                    views.register_SIG(
                        form.cleaned_data['SigMain2'],
                        account,
                        datetime.datetime.now(),
                        "WR"
                    )
                    i = i + 1
                if i == 2:
                    views.register_SIG(
                        form.cleaned_data['SigAux1'],
                        account,
                        datetime.datetime.now(),
                        "WR"
                    )
                    i = i + 1
                if i == 3:
                    views.register_SIG(
                        form.cleaned_data['SigAux2'],
                        account,
                        datetime.datetime.now(),
                        "WR"
                    )
                    i = i + 1
            request.session['alert_success'] = "Successfully registered SIGS with the portal."
            registered_sigs = Status.objects.filter(user=account)
            final_cleaned_data = []
            DB_Status = Status.STATUS_TYPES
            DB_SIG = Status.SIG_TYPES
            for entry in registered_sigs:
                for type in DB_SIG:
                    if entry.SIG == type[0]:
                        sig_name = type[1]
                for status in DB_Status:
                    if entry.status == status[0]:
                        sig_status = status[1]
                final_cleaned_data.append([sig_name, sig_status])
            return render(request, 'ienitk/status.html', {'query': final_cleaned_data})
        else:
            form = SIGForm()
        template_data['form'] = form
        return render(request, 'ienitk/apply.html', template_data)
    else:
        request.session['alert_success'] = "Already registered."
        return HttpResponseRedirect('/profile/')

def status(request):
    current_user = request.user
    account = current_user.account
    # account = Account.objects.get(pk=request.user.id)
    registered_sigs = Status.objects.filter(user=account)
    final_cleaned_data = []
    DB_Status = Status.STATUS_TYPES
    DB_SIG = Status.SIG_TYPES
    for entry in registered_sigs:
        for type in DB_SIG:
            if entry.SIG == type[0]:
                sig_name = type[1]
        for status in DB_Status:
            if entry.status == status[0]:
                sig_status = status[1]
        final_cleaned_data.append([sig_name, sig_status])
    return render(request, 'ienitk/status.html', {'query': final_cleaned_data})
