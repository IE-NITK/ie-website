import csv
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from accounts import views
from accounts.models import Account, Status, BasicResponses, EscapeCounter, Profile
from webadmin.forms import AddUserForm, GetBranchNameForm
from djqscsv import render_to_csv_response
from django.core.exceptions import PermissionDenied
import subprocess
import os
from django.urls import reverse

from iewebsite import constants

User = get_user_model()


def error_404_view(request, exception):
    return render(request, '404.html', locals())


def view_team(request):
    return render(request, 'events.html')


def sitemap(request):
    return render(request, 'sitemap.xml', content_type="application/xhtml+xml")


def view_archived_users(request):
    # Authentication check.
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    template_data['query'] = Account.objects.filter(archive=True)
    return render(request, 'ienitk/admin/archived_users.html', template_data)


def restore_user(request):
    # Authentication check.
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN])
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
                return HttpResponseRedirect(reverse('webadmin:admin/users'))
            user.archive = False
            user.save()
            template_data['alert_success'] = "The user has been restored."
            return HttpResponseRedirect(reverse('webadmin:admin/users'))
    return HttpResponseRedirect(reverse('webadmin:admin/users'))


def users_view(request):
    # Authentication check
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
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
            template_data['alert_success'] = "Updated " + \
                account.user.username + "'s role!"

    if request.method == 'POST' and 'SIG' in request.POST:
        pk = request.POST['pk']
        SIG = request.POST['SIG']
        account = Account.objects.get(pk=pk)
        if account is not None:
            account.SIG = SIG
            account.save()
            template_data['alert_success'] = "Updated " + \
                account.user.username + "'s SIG!"

    # Parse search sorting
    template_data['query'] = Account.objects.filter(
        archive=False, role__in=[1, 2, 4]).order_by('-role')
    return render(request, 'ienitk/admin/users.html', template_data)


def user_archive(request):
    # Authentication check.
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view

    if request.method == 'POST':
        if 'delete' in request.POST and 'pk' in request.POST:
            pk = request.POST['pk']
            print("hi", pk)
            try:
                user = Account.objects.get(pk=pk)
            except Exception:
                template_data['alert_danger'] = "Unable to archive the user. Please try again later"
                return
            user.archive = True
            user.save()
            template_data['alert_success'] = "The user has been archived."
            return HttpResponseRedirect(reverse('webadmin:admin/users'))


def delete_user(request):
    # Authentication check.
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN])
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
                profile = Profile.objects.get(pk=pk)
                USER = user.user
            except Exception:
                template_data['alert_danger'] = "Unable to delete the user. Please try again later"
                return
            USER.delete()
            profile.delete()
            template_data['alert_success'] = "The user has been deleted."
            return HttpResponseRedirect(reverse('webadmin:admin/users'))


def add_user(request):
    # Authentication check
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
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
                0,
                "",
                True,
                form.cleaned_data['member_type']
            )
            request.session['alert_success'] = "Successfully created new member account. Please ask them to change the password first"
            return HttpResponseRedirect(reverse('webadmin:admin/users'))
    else:
        form = AddUserForm()
    template_data['form'] = form
    return render(request, 'ienitk/admin/createuser.html', template_data)


# View all candidates and their status
def all_candidates_view(request):
    # Authentication check
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN, Account.ACCOUNT_MEMBER, Account.ACCOUNT_AUX_ADMIN])
    if authentication_result is not None:
        return authentication_result

    # Get the template data from the session
    template_data = views.parse_session(request)
    # Get the SIG information of the user
    current_user = request.user

    if current_user.account.role != 1:
        return

    # update status of candidates
    if request.method == 'POST':
        pk = request.POST['pk']
        status = request.POST['status']
        candidate = Status.objects.get(pk=pk)
        if candidate is not None:
            candidate.status = status
            candidate.save()
            template_data['alert_success'] = "Updated" + \
                candidate.user.user.username + "'s status!"
    # Parse search sorting
    template_data['query'] = Account.objects.filter(role=3)

    template_data['logged_in_user'] = current_user
    return render(request, 'ienitk/admin/all_candidates.html', template_data)


# View SIG specific candidates and their status
def candidates_view(request):
    # Authentication check
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN, Account.ACCOUNT_MEMBER, Account.ACCOUNT_AUX_ADMIN])
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
            template_data['alert_success'] = "Updated" + \
                candidate.user.user.username + "'s status!"
    # Parse search sorting
    template_data['query'] = Status.objects.filter(SIG=SIG_User)
    if current_user.account.role == 4:
        template_data['query'] = Status.objects.filter(
            SIG__in=["SR", "VR", "RO", "CA", "TE"])
    template_data['logged_in_user'] = current_user
    return render(request, 'ienitk/admin/candidates.html', template_data)


def not_applied_candidate_view(request):
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN, Account.ACCOUNT_MEMBER, Account.ACCOUNT_AUX_ADMIN])
    if authentication_result is not None:
        return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)

    current_user = request.user

    if current_user.account.role != 1:
        return

    all_candidates = Account.objects.filter(role=3)
    applied_candidates = BasicResponses.objects.all()

    not_applied_candidates = []

    for candidate in all_candidates:
        flag = True
        for applied_candidate in applied_candidates:
            if(candidate == applied_candidate.user):
                flag = False
                break
        
        if(flag):
            not_applied_candidates.append(candidate)
    
    template_data['query'] = not_applied_candidates

    template_data['logged_in_user'] = current_user
    return render(request, 'ienitk/admin/not_applied_candidates.html', template_data)


