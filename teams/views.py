from django.shortcuts import render
import json
import os
from django.conf import settings


def view_teams(request):
    core = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'core.json')).read())
    code = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'code.json')).read())
    gadget = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'gadget.json')).read())
    garage = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'garage.json')).read())
    website = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'website.json')).read())
    context={'core': core,'code': code, 'gadget': gadget, 'garage': garage, 'website': website}
    return render(request, 'teams.html',context)
