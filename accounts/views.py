from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import datetime
from .models import Account, Profile, Status, ActivationRecord, BasicResponses
from django.views.generic import View
from django.template.loader import get_template
from django.shortcuts import render


def authentication_check(request, required_roles=None, required_GET=None):
    """
    :param request: page request
    :param required_roles: role values of users allowed to view the page
    :param required_GET: GET values that the page needs to function properly
    :return: A redirect request if there's a problem, None otherwise
    """
    # Authentication check. Users not logged in cannot view the page
    if not request.user.is_authenticated:
        request.session['alert_danger'] = "You must be logged in to view the page."
        return HttpResponseRedirect('/login/')
    # Sanity Check. Users without accounts cannot interact with virtual clinic
    try:
        request.user.account
    except ObjectDoesNotExist:
        request.session['alert_danger'] = "Your account was not properly created, please try a different account."
        return HttpResponseRedirect('/logout/')
    # Permission check
    if required_roles and request.user.account.role not in required_roles:
        request.session['alert_danger'] = "You don't have permission to view the page."
        return HttpResponseRedirect('/error/denied/')
    # Validation check. Make sure this page has any required GET keys
    if required_GET:
        for key in required_GET:
            if key not in request.GET:
                request.session['alert_danger'] = "Looks like you tried to use a malformed URL."
                return HttpResponseRedirect('/error/denied/')


def parse_session(request, template_data=None):
    """
    Checks the session for any alert data. If there is alert data, it added to the given template data.
    :param request: The request to check session data for
    :param template_data: The dictionary to update
    :return: The updated dictionary
    """
    if template_data is None:
        template_data = {}
    if request.session.has_key('alert_success'):
        template_data['alert_success'] = request.session.get('alert_success')
        del request.session['alert_success']
    if request.session.has_key('alert_danger'):
        template_data['alert_danger'] = request.session.get('alert_danger')
        del request.session['alert_danger']
    return template_data


def register_user(email, password, first_name, last_name, phone, roll_no, active, role):
    user = User.objects.create_user(
        email.lower(),
        email.lower(),
        password,
        is_active=active
    )
    profile = Profile(
        firstname=first_name,
        lastname=last_name,
        phone=phone,
    )
    profile.save()
    account = Account(
        role=role,
        profile=profile,
        user=user,
        roll_no=roll_no,
    )
    account.save()

    return user


def activate_candidate(user):
    record = user.activationrecord
    profile = Profile(
        firstname=record.firstname,
        lastname=record.lastname,
        phone=record.phone,
    )
    profile.save()
    account = Account(
        role=Account.ACCOUNT_CANDIDATE,
        profile=profile,
        user=user,
        roll_no=record.roll_no,
    )
    account.save()
    record.delete()

    return


def register_candidate(email, password, first_name, last_name, phone, roll_no):
    user = User.objects.create_user(
        email.lower(),
        email.lower(),
        password,
        is_active=False
    )

    record = ActivationRecord(
        user=user,
        firstname=first_name,
        lastname=last_name,
        phone=phone,
        roll_no=roll_no,
    )
    record.save()

    return user


def register_SIG(SIG, user, updated_at, status):
    if SIG != "":
        status = Status(
            user=user,
            updated_at=updated_at,
            status=status,
            SIG=SIG
        )
        existing_status = Status.objects.filter(user=user)
        if status.SIG not in existing_status.values_list('SIG', flat=True):
            status.save()


def sanitize_js(string):
    return string.replace("\\", "\\\\").replace("'", "\\'")


def register_question_responses(ans1, ans2, ans3, user, updated_at):
    responses = BasicResponses(
        user=user,
        ans1=ans1,
        ans2=ans2,
        ans3=ans3,
        created_at=updated_at
    )
    responses.save()


def is_eligible(registered_sigs, sig):
    if registered_sigs.__contains__(sig):
        return True
    else:
        return False
