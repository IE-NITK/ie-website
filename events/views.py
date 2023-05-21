from django.shortcuts import render


def view_events(request):
    return render(request, 'events.html')


def smp2019(request):
    return render(request, 'smp2019.html')

def smp2020(request):
    return render(request, 'smp2020.html')

def smp2021(request):
    return render(request, 'smp2021.html')

def smp2022(request):
    return render(request, 'smp2022.html')

def smp2023(request):
    return render(request, 'smp2023.html')

def hackverse(request):
    return render(request, 'hackverse.html')