from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect

from .models import Exam, Question
from .forms import NameForm, ExamConfigForm, QuestionConfigForm, UploadForm

# Create your views here.
def home(request):
	"""
	home page of the configq app. contain links for other configurations
	"""
	context = {}
	return render(request, 'configq/config_home.html', context)

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
			return HttpResponseRedirect(reverse('configq:home'))
		else:
			return render(request, 'configq/exam_config_form.html', {'form': form})
	else:
		form = ExamConfigForm()
		return render(request, 'configq/exam_config_form.html', {'form': form})

def question_config(request):
	"""
	instantiate question objects. set various parameter like loaction of question on the image,
	question text, question ans etc..
	"""
	if request.method == 'POST':
		form = QuestionConfigForm(request.POST)
		if form.is_valid():
			# print(form.cleaned_data)
			topLeftX = form.cleaned_data.get("top_left_x")
			topLeftY = form.cleaned_data.get("top_left_y")
			bottomRightX = form.cleaned_data.get("bottom_right_y")
			bottomRightY = form.cleaned_data.get("bottom_right_y")
			exam =Exam.objects.get(pk=form.cleaned_data.get("exam"))
			page = form.cleaned_data.get("page")
			questionText = form.cleaned_data.get("question_text")
			questionAns = form.cleaned_data.get("question_answer")
			questionObj = Question(
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

			return HttpResponseRedirect(reverse('configq:home'))
		else:
			return render(request, 'configq/question_config_form.html', {'form':form})
	else:
		form = QuestionConfigForm()
		return render(request, 'configq/question_config_form.html', {'form':form})


def question_list(request):
	"""
	shows all questions
	"""
	questions = Question.objects.all()
	return render(request, 'configq/question_list.html', {'questions':questions})


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
		file_name = request.FILES["file"].name
		return HttpResponse(file_name)
	else:
		return render(request, 'configq/upload.html', {'form': form})




