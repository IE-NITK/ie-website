from django.shortcuts import render
import json
import os
from django.conf import settings



def view_teams(request):
    data = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'iemembers.json')).read())
    context={'data':data}
    return render(request, 'teams.html',context)
