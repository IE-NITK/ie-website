from django.shortcuts import render

def error_404_view(request, exception):
	return render(request, '404.html', locals())

def view_team(request):
	return render(request, 'events.html')