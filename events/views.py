from django.shortcuts import render


def view_events(request):
    return render(request, 'events.html')


def smp(request):
    return render(request, 'smp.html')


def hackverse(request):
    return render(request, 'hackverse.html')

def enigma19(request):
    return render(request, 'enigma19.html')
