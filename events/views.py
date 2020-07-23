from django.shortcuts import render


def view_events(request):
    return render(request, 'events.html')


def smp2019(request):
    return render(request, 'smp2019.html')

def smp2020(request):
    return render(request, 'smp2020.html')

def hackverse(request):
    return render(request, 'hackverse.html')

def virtual_expo(request):
    return render(request, 'virtual_expo.html')
