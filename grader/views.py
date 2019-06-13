#### grader.views  ###

from django.shortcuts import render, reverse, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, FormView
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError

from .models import StudentAns
from .forms import UploadAnsScriptForm, ExamGradeUpdateForm

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
		ans_grader.auto_grade_all_ans(request)
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
			return StudentAns.objects.filter(exam= get_exam(self.request)).order_by(order, 'matching_confidence')[:50]
		return StudentAns.objects.filter(exam= get_exam(self.request)).order_by('question_num')[:50]

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
			# iter randomly
			same_anss = all_ans
			random_ans = random.choice(same_anss)
			pk = random_ans.pk
		elif(option == 'student'):
			# iter all ans of this student
			id = request.POST['pk']
			current_ans = all_ans.get(pk=id)
			# get the next ans of this student
			same_anss = all_ans.filter(exam=exam, matriculation_num=current_ans.matriculation_num)
			random_ans = random.choice(same_anss)
			pk = random_ans.pk
		else:
			# same question iter for random student
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
	# uncomment the appropriate line to choose the correct img ext.
	# image_name = str(exam.id) +'_'+ str(student_ans.matriculation_num) +'_'+ str(page_num) + '.png'
	image_name = str(exam.id) +'_'+ str(student_ans.matriculation_num) +'_'+ str(page_num) + '.jpg'
	top_x = question.topLeftX
	top_y = question.topLeftY
	bottom_x = question.bottomRightX
	bottom_y = question.bottomRightY
	# get the related image crop the specific part and pass to template as base64 encoded data 
	img_path = os.path.join(settings.MEDIA_ROOT, 'cleaned_image', image_name)
	try:
		img = cv.imread(img_path)
		sub_img = img[top_y:bottom_y, top_x:bottom_x]
	except Exception as e:
		return HttpResponse("could not read the subimage. check img ext on line 184/185." + str(e))
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
	"""
	change threshold of a question during examiners reevaluation.
	also re-evaluate the result based on new threshold.
	"""
	# print("ajax request received")
	question_id = request.POST['question_id']
	new_th = request.POST['new_th']
	# print(question_id)
	# print(new_th)
	try:
		question = get_object_or_404(Question, pk=question_id)
		question.threshold = new_th
		question.save()
	except:
		return JsonResponse("problem occured while changing the threshold", safe=False)
	try:
		ans_grader.auto_grade_all_ans(request, question) 
	except:
		return JsonResponse("failed to re evaluate ans", safe=False)
	return_dict = {
	'new_th':question.threshold,
	'error': "Failed to update the threshold"
	}
	return JsonResponse(return_dict)

def change_final_grade(request):
	"""
	change final grade of a student_ans 
	this will not be ovrwritten by auto grade
	"""
	# print(request.POST)
	student_ans = get_object_or_404(StudentAns, pk=request.POST['student_ans_id'])
	print(student_ans)
	student_ans.final_grade = request.POST['new_fg']
	student_ans.manually_graded = True
	student_ans.save()
	return_dict = {
	'fg':student_ans.final_grade
	}
	return JsonResponse(return_dict)

def finalize_result(request):
	exam = get_exam(request)
	student_anss = StudentAns.objects.filter(exam=exam)
	for ans in student_anss:
		if not ans.manually_graded:
			ans.final_grade = ans.auto_grade
			ans.save()
	return HttpResponseRedirect(reverse('grader:ans_list'))


def final_result(request):
	exam = get_exam(request)
	appeared = StudentAns.objects.filter(exam=exam).values('matriculation_num').distinct()
	appeared_list = [x['matriculation_num'] for x in appeared]
	total_appeared = len(appeared_list)
	grades = [0,0,0,0,0,0,0,0,0,0,0,0,]
	results = []
	for mat_num in appeared_list:
		achieved_marks = 0
		ans_list = StudentAns.objects.filter(exam=exam, matriculation_num=mat_num)
		for ans in ans_list:
			achieved_marks += ans.final_grade
		total_marks = exam.total_marks
		achieved_percentage = (achieved_marks/total_marks)*100

		if(achieved_percentage < exam.grade_5_0):
			grade = 5.00
			grades[11] += 1
		elif(achieved_percentage >= exam.grade_4_0 and achieved_percentage < exam.grade_3_7):
			grade= 4.00
			grades[10] += 1
		elif(achieved_percentage >= exam.grade_3_7 and achieved_percentage < exam.grade_3_3):
			grade= 3.70
			grades[9] += 1
		elif(achieved_percentage >= exam.grade_3_3 and achieved_percentage < exam.grade_3_0):
			grade= 3.30
			grades[8] += 1
		elif(achieved_percentage >= exam.grade_3_0 and achieved_percentage < exam.grade_2_7):
			grade= 3.00
			grades[7] += 1
		elif(achieved_percentage >= exam.grade_2_7 and achieved_percentage < exam.grade_2_3):
			grade= 2.70
			grades[6] += 1
		elif(achieved_percentage >= exam.grade_2_3 and achieved_percentage < exam.grade_2_0):
			grade= 2.30
			grades[5] += 1
		elif(achieved_percentage >= exam.grade_2_0 and achieved_percentage < exam.grade_1_7):
			grade= 2.00
			grades[4] += 1
		elif(achieved_percentage >= exam.grade_1_7 and achieved_percentage < exam.grade_1_3):
			grade= 1.70
			grades[3] += 1
		elif(achieved_percentage >= exam.grade_1_3 and achieved_percentage < exam.grade_1_0):
			grade= 1.30
			grades[2] += 1
		elif(achieved_percentage >= exam.grade_1_0 and achieved_percentage < exam.grade_0_7):
			grade= 1.00
			grades[1] += 1
		elif(achieved_percentage >= exam.grade_0_7):
			grade= 0.70
			grades[0] += 1
		results.append((mat_num, achieved_marks, achieved_percentage, grade))

	count_p_f = [0,0]
	for result in results:
		if result[2]< 5.0:
			count_p_f[0] += 1
		else:
			count_p_f[1] += 1
	context = {
	'total_appeared': total_appeared,
	'total_marks': total_marks,
	'results': results,
	'grades': grades,
	'count_p_f': count_p_f,
	}
	
	return render(request, 'grader/final_result.html', context)

# def highchart(request):
# 	return render (request, 'grader/highchart_test.html',)	

def update_exam_grade_thresh(request):
	exam = get_exam(request)
	if request.method == 'POST':
		# return HttpResponse("posted")
		form = ExamGradeUpdateForm(request.POST, instance=exam)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('grader:final_result'))
	form = ExamGradeUpdateForm(instance=exam)
	context = {
	'form': form,
	}

	return render(request, 'grader/exam_grade_update_thresh.html', context)

def publish_result(request):
	context = {
	'error': "Export the result to somewhere"
	}
	return render(request, 'grader/custom_error.html', context)