def download_basic_responses_csv(request):
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN, Account.ACCOUNT_MEMBER, Account.ACCOUNT_AUX_ADMIN])
    if authentication_result is not None:
        return authentication_result
    column_mapping = {
        'user__profile__firstname': 'Firstname',
        'user__roll_no': 'Roll No',
        'ans1': 'Answer1',
        'ans2': 'Answer2',
        'ans3': 'Answer3',
        'user__profile__phone': 'Contact Number',
        'created_at': 'Create At'
    }

    responses = BasicResponses.objects.values(
        'user__profile__firstname', 'user__roll_no', 'ans1', 'ans2', 'ans3', 'user__profile__phone', 'created_at')
    return render_to_csv_response(responses, filename=u'Candidates_responses.csv', field_header_map=column_mapping)


def download_esc_count_csv(request):
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN, Account.ACCOUNT_MEMBER, Account.ACCOUNT_AUX_ADMIN])
    if authentication_result is not None:
        return authentication_result
    column_mapping = {
        'user__profile__firstname': 'Firstname',
        'user__roll_no': 'Roll No',
        'user__esc_counter': 'Escape Count',
        'user__profile__phone': 'Contact Number',
        'pressed_at': 'Pressed At'
    }

    responses = EscapeCounter.objects.values(
        'user__profile__firstname', 'user__roll_no', 'user__esc_counter', 'user__profile__phone', 'pressed_at')
    return render_to_csv_response(responses, filename=u'Candidate Escape Responses.csv', field_header_map=column_mapping)


def update_status(request):
    # Authentication check
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
    
    all_status = Status.objects.filter(status="RE")
    
    for entry in all_status:
        entry.status = "NS"
        entry.save()

    return HttpResponseRedirect('/profile')


def download_selected_candidates(request):
    # Authentication check
    authentication_result = views.authentication_check(
        request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
    
    all_status = Status.objects.filter(status="TE")

    SIGs = { "CO": 3, "GD": 4, "GR": 5, "CA": 6, "RO": 7, "SR": 8, "TE": 9}

    candidates = {}
    
    for entry in all_status:
        candidates[f"{entry.user.roll_no}"] = [f"{entry.user.profile.firstname}", f"{entry.user.profile.lastname}", f"{entry.user.profile.phone}", 0, 0, 0, 0, 0, 0, 0]
    
    for entry in all_status:
        candidates[f"{entry.user.roll_no}"][SIGs[entry.SIG]] = 1
    
    response = HttpResponse(
        content_type='text/csv',
    )

    response['Content-Disposition'] = 'attachment; filename="selectedcandidates.csv"'
    
    writer = csv.writer(response)

    writer.writerow(["First Name", "Last Name", "Roll No.", "Mobile Number", "Code", "Gadget", "Garage", "Capital", "Robotics", "Script", "Tectonic"])

    for key in candidates:
        writer.writerow([candidates[key][0], candidates[key][1], key, candidates[key][2], candidates[key][3], candidates[key][4], candidates[key][5], candidates[key][6], candidates[key][7], candidates[key][8], candidates[key][9]])

    return response


def executeCommand(cmd, output):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        print("success")
        return output


    else:
        # handle error
        output = output + repr(stdout) + "\n"
        output = output + repr(stderr) + "\n"
        return output

def executeSudoCommand(cmd, output):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                                      universal_newlines=True)
    stdout, stderr = p.communicate(constants.SERVER_PASSWORD+'\n')
    if p.returncode == 0:
        print("success")
        return output

    else:
        # handle error
        output = output + repr(stdout) + "\n"
        output = output + repr(stderr) + "\n"
        return output

def deploy_website(request):
    # Only deploy for Superusers
    if request.user.is_superuser:
        template_data = {}
        # Getting branch name to deploy
        if request.method == 'POST':
            form = GetBranchNameForm(request.POST)
            if form.is_valid():
                branch_name = form.cleaned_data["branch_name"]
                prevdir = os.getcwd()
                # Get all errors as output in html
                output = "" 
            
                # Changing directory to the project directory
                os.chdir("/home/ie/newsite/ie-website")
                # Checkout to given branch
                output = executeCommand(['git', 'checkout', branch_name], output)
                output = executeCommand(['git', 'pull', 'origin', branch_name], output)
                # output = executeCommand(['.', '../venv/bin/activate'], output)
                # os.system(". ../bin/activate")
                activate_this = "/home/ie/newsite/bin/activate"
                with open(activate_this) as f:
                        code = compile(f.read(), activate_this, 'exec')
                        exec(code, dict(__file__=activate_this))
                output = executeCommand(
                    ["python3", "manage.py", "makemigrations"], output)
                output = executeCommand(["python3", "manage.py", "migrate"], output)
                output = executeSudoCommand(["sudo", "-S", "systemctl", "restart", "gunicorn"], output)
                os.chdir(prevdir)
                request.session['alert_success'] = "Successfully deployed to " + \
                    branch_name + " branch"
                template_data["output"] = output
                
                return render(request, 'ienitk/admin/deploy-errors.html', template_data)
                
        else:
            form = GetBranchNameForm()
        template_data['form'] = form
        return render(request, 'ienitk/admin/deploy.html', template_data)
    else:
        request.session['alert_danger'] = "You don't have permission to view the page."
        return HttpResponseRedirect(reverse('accounts:error_denied'))
