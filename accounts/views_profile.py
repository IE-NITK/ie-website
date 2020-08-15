from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import datetime
from .forms import PasswordForm, ProfileForm, SIGForm
from .models import Account, Status, RoundOneSubmission
from . import views
from django.http import Http404


def profile_view(request):
    # Authentication check
    authentication_result = views.authentication_check(request)
    if authentication_result is not None:
        return authentication_result
    # Get template data from session
    template_data = views.parse_session(request)

    # Passing profile to template data
    current_user = request.user
    account = Account.objects.get(user=current_user)
    profile = account.profile
    template_data["profile"] = profile

    # Checking if the candidate applied for Script (online test link to be provided)
    account = current_user.account

    registered_sigs = Status.objects.filter(user=account)
    applied_for_script = False
    for entry in registered_sigs:
        if entry.SIG == "SR":
            applied_for_script = True
    template_data["applied_for_script"] = applied_for_script
    # passing status of the user to html
    status = Status.objects.filter(user=account)
    # flag = 0 means not selected
    flag = 0
    for entry in status:
        if entry.status == 'SL':
            flag = 1
    template_data["selected"] = flag
    # Proceed with rest of the view
    return render(request, 'ienitk/profile.html', template_data)


def password_view(request):
    # Authentication check
    authentication_result = views.authentication_check(request)
    if authentication_result is not None:
        return authentication_result
    # Get template data from session
    template_data = views.parse_session(
        request, {'form_button': "Change password"})
    # Proceed with rest of the view
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username,
                                password=form.cleaned_data['password_current'])
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
    if authentication_result is not None:
        return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(
        request, {'form_button': "Update profile"})
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
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN, Account.ACCOUNT_CANDIDATE])
    if authentication_result is not None:
        return authentication_result
    template_data = views.parse_session(request, {'form_button': "Submit"})

    account = Account.objects.get(user=request.user)

    stat = Status.objects.filter(user=account).first()

    if stat is None:
        if request.method == 'POST':
            form = SIGForm(request.POST)
            if form.is_valid():
                views.register_SIG(
                    form.cleaned_data['SigMain1'],
                    account,
                    datetime.datetime.now(),
                    "RE"
                )

                views.register_SIG(
                    form.cleaned_data['SigMain2'],
                    account,
                    datetime.datetime.now(),
                    "RE"
                )

                views.register_SIG(
                    form.cleaned_data['SigAux1'],
                    account,
                    datetime.datetime.now(),
                    "RE"
                )

                views.register_SIG(
                    form.cleaned_data['SigAux2'],
                    account,
                    datetime.datetime.now(),
                    "RE"
                )

                views.register_SIG(
                    form.cleaned_data['SigAux3'],
                    account,
                    datetime.datetime.now(),
                    "RE"
                )

                views.register_question_responses(
                    form.cleaned_data['quesn1'],
                    form.cleaned_data['quesn2'],
                    form.cleaned_data['quesn3'],
                    account,
                    datetime.datetime.now()
                )

                request.session['alert_success'] = "Successfully registered the SIGs with the portal."
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

                applied_for_script = False
                for entry in registered_sigs:
                    if entry.SIG == "SR":
                        applied_for_script = True
                return render(request, 'ienitk/status.html', {'query': final_cleaned_data, 'applied_for_script': applied_for_script})
            else:
                return render(request, 'ienitk/apply.html', template_data)
        else:
            form = SIGForm()
        template_data['form'] = form
        return render(request, 'ienitk/apply.html', template_data)
    else:
        request.session['alert_danger'] = "You have already registered! If this was a mistake contact Chaitany : +91 9834708844"
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

    applied_for_script = False

    for entry in registered_sigs:
        if entry.SIG == "SR":
            applied_for_script = True

    return render(request, 'ienitk/status.html',
                  {'query': final_cleaned_data, 'applied_for_script': applied_for_script})


def scriptroundone(request):
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_CANDIDATE])
    if authentication_result is not None:
        return authentication_result
    account = Account.objects.get(user=request.user)
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

    applied_for_script = False
    for entry in registered_sigs:
        if entry.SIG == "SR":
            applied_for_script = True

    if applied_for_script is True:
        return render(request, 'ienitk/scriptroundone.html')
    else:
        request.session['alert_danger'] = "You haven't registered for the Script SIG to be part of the round!"
        return HttpResponseRedirect('/profile/')


def submission_scriptroundone(request):
    if request.method == 'POST':
        ans1 = request.POST.get('ans1', None)
        ans2 = request.POST.get('ans2', None)
        ans3 = request.POST.get('ans3', None)
        ans4 = request.POST.get('ans4', None)
        ans5 = request.POST.get('ans5', None)
        essayans = request.POST.get('essayans', None)
        created = datetime.datetime.now()
        current_user = request.user
        account = current_user.account
        submission = RoundOneSubmission.create(
            account, ans1, ans2, ans3, ans4, ans5, essayans, created)
        submission.save()
    return HttpResponseRedirect('/profile/')


def test_round_1(request):

    return render(request, 'ienitk/roundone.html')
