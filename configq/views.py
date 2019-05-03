from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist

from . import misc_function
from .models import Exam, Question, UploadQuestion, PageConfig
from .forms import (
	ExamConfigForm, QuestionConfigForm, QuestionImageUploadForm, 
	UploadForm, PreQuestionConfigForm, SelectExamForm, PageConfigForm, EditQuestionForm,
	 ExamModelForm)

# Create your views here.
def home(request):
	"""
	home page of the configq app. contain links for other configurations
	"""
	exam = misc_function.get_exam(request)
	context = {
	'exam': exam,
	}
	return render(request, 'configq/config_home.html', context)

def select_exam(request):
	"""
	provide option to select the exams which was created by this user.(need to add this functionality) 
	selected exam is added to the session var.
	all further task will be based on this selection.
	"""
	print('selection submitted')
	if request.method == 'POST':
		form = SelectExamForm(request.POST)
		if form.is_valid():
			# check whether selected exam was created by  this user or not.
			#
			# if selected exam was created by this user then:
			
			misc_function.set_session_var(request, exam=form.cleaned_data['exam'].id)
			# print(type(form.cleaned_data['exam'].id))

	return HttpResponseRedirect(reverse('configq:question_image_upload'))

def exam_config(request):
	"""
	instantiate an exam object based on user slection of course name and semester
	store in db. used during intantiating the question object. course name and semester together has to be unique
	"""
	if request.method=='POST':
		form = ExamConfigForm(request.POST)
		if form.is_valid():
			# print(type(form))
			new_instance = form.save()
			misc_function.set_session_var(request, exam=new_instance.id)
			return HttpResponseRedirect(reverse('configq:question_image_upload'))
		else:
			return render(request, 'configq/exam_config_form.html', {'form': form})
	else:
		exam = misc_function.get_exam(request)
		form = ExamConfigForm()
		form2 = SelectExamForm()
		context = {
		'exam' : exam,
		'form': form,
		'form2': form2,
		# 'exam': Exam.objects.get(pk=request.session['exam']),
		}
		return render(request, 'configq/exam_config_form.html', context)

def exam_update(request):
	"""
	edit exam parameters including grading threshold
	"""
	exam = misc_function.get_exam(request)
	if request.method == 'POST':
		form = ExamModelForm(request.POST, instance=exam)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('configq:exam_config'))
	form = ExamModelForm(instance=exam)
	context = {
	'form': form,
	'exam': exam,
	}
	return render(request, 'configq/exam_update.html', context)

def pre_question_config(request):
	"""
	display form to select exam and page number. 
	based on provided information question config form and appropriate image will be open 
	to configure a question and answer box's position.
	"""

	if request.method == 'POST':
		form = PreQuestionConfigForm(request.POST)
		if form.is_valid():
			misc_function.set_session_var(request, page=form.cleaned_data.get('page'))
			# request.session['page_number'] = form.cleaned_data.get("page")
			# request.session['exam'] = form.cleaned_data.get("exam")
		
			return HttpResponseRedirect(reverse('configq:question_config'))
		return render(request, 'configq/pre_question_config_form.html', {'form':form})

	else:		
		form = PreQuestionConfigForm()
		exam = misc_function.get_exam(request)
		if not exam:
			context = {
			'message': """No exam is selected or selected exam is not found for this session. 
			Please consider select a valid exam from 'exam config page'."""
			}
			return render(request, 'configq/common_error.html', context)
		context = {
		'form': form,
		'exam': exam,
		}
		return render(request, 'configq/pre_question_config_form.html', context)

def page_config(request):
	"""
	configure matriculation number digits loaction and page number box location on the page
	all request must accompany with page_number parameter set
	"""

	exam = misc_function.get_exam(request)
	if not exam:
		context = {
		'message': """No exam is selected or selected exam is not found for this session. 
		Please consider select a valid exam from 'exam config page'."""
		}
		return render(request, 'configq/common_error.html', context)

	# data has been entered and submit button has been clicked from page_config page
	# save the provided data. this form can save partial data(all fields are optional)
	if request.method == 'POST' and request.POST.get('submit') == 'Submit':
		page_number = request.POST.get('page_number')
		upload_question_instance = UploadQuestion.objects.get(exam= exam, page= page_number)
		form = PageConfigForm(request.POST or None)
		if form.is_valid():
			page_config = form.save(commit=False)
			# page_config.exam = exam 
			# page_config.page = page_number
			page_config.upload_question = upload_question_instance
			page_config.save()
			if request.POST.get('same_for_all'):
				print('same for all selected')
				## set the same parameter to all page of currently selected exam
				misc_function.set_all_page_config(request, page_config)  #currently populated page

			return HttpResponseRedirect(reverse('configq:question_image_upload'))
	# 'next' button has been clicked after entering page_number from page_config page
	# also this point should reach from question upload page by clicking 'config' button 
	elif request.method == 'POST' and (request.POST.get('submit') == 'Next' or request.POST.get('submit') == 'Config') :		
		page_number = request.POST.get('page_number')
		# print(page_number)
		upload_question_instance = UploadQuestion.objects.get(exam= exam, page= page_number)
		page_config_instance = PageConfig.objects.get(upload_question=upload_question_instance)
		image_url = upload_question_instance.get_image_url()
		# print(page_config_instance)
		form = PageConfigForm(instance=page_config_instance or None)
		context = {
		'form': form,
		'exam': exam,
		'image_url': str(image_url),
		'page_number': page_number,
		}
		# print(context)
		return render(request, 'configq/page_config_form.html', context)
	else:
		form = PageConfigForm()
		context = {
		'form': form,
		'exam': exam,
		}
		return render(request, 'configq/page_config_form.html', context)

def question_config(request):
	"""
	instantiate question objects. set various parameter like loaction of question on the image,
	question text, question ans etc.. display the related page image and allow
	to select precise pixel value of ans box by clicking
	"""
	# retrive selected exam id from session var. returns None in case of exam not set in the session or not found in db
	exam = misc_function.get_exam(request)
	if not exam:
		context = {
		'message': """No exam is selected or selected exam is not found. 
		Please consider select a valid exam from 'exam config page'."""
		}
		return render(request, 'configq/common_error.html', context)
	page_number = request.session['page']
	if request.method == 'POST':
		form = QuestionConfigForm(request.POST)
		if form.is_valid():
			# print(form.cleaned_data)
			question_number = form.cleaned_data.get("question_number")
			allotedMarks = form.cleaned_data.get("allotedMarks")
			threshold = form.cleaned_data.get("threshold")
			topLeftX = form.cleaned_data.get("top_left_x")
			topLeftY = form.cleaned_data.get("top_left_y")
			bottomRightX = form.cleaned_data.get("bottom_right_x")
			bottomRightY = form.cleaned_data.get("bottom_right_y")
			exam = exam
			page = page_number
			questionText = form.cleaned_data.get("question_text")
			questionAns = form.cleaned_data.get("question_answer")
			questionObj = Question(
					question_number= question_number,
					topLeftX= topLeftX,
					topLeftY= topLeftY,
					bottomRightX = bottomRightX,
					bottomRightY = bottomRightY,
					exam = exam,
					page = page,
					questionText= questionText,
					questionAns = questionAns,
					allotedMarks = allotedMarks,
					threshold = threshold,
				)
			# print(exam)
			questionObj.save()

			return HttpResponseRedirect(reverse('configq:question_list'))
		else:
			return render(request, 'configq/question_config_form.html', {'form':form})
	else:
		form = QuestionConfigForm()
		image_url = UploadQuestion.objects.get(exam= exam, page= page_number).get_image_url() # to display the image with the config form
		context ={
		'form': form,
		'exam': exam,
		'page_number': page_number,
		'image_url': str(image_url),
		}

		
		return render(request, 'configq/question_config_form.html', context)

