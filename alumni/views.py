from django.shortcuts import render
import json
import os
from django.conf import settings
import datetime


def view_alumni(request,year=datetime.datetime.now().year):
    alumni = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'alumni'+str(year).strip()+'.json')).read())
    context={'alumni': alumni,'year':year}
    return render(request, 'alumni.html',context)
