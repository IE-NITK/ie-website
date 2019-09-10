from django.shortcuts import render
import json
import os
from django.conf import settings


def view_sig(request):
    return render(request, 'sig.html')


def view_projects(request, sig):
    # code = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'odeprojects2019.json')).read())
    # gadget = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'gadgetprojects2019.json')).read())
    projects = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], sig+'projects2019.json')).read())

    context = {'sig': sig, 'projects': projects}
    return render(request, 'projects.html', context)
