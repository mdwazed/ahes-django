#### grader.views  ###

from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, FormView
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError

from .models import StudentAns
from .forms import UploadAnsScriptForm

from grader.src.preProcessAnsScript import ansScript
from grader.src import ans_grader
from configq.misc_function import get_exam
from configq.models import Question

import random

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
	upload all scanned image to raw_image dir.
	exam_id is prefixed to each image before saving.
	images from this dir will be removed once it is read or failed to read during read action.
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
	read students ans from each uplaoded image in raw_image dir and save in db
	after reading reading remove the original image from raw_image dir
	and save them to cleaned_image or unread_image dir.
	"""
	if request.method == 'POST':
		ansc = ansScript()
		(readFileCount, unReadFileCount) = ansc.processAnsScript(request)
		try:
			ansc.readAns(request)
		except IntegrityError as e:
			error = "Duplicate entry for compound key exam - matriculation nr. Plese try to remove already existing entry for this exam" + str(e)
			context = {
			'error': error
			}
			return render(request, 'grader/custom_error.html', context)
		
		
		context ={
			'success_message': 'image pre processing complete',
			'readFileCount': readFileCount,
			'unReadFileCount' : unReadFileCount,
		}
	else:
		context={

		}
	
	return render(request, 'grader/read_ans_script.html', context)

def evaluate_ans_scripts(request):
	"""
	evaluate all students ans on database against official ans,
	auto grade the ans based on threshold and alloted marks  
	"""
	if request.method == 'POST':
		ans_grader.grade_all_ans(request)
		return HttpResponseRedirect(reverse('grader:ans_list'))

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
			return StudentAns.objects.filter(exam= get_exam(self.request)).order_by(order, 'matching_confidence')
		return StudentAns.objects.filter(exam= get_exam(self.request)).order_by('question_num')

	def post(self, request, *args, **kwargs):
		ques_nr = request.POST['ques_nr']
		mat_nr = request.POST['mat_nr']
		if ques_nr and mat_nr:
			object_list = StudentAns.objects.filter(exam= get_exam(self.request), matriculation_num=mat_nr, question_num=ques_nr)
			context = {
			'object_list':object_list
			}
			return render(request, 'grader/studentans_list.html', context)
		elif ques_nr:
			object_list = StudentAns.objects.filter(exam= get_exam(self.request), question_num=ques_nr)
			context = {
			'object_list':object_list
			}
			return render(request, 'grader/studentans_list.html', context)
		elif mat_nr:
			object_list = StudentAns.objects.filter(exam= get_exam(self.request), matriculation_num=mat_nr)
			context = {
			'object_list':object_list
			}
			return render(request, 'grader/studentans_list.html', context)
		else:
			object_list = StudentAns.objects.filter(exam= get_exam(self.request))
			context = {
			'object_list':object_list
			}
			return render(request, 'grader/studentans_list.html', context)


def ans_details(request, pk=None):
	"""
	renders details of an ans with original written subimage
	"""
	exam = get_exam(request)
	# posted from the ans_details page by clicking the next button
	# check which radio button was selected and set the pk according to that 
	if request.method == 'POST':
		all_ans = StudentAns.objects.filter(exam=exam)
		option = request.POST['next_choice']
		if (option == 'random'):
			pass
		elif(option == 'student'):
			pass
		else:
			id = request.POST['pk']
			current_ans = all_ans.get(pk=id)
			# get a random pk of another ans with same question id 
			same_anss = all_ans.filter(exam=exam, question_num=current_ans.question_num)
			# print(same_anss)
			random_ans = random.choice(same_anss)
			pk = random_ans.pk
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

def change_threshold(request):
	print("ajax request received")
	question_id = request.POST['question_id']
	new_th = request.POST['new_th']
	print(question_id)
	print(new_th)
	# return JsonResponse(question_id, safe=False)
	
	try:
		question = get_object_or_404(Question, pk=question_id)
		question.threshold = new_th
		question.save()
		
		# return JsonResponse(question_id, safe=False)
	except:
		return JsonResponse("problem occured while changing the threshold", safe=False)
	try:
		ans_grader.grade_all_ans(request, question) 
	except:
		return JsonResponse("failed to re evaluate ans", safe=False)
	return JsonResponse("Threshold changed successfuly with re evaluation of ans", safe=False)



def final_result(request):
	
	context = {

	}
	
	return render(request, 'grader/final_result.html', context)

