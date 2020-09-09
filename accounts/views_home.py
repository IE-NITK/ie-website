from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token


from .forms import LoginForm, AccountRegisterForm
from .models import Account, ActivationRecord
from . import views


def setup_view(request):
    if Account.objects.all().count() > 0:
        request.session['alert_success'] = "Setup has already been completed."
        return HttpResponseRedirect('/')
    # Get template data from the session
    template_data = views.parse_session(request, {'form_button': "Register"})
    # Proceed with rest of the view
    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            views.register_user(
                form.cleaned_data['email'],
                form.cleaned_data['password_first'],
                form.cleaned_data['firstname'],
                form.cleaned_data['lastname'],
                0,
                "",
                True,
                Account.ACCOUNT_ADMIN
            )
            user = authenticate(
                # Make sure it's lowercase
                username=form.cleaned_data['email'].lower(),
                password=form.cleaned_data['password_first']
            )
            login(request, user)
            request.session['alert_success'] = "Successfully setup IE NITK primary admin account."
            return HttpResponseRedirect('/profile/')
    else:
        form = AccountRegisterForm()
    template_data['form'] = form
    return render(request, 'ienitk/setup.html', template_data)


def logout_view(request):
    saved_data = {}
    if request.session.has_key('alert_success'):
        saved_data['alert_success'] = request.session['alert_success']
    else:
        saved_data['alert_success'] = "You have successfully logged out."
    if request.session.has_key('alert_danger'):
        saved_data['alert_danger'] = request.session['alert_danger']
    logout(request)
    if 'alert_success' in saved_data:
        request.session['alert_success'] = saved_data['alert_success']
    if 'alert_danger' in saved_data:
        request.session['alert_danger'] = saved_data['alert_danger']
    return HttpResponseRedirect('/')


def login_view(request):
    # Authentication check. Users currently logged in cannot view this page.
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    elif Account.objects.all().count() == 0:
        return HttpResponseRedirect('/setup/')
    # get template data from session
    template_data = views.parse_session(request, {'form_button': "Login"})
    # Proceed with the rest of view
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['email'].lower(),
                password=form.cleaned_data['password']
            )
            login(request, user)
            request.session['alert_success'] = "Successfully logged in."
            return HttpResponseRedirect('/profile')
    else:
        form = LoginForm()
    template_data['form'] = form
    return render(request, 'ienitk/login.html', template_data)


# For allowing registration
def register_view(request):
    # Authentication check. Users logged in cannot view this page.

    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    elif Account.objects.all().count() == 0:
        return HttpResponseRedirect('/setup/')
    # Get template data from session
    template_data = views.parse_session(request, {'form_button': "Register"})
    # Proceed with rest of the view

    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():

            user = views.register_candidate(
                form.cleaned_data['email'],
                form.cleaned_data['password_first'],
                form.cleaned_data['firstname'],
                form.cleaned_data['lastname'],
                form.cleaned_data['phone'],
                form.cleaned_data['roll_no'],
            )
            # Getting firstname of user for mail
            account = ActivationRecord.objects.get(user=user)
            firstname = account.firstname
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'

            message = render_to_string('ienitk/acc_active_email.html', {
                'user': user,
                'firstname': firstname,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data['email']
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()

            return render(request, 'ienitk/activation_requested.html')
    else:
        form = AccountRegisterForm()
    template_data['form'] = form
    return render(request, 'ienitk/register.html', template_data)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print(account_activation_token.check_token(user, token))
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        views.activate_candidate(user)
        # return redirect('home')
        request.session['alert_success'] = "Successfully registered with the portal."

        return HttpResponseRedirect('/profile/apply')
    else:
        return HttpResponse('Activation link is invalid!')


def error_denied_view(request):
    # Authentication check
    authentication_result = views.authentication_check(request)
    if authentication_result is not None:
        return authentication_result
    # Get template data from session
    template_data = views.parse_session(request)
    # Proceed with rest of the view
    return render(request, 'ienitk/error_denied.html', template_data)
