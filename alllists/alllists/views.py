from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello world") 	

def console(request):
	return render(request, 'console.html')