def edit_question(request):
	
	if request.method == 'POST' and request.POST.get('submit') == 'Save': # posted after edit
	
		question_id = request.POST.get('question_id')
		exam_id = request.POST.get('exam_id')
		if question_id and exam_id:
			current_question = Question.objects.get(pk=question_id)
			form = EditQuestionForm(request.POST or None, instance= current_question)
			form.save()
			# print(form)
		
			
			return HttpResponseRedirect(reverse('configq:question_list'))
		return HttpResponse('form data is not valid')
		
	elif request.method == 'POST' and request.POST.get('submit') == 'Edit':	# pasted from question list page through edit button	
		current_question = Question.objects.get(pk=request.POST.get('question_id'))
		# question_id = current_question.id
		# exam_id = current_question.exam_id
		form = EditQuestionForm(instance = current_question)
		context = {
		'form': form.as_table,
		'current_question': current_question,
		# 'question_id': question_id,
		# 'exam_id': exam_id,
		}
		return render(request, 'configq/edit_question.html', context)

def delete_question(request):
	if request.method == 'POST':
		question_id = request.POST.get('question_id')
		Question.objects.get(pk=question_id).delete()
		return HttpResponseRedirect(reverse('configq:question_list'))



def question_list(request):
	"""
	shows all questions of currently working exam
	"""
	exam = misc_function.get_exam(request)
	if not exam:
		context = {
		'message': """No exam is selected or selected exam is not found for this session. 
		Please consider select a valid exam from 'exam config page'."""
		}
		return render(request, 'configq/common_error.html', context)
	questions = Question.objects.filter(exam= exam).order_by('question_number')
	return render(request, 'configq/question_list.html', {'questions':questions, 'exam': exam})




def question_image_upload(request):
	"""
	upload image of an exam and show the list of already uploaded images
	"""
	exam = misc_function.get_exam(request)
	if not exam:
		context = {
		'message': """No exam is selected or selected exam is not found for this session. 
		Please consider select a valid exam from 'exam config page'."""
		}
		return render(request, 'configq/common_error.html', context)

	if request.method == "POST":
		form = QuestionImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			f = form.save(commit=False) # get form data 
			f.exam = Exam.objects.get(pk=request.session['exam']) # add corresponding exam object to f 
		
			f.save()
			
			form = QuestionImageUploadForm()
			uploaded_images = UploadQuestion.objects.filter(exam=request.session['exam']) # populate list of uploaded images of this exam 
			message = "Image uploaded successfully add another.."
			context = {
				'form': form,
				'message': message,
				'uploaded_images': uploaded_images,
				'exam': exam
			}
			return render(request, 'configq/question_image_upload.html', context)
		else:
			pass
			####### return something if form is not valid  #######
	else: # if landed through get method show the blank form and related image
		uploaded_images = UploadQuestion.objects.filter(exam=request.session['exam']).order_by('page')
		form = QuestionImageUploadForm()
		context = {
			'form': form,
			'uploaded_images': uploaded_images,	
			'exam': exam
		}
		return render(request, 'configq/question_image_upload.html', context)

def show_question_image(request):
	if request.method == 'POST':
		image_id = request.POST.get('uploaded_image_id')
		upload_instance = UploadQuestion.objects.get(pk= image_id)
		image_url = upload_instance.get_image_url()
		context = {
		'upload_instance': upload_instance,
		'image_url': image_url,
		}

		return render(request, 'configq/show_question_image.html', context)
def delete_question_image(request):
	if request.method == 'POST':
		image_id = request.POST.get('uploaded_image_id')
		upload_instance = UploadQuestion.objects.get(pk= image_id)
		image_url = upload_instance.get_image_url()
		upload_instance.delete()
		# image_url = request
		return HttpResponseRedirect(reverse('configq:question_image_upload'))
