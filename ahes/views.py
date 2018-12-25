from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect



# Create your views here.

def home(request):
	context ={}
	return render(request, 'ahes_home.html', context)