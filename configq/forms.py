from django import forms 
from .models import Semester, CourseName, Exam, UploadQuestion, PageConfig, Question
from django.core.exceptions import ValidationError

FRUIT_CHOICES=[
	('orange','Orange'),
	('apple', 'Apple'),
	('banana', 'Banana')
]


# def get_exam_choices():
# 	"""
# 	populate 'select widget's choices with exams. 
# 	exam objeects pk is value for select to ensure foreign key integrity
# 	"""
# 	exams = Exam.objects.all()	
# 	exam_list=[(None, '------'),]
# 	for exam in exams:
# 		key = exam.pk
# 		value = exam.course_name.__str__()+ '-' + exam.semester.__str__()
# 		exam_list.append((key, value))
# 	exam_choices = tuple(exam_list)
# 	return exam_choices

class SelectExamForm(forms.Form):
	# exam = forms.CharField(widget=forms.Select(choices=get_exam_choices()))
	exam = forms.ModelChoiceField(queryset=Exam.objects.all())

class ExamConfigForm(forms.ModelForm):
	class Meta:
		model = Exam
		fields= '__all__'

class PageConfigForm(forms.ModelForm):
	class Meta:
		model = PageConfig
		exclude = ['upload_question']


class QuestionImageUploadForm(forms.ModelForm):
	class Meta:
		model = UploadQuestion
		fields = ['page', 'description', 'image']
	


class PreQuestionConfigForm(forms.Form):
	# exam = forms.CharField(widget=forms.Select(choices=get_exam_choices()))
	page = forms.IntegerField()
	
class QuestionConfigForm(forms.Form):
	question_number = forms.CharField(max_length=5,)
	top_left_x = forms.IntegerField()
	top_left_y = forms.IntegerField()
	bottom_right_x = forms.IntegerField()
	bottom_right_y = forms.IntegerField()	
	# coord = forms.CharField(max_length=10)
	question_text = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'rows': 2}),)
	question_answer = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'rows': 2}),)

class EditQuestionForm(forms.ModelForm):
	questionText = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'rows': 2}),)
	questionAns = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'rows': 2}),)
	class Meta:
		model = Question
		exclude = ['exam']
	

class NameForm(forms.Form):
	your_name = forms.CharField(max_length=100)
	your_age = forms.IntegerField()
	favorite_friuts = forms.CharField(max_length=20, widget=forms.Select(choices=FRUIT_CHOICES))

class UploadForm(forms.Form):
	file = forms.FileField()