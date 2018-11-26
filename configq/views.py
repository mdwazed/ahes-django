from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView

from . import misc_function
from .models import Exam, Question, UploadQuestion
from .forms import NameForm, ExamConfigForm, QuestionConfigForm, QuestionImageUploadForm, UploadForm, PreQuestionConfigForm, SelectExamForm, PageConfigForm, EditQuestionForm

# Create your views here.
def home(request):
	"""
	home page of the configq app. contain links for other configurations
	"""
	context = {}
	return render(request, 'configq/config_home.html', context)

def select_exam(request):
	"""
	provide option to select the exams which was created by this user.(need to add this functionality) 
	selected exam is added to the swssion var.
	all further task will be based on this selection.
	"""
	form = SelectExamForm(request.POST)
	if form.is_valid():
		# check whether selected exam was created by  this user or not.
		#
		# if selected exam was created by this user then:
		misc_function.set_session_var(request, exam=form.cleaned_data.get('exam'))
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
			form.save()
			return HttpResponseRedirect(reverse('configq:question_config'))
		else:
			return render(request, 'configq/exam_config_form.html', {'form': form})
	else:
		form = ExamConfigForm()
		form2 = SelectExamForm()
		context = {
		'form': form,
		'form2': form2,
		# 'exam': Exam.objects.get(pk=request.session['exam']),
		}
		return render(request, 'configq/exam_config_form.html', context)



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
		exam = Exam.objects.get(pk=request.session['exam'])
		context = {
		'form': form,
		'exam': exam,
		}
		return render(request, 'configq/pre_question_config_form.html', context)

def page_config(request):
	"""
	configure matriculation number digits loaction and page number box location
	"""
	exam = Exam.objects.get(pk=request.session['exam'])	
	if request.method == 'POST':
		pass
	else:
		image_url = UploadQuestion.objects.get(exam= exam, page= 1).get_image_url()
		form = PageConfigForm()
		context = {
		'form': form,
		'exam': exam,
		'image_url': str(image_url),
		}
		# print(form)
		return render(request, 'configq/page_config_form.html', context)

def question_config(request):
	"""
	instantiate question objects. set various parameter like loaction of question on the image,
	question text, question ans etc..
	"""
	
	exam = Exam.objects.get(pk=request.session['exam'])
	page_number = request.session['page']


	if request.method == 'POST':
		form = QuestionConfigForm(request.POST)
		if form.is_valid():
			# print(form.cleaned_data)
			question_number = form.cleaned_data.get("question_number")
			topLeftX = form.cleaned_data.get("top_left_x")
			topLeftY = form.cleaned_data.get("top_left_y")
			bottomRightX = form.cleaned_data.get("bottom_right_y")
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
					questionAns = questionAns
				)
			# print(exam)
			questionObj.save()

			return HttpResponseRedirect(reverse('configq:pre_question_config'))
		else:
			return render(request, 'configq/question_config_form.html', {'form':form})
	else:
		form = QuestionConfigForm()
		image_url = UploadQuestion.objects.get(exam= exam, page= page_number).get_image_url()
		context ={
		'form': form,
		'exam': exam,
		'page_number': page_number,
		'image_url': str(image_url),
		}

		
		return render(request, 'configq/question_config_form.html', context)

def edit_question(request):
	
	if request.method == 'POST' and request.POST.get('submit') == 'Save':
	
		question_id = request.POST.get('question_id')
		exam_id = request.POST.get('exam_id')
		if question_id and exam_id:
			current_question = Question.objects.get(pk=question_id)
			form = EditQuestionForm(request.POST or None, instance= current_question)
			form.save()
			# print(form)
		
			
			return HttpResponseRedirect(reverse('configq:question_list'))
		return HttpResponse('form data is not valid')
		
	elif request.method == 'POST' and request.POST.get('submit') == 'Edit':		
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
	questions = Question.objects.filter(exam= request.session['exam']).order_by('question_number')
	return render(request, 'configq/question_list.html', {'questions':questions})




def question_image_upload(request):
	"""
	upload image of an exam and show the list of already uploaded images
	"""
	exam = Exam.objects.get(pk=request.session['exam'])

	if request.method == "POST":
		form = QuestionImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			f = form.save(commit=False) # get form data 
			f.exam = Exam.objects.get(pk=request.session['exam']) # add corresponding exam object to f 
		
			f.save()
			
			form = QuestionImageUploadForm()
			uploaded_iamges = UploadQuestion.objects.filter(exam=request.session['exam']) # populate list of uploaded images of this exam 
			message = "Image uploaded successfully add another.."
			context = {
				'form': form,
				'message': message,
				'uploaded_iamges': uploaded_iamges,
				'exam': exam
			}
			return render(request, 'configq/question_image_upload.html', context)

	else:
		uploaded_iamges = UploadQuestion.objects.filter(exam=request.session['exam']).order_by('page')
		form = QuestionImageUploadForm()
		context = {
			'form': form,
			'uploaded_iamges': uploaded_iamges,	
			'exam': exam
		}
		return render(request, 'configq/question_image_upload.html', context)

def delete_question_image(request):
	if request.method == 'POST':
		print(request)
		# image_url = request
		return HttpResponse('delete submitted')

############################################################################
def get_name(request):
	"""
	test view for forms andd other testing and experimenting
	"""
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data['your_name'])
			print(form.cleaned_data['favorite_friuts'])
			return HttpResponseRedirect(reverse('home'))			
	else:
		form = NameForm()
	return render(request, 'configq/name.html', {'form':form})

def upload_file(request):
	"""
	test upload functionality
	"""
	form = UploadForm()
	if request.method =="POST":
		file = request.FILES["file"]
		return HttpResponse(file)
	else:
		return render(request, 'configq/upload.html', {'form': form})




