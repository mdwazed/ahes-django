from django.db import models

# Create your models here.

class CourseName(models.Model):
	course_name = models.CharField(max_length=100)

	def __str__(self):
		return self.course_name


class Semester(models.Model):
	semester = models.CharField(max_length=50)

	def __str__(self):
		return self.semester

class Exam(models.Model):
	"""
	each object corresponds to a single course within a single semester. 
	"""
	course_name = models.ForeignKey(CourseName, on_delete=models.CASCADE)
	semester = models.ForeignKey(Semester, on_delete=models.CASCADE)		
	credit_point = models.CharField(max_length=2)
	professor = models.CharField(max_length=100, null=True)

	class Meta:
		unique_together = ('course_name', 'semester')

	def __str__(self):
		return str(self.course_name) + '-' + str(self.semester)

	

class Question(models.Model):
	"""
	hold parameter like answer box location on image, question number, page number in actual exam script,
	instructor provided answer of the question with which students answer will be compared during evaluation.
	"""
	exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
	page = models.SmallIntegerField()
	question_number = models.CharField(max_length=5)
	topLeftX = models.SmallIntegerField()
	topLeftY = models.SmallIntegerField()
	bottomRightX = models.SmallIntegerField()
	bottomRightY = models.SmallIntegerField()	
	questionText = models.TextField(max_length = 500)
	questionAns = models.TextField(max_length = 200)

	class Meta:
		unique_together = ('exam', 'page', 'question_number')

	def __str__(self):
		return self.questionText

class UploadQuestion(models.Model):
	"""
	upload actual question image to be used during question configuration. user will select ans box from these images
	"""
	exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
	page = models.SmallIntegerField()
	description = models.CharField(max_length=100, null=True, blank=True)
	image = models.ImageField(upload_to='questions/')

	class Meta:
		unique_together = ('exam', 'page')

	def get_image_url(self):
		return self.image

	def __str__(self):
		return str(exam + self.image)

class PageConfig(models.Model):
	"""
	Store all page level configuration data  like location of page number, matriculation number etc  
	"""
	exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
	page = models.SmallIntegerField()
	mat_digit_count = models.SmallIntegerField()

	mat_digit_1_top_left_x = models.SmallIntegerField()
	mat_digit_1_top_left_y = models.SmallIntegerField()
	mat_digit_1_bottom_right_x = models.SmallIntegerField()
	mat_digit_1_bottom_right_y = models.SmallIntegerField()

	mat_digit_2_top_left_x = models.SmallIntegerField()
	mat_digit_2_top_left_y = models.SmallIntegerField()
	mat_digit_2_bottom_right_x = models.SmallIntegerField()
	mat_digit_2_bottom_right_y = models.SmallIntegerField()

	mat_digit_3_top_left_x = models.SmallIntegerField()
	mat_digit_3_top_left_y = models.SmallIntegerField()
	mat_digit_3_bottom_right_x = models.SmallIntegerField()
	mat_digit_3_bottom_right_y = models.SmallIntegerField()

	mat_digit_4_top_left_x = models.SmallIntegerField()
	mat_digit_4_top_left_y = models.SmallIntegerField()
	mat_digit_4_bottom_right_x = models.SmallIntegerField()
	mat_digit_4_bottom_right_y = models.SmallIntegerField()

	mat_digit_5_top_left_x = models.SmallIntegerField()
	mat_digit_5_top_left_y = models.SmallIntegerField()
	mat_digit_5_bottom_right_x = models.SmallIntegerField()
	mat_digit_5_bottom_right_y = models.SmallIntegerField()

	mat_digit_6_top_left_x = models.SmallIntegerField()
	mat_digit_6_top_left_y = models.SmallIntegerField()
	mat_digit_6_bottom_right_x = models.SmallIntegerField()
	mat_digit_6_bottom_right_y = models.SmallIntegerField()

	mat_digit_7_top_left_x = models.SmallIntegerField()
	mat_digit_7_top_left_y = models.SmallIntegerField()
	mat_digit_7_bottom_right_x = models.SmallIntegerField()
	mat_digit_7_bottom_right_y = models.SmallIntegerField()

	page_no_top_left_x = models.SmallIntegerField()
	page_no_top_left_y = models.SmallIntegerField()
	page_no_bottom_right_x = models.SmallIntegerField()
	page_no_bottom_right_y = models.SmallIntegerField()

	def __str__(self ):
		return str(self.exam +'-'+ self.page)








	


 