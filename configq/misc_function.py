from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, reverse

from .models import Exam, PageConfig


def set_session_var(request, **kwargs):
	"""
	# set exam or page number in session 
	"""
	for key, value in kwargs.items():
		if key == 'exam':
			request.session['exam'] = value
		if key == 'page':
			request.session['page'] = value



def get_exam(request):
	"""
	# return currently set exam in session
	"""
	try:
		exam = Exam.objects.get(pk=request.session['exam'])
	except (ObjectDoesNotExist, KeyError):
		return None

	return exam

def set_all_page_config(request, current_page):
	"""
	set same parameter to all page of currently selected exam.
	current parameters are taken from current under config page
	"""
	exam_instance = get_exam(request)
	# get all page config instance of current exam
	page_config_query_set = PageConfig.objects.filter(upload_question__exam=exam_instance)
	for page in page_config_query_set:
		p = PageConfig()
		p = current_page
		p.upload_question = page.upload_question
		p.save()	


