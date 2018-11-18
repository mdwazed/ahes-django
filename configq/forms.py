from django import forms 
from .models import Semester, CourseName, Exam
from django.core.exceptions import ValidationError

FRUIT_CHOICES=[
	('orange','Orange'),
	('apple', 'Apple'),
	('banana', 'Banana')
]


def get_exam_choices():
	"""
	prepare 'select choices' of exam object's course and semester for question objects.
	exam objeects pk is value for select to ensure foreign key integrity
	"""
	exams = Exam.objects.all()	
	exam_list=[]
	for exam in exams:
		key = exam.pk
		value = exam.course_name.__str__()+ '-' + exam.semester.__str__()
		exam_list.append((key, value))
	exam_choices = tuple(exam_list)
	return exam_choices


class ExamConfigForm(forms.ModelForm):
	class Meta:
		model = Exam
		fields= ['course_name', 'semester', 'professor', 'credit_point']


class QuestionConfigForm(forms.Form):
	exam = forms.IntegerField(widget=forms.Select(choices=get_exam_choices()))
	top_left_x = forms.IntegerField()
	top_left_y = forms.IntegerField()
	bottom_right_x = forms.IntegerField()
	bottom_right_y = forms.IntegerField()	
	page = forms.IntegerField()
	question_num = forms.CharField(max_length=5,)
	question_text = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 5}),)
	question_answer = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 5}),)

	# def clean_exam(self):
	# 	data = self.cleaned_data['exam']
	# 	if not data == 
	# 	raise ValidationError('incorrect value in exam field')
	# 	return data
	

class NameForm(forms.Form):
	your_name = forms.CharField(max_length=100)
	your_age = forms.IntegerField()
	favorite_friuts = forms.CharField(max_length=20, widget=forms.Select(choices=FRUIT_CHOICES))

class UploadForm(forms.Form):
	file = forms.FileField()