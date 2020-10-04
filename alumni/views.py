from django.shortcuts import render
import json
import os
from django.conf import settings


def view_alumni(request):
    alumni2020 = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'alumni2020.json')).read())
    alumni2019 = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'alumni2019.json')).read())
    alumni2018 = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'alumni2018.json')).read())
    alumni2017 = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'alumni2017.json')).read())
    alumni2016 = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'alumni2016.json')).read())
    alumni2015 = json.loads(open(os.path.join(settings.STATICFILES_DIRS[0], 'alumni2015.json')).read())

    context={'alumni2020': alumni2020,'alumni2019': alumni2019,'alumni2018': alumni2018, 'alumni2017': alumni2017, 'alumni2016': alumni2016, 'alumni2015': alumni2015}
    return render(request, 'alumni.html',context)
