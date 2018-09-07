from django.shortcuts import render

def view_events(request):
	return render(request, 'events.html')
