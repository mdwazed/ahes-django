from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, reverse

from .models import Exam

def set_session_var(request, **kwargs):
	for key, value in kwargs.items():
		if key == 'exam':
			request.session['exam'] = value
		if key == 'page':
			request.session['page'] = value
		
def get_exam(request):
	try:
		exam = Exam.objects.get(pk=request.session['exam'])
	except (ObjectDoesNotExist, KeyError):
		return None

	return exam
