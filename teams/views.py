from django.shortcuts import render
import json
import os
from django.conf import settings


def view_teams(request):
    core = json.loads(
        open(os.path.join(settings.STATICFILES_DIRS[0], 'core2021.json')).read())
    code = json.loads(
        open(os.path.join(settings.STATICFILES_DIRS[0], 'code.json')).read())
    gadget = json.loads(
        open(os.path.join(settings.STATICFILES_DIRS[0], 'gadget.json')).read())
    garage = json.loads(
        open(os.path.join(settings.STATICFILES_DIRS[0], 'garage.json')).read())
    website = json.loads(
        open(os.path.join(settings.STATICFILES_DIRS[0], 'website.json')).read())
    robotics = json.loads(
        open(os.path.join(settings.STATICFILES_DIRS[0], 'robotics.json')).read())
    script = json.loads(
        open(os.path.join(settings.STATICFILES_DIRS[0], 'script.json')).read())
    media = json.loads(
        open(os.path.join(settings.STATICFILES_DIRS[0], 'media.json')).read())
    capital = json.loads(
        open(os.path.join(settings.STATICFILES_DIRS[0], 'capital.json')).read())
    tectonic = json.loads(
        open(os.path.join(settings.STATICFILES_DIRS[0], 'tectonic.json')).read())

    context = {'core': core, 'code': code, 'gadget': gadget, 'garage': garage, 'website': website, 'robotics': robotics, 'script': script, 'media': media, 'capital': capital, 'tectonic': tectonic, }
    return render(request, 'teams.html', context)
