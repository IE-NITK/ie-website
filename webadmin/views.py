import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from accounts import views
from accounts.models import Account, Status
from webadmin.forms import AddUserForm
User = get_user_model()


def error_404_view(request, exception):
    return render(request, '404.html', locals())


def view_team(request):
    return render(request, 'events.html')


def sitemap(request):
    return render(request, 'sitemap.xml', content_type="application/xhtml+xml")


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
    if request.method == 'POST' and 'role' in request.POST:
        pk = request.POST['pk']
        role = request.POST['role']
        account = Account.objects.get(pk=pk)
        if account is not None:
            account.role = role
            account.save()
            template_data['alert_success'] = "Updated " + account.user.username + "'s role!"

    elif request.method == 'POST' and 'SIG' in request.POST:
        pk = request.POST['pk']
        SIG = request.POST['SIG']
        account = Account.objects.get(pk=pk)
        if account is not None:
            account.SIG = SIG
            account.save()
            template_data['alert_success'] = "Updated " + account.user.username + "'s SIG!"

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
                USER = user.user
            except Exception:
                template_data['alert_danger'] = "Unable to delete the user. Please try again later"
                return
            USER.delete()
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
                form.cleaned_data['member_type']
            )
            request.session['alert_success'] = "Successfully created new member account. Please ask them to change the password first"
            return HttpResponseRedirect('/admin/users/')
    else:
        form = AddUserForm()
    template_data['form'] = form
    return render(request, 'ienitk/admin/createuser.html', template_data)


# View all candidates and their status
def candidates_view(request):
    # Authentication check
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN, Account.ACCOUNT_MEMBER])
    if authentication_result is not None:
        return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Get the SIG information of the user
    current_user = request.user
    SIG_User = current_user.account.SIG
    # update status of candidates
    if request.method == 'POST':
        pk = request.POST['pk']
        status = request.POST['status']
        candidate = Status.objects.get(pk=pk)
        if candidate is not None:
            candidate.status = status
            candidate.save()
            template_data['alert_success'] = "Updated" + candidate.user.user.username + "'s status!"
    # Parse search sorting
    template_data['query'] = Status.objects.filter(SIG=SIG_User)
    return render(request, 'ienitk/admin/candidates.html', template_data)


# def download_csv(request):
#     authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN, Account.ACCOUNT_MEMBER])
#     if authentication_result is not None:
#         return authentication_result
#
#     candidates = sorted(Status.objects.all())
#
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="candidates.csv"'
#
#     writer = csv.writer(response)
#     writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
#     writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])


