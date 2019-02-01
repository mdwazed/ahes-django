#### grader.views  ###

from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, FormView
from django.core.files.storage import FileSystemStorage

from .models import StudentAns
from .forms import UploadAnsScriptForm

from grader.src.preProcessAnsScript import ansScript
from grader.src import ans_grader
from configq.misc_function import get_exam
from configq.models import Question

import cv2 as cv
import base64
import numpy as np
import os
from django.conf import settings
from PIL import Image


def home(request):
	context={}    
	return render(request, 'grader/grader_home.html', context)

def upload(request):
	"""
	upload all scanned image to resized folder from where all further processing will be done.
	"""
	upload_file_count = 0
	if request.method == "POST":
		myfiles = request.FILES.getlist('myfile')
		# print(myfiles)
		exam = get_exam(request)
		for file in myfiles:
			fs = FileSystemStorage()
			fs.save('raw_image/'+ str(exam.id) +'_'+file.name, file)
			upload_file_count +=1
		context = {
		'upload_file_count' : upload_file_count
		}
		return render(request, 'grader/upload_ans_script.html', context)
	else:
		context = {

		}
		return render(request, 'grader/upload_ans_script.html', context)


def read_ans_script(request):
	"""
	read students ans from each uplaoded image and seve in db
	"""
	if request.method == 'POST':
		ansc = ansScript()
		(readFileCount, unReadFileCount) = ansc.processAnsScript(request)
		ansc.readAns(request)
		ans_grader.grade_all_ans(request)
		
		context ={
			'success_message': 'image pre processing complete',
			'readFileCount': readFileCount,
			'unReadFileCount' : unReadFileCount,
		}
	else:
		context={

		}
	
	return render(request, 'grader/read_ans_script.html', context)

def delete_ans(request):
	"""
	delete all ans fro the currently selected exam
	"""
	if request.method == 'POST':
		StudentAns.objects.filter(exam= get_exam(request)).delete()
		return HttpResponseRedirect(reverse('grader:ans_list'))

class StudentsAnsList(ListView):
	model = StudentAns

	def get_queryset(self):
		order = self.kwargs.get('order', None)
		if order:
			return StudentAns.objects.filter(exam= get_exam(self.request)).order_by(order)
		return StudentAns.objects.filter(exam= get_exam(self.request))


def ans_details(request, pk=None):
	"""
	renders details of an ans with original written subimage
	"""
	exam = get_exam(request)
	if pk:
		student_ans = StudentAns.objects.get(pk=pk)
	else:
		# get a random mat num from this exam 
		return HttpResponse('did you forget to implement this page without pk url prt')

	question = get_object_or_404(Question, exam=exam, question_number=student_ans.question_num)
	page_num = question.page
	image_name = str(exam.id) +'_'+ str(student_ans.matriculation_num) +'_'+ str(page_num) + '.png'
	top_x = question.topLeftX
	top_y = question.topLeftY
	bottom_x = question.bottomRightX
	bottom_y = question.bottomRightY
	# get the related image crop the specific part and pass to ttemplate as base64 encoded data 
	img_path = os.path.join(settings.MEDIA_ROOT, 'cleaned_image' ,image_name)
	img = cv.imread(img_path)
	sub_img = img[top_y:bottom_y, top_x:bottom_x]
	ret, frame_buff = cv.imencode('.png', sub_img)
	frame_b64 = base64.b64encode(frame_buff)
	frame_b64 = frame_b64.decode('utf8')
	# print(frame_b64)
	context = {
		'exam':exam,
		'pk':pk,
		'student_ans': student_ans,
		'img': frame_b64,
		'question': question,
	}
	return render(request, 'grader/ans_details.html', context)


