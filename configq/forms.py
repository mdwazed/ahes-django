from django import forms 
from .models import Semester, CourseName, Exam, UploadQuestion, PageConfig, Question
from django.core.exceptions import ValidationError

# FRUIT_CHOICES=[
# 	('orange','Orange'),
# 	('apple', 'Apple'),
# 	('banana', 'Banana')
# ]


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

class ExamModelForm(forms.ModelForm):
	"""
	Exam Model form to create a new exam and 
	update an existing exam
	"""
	grade_5_0 = forms.CharField(label='Grade 5.0 <')
	grade_4_0 = forms.CharField(label='Grade 4.0 >=')
	grade_3_7 = forms.CharField(label='Grade 3.7 >=')
	grade_3_3 = forms.CharField(label='Grade 3.3 >=')
	grade_3_0 = forms.CharField(label='Grade 3.0 >=')
	grade_2_7 = forms.CharField(label='Grade 2.7 >=')
	grade_2_3 = forms.CharField(label='Grade 2.3 >=')
	grade_2_0 = forms.CharField(label='Grade 2.0 >=')
	grade_1_7 = forms.CharField(label='Grade 1.7 >=')
	grade_1_3 = forms.CharField(label='Grade 1.3 >=')
	grade_1_0 = forms.CharField(label='Grade 1.0 >=')
	grade_0_7 = forms.CharField(label='Grade 0.7 >=')
	class Meta:
		model = Exam
		exclude = ['course_name', 'semester', 'credit_point', 'exam_code']
		

class ExamConfigForm(forms.ModelForm):
	grade_5_0 = forms.CharField(label='Grade 5.0 <', initial=50.00)
	grade_4_0 = forms.CharField(label='Grade 4.0 >=', initial=50.00)
	grade_3_7 = forms.CharField(label='Grade 3.7 >=', initial=55.00)
	grade_3_3 = forms.CharField(label='Grade 3.3 >=', initial=60.00)
	grade_3_0 = forms.CharField(label='Grade 3.0 >=', initial=65.00)
	grade_2_7 = forms.CharField(label='Grade 2.7 >=', initial=70.00)
	grade_2_3 = forms.CharField(label='Grade 2.3 >=', initial=75.00)
	grade_2_0 = forms.CharField(label='Grade 2.0 >=', initial=80.00)
	grade_1_7 = forms.CharField(label='Grade 1.7 >=', initial=85.00)
	grade_1_3 = forms.CharField(label='Grade 1.3 >=', initial=90.00)
	grade_1_0 = forms.CharField(label='Grade 1.0 >=', initial=95.00)
	grade_0_7 = forms.CharField(label='Grade 0.7 >=', initial=99.00)
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
	allotedMarks = forms.DecimalField()
	threshold = forms.DecimalField()
	top_left_x = forms.IntegerField()
	top_left_y = forms.IntegerField()
	bottom_right_x = forms.IntegerField()
	bottom_right_y = forms.IntegerField()	
	# coord = forms.CharField(max_length=10)
	question_text = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 4, 'cols': 70}),)
	question_answer = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 4, 'cols': 70}),)

class EditQuestionForm(forms.ModelForm):
	questionText = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 4, 'cols': 70}),)
	questionAns = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 4, 'cols': 70}),)
	class Meta:
		model = Question
		exclude = ['exam', 'topLeftX', 'topLeftY', 'bottomRightX', 'bottomRightY']
	

# class NameForm(forms.Form):
# 	your_name = forms.CharField(max_length=100)
# 	your_age = forms.IntegerField()
# 	favorite_friuts = forms.CharField(max_length=20, widget=forms.Select(choices=FRUIT_CHOICES))

class UploadForm(forms.Form):
	file = forms.FileField()