from django.shortcuts import render

def view_sig(request):
	return render(request, 'sig.html')
