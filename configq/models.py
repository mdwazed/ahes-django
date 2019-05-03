from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save

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
	course_name = models.ForeignKey('CourseName', on_delete=models.CASCADE)
	semester = models.ForeignKey('Semester', on_delete=models.CASCADE)		
	credit_point = models.CharField(max_length=2)
	professor = models.CharField(max_length=100, null=True)
	exam_code = models.CharField(max_length=20, null=True, blank=True)
	total_marks = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
	grade_5_0 = models.DecimalField(max_digits= 5, decimal_places=3, default=50.000)
	grade_4_0 = models.DecimalField(max_digits= 5, decimal_places=3, default=50.000)
	grade_3_7 = models.DecimalField(max_digits= 5, decimal_places=3, default=55.000)
	grade_3_3 = models.DecimalField(max_digits= 5, decimal_places=3, default=60.000)
	grade_3_0 = models.DecimalField(max_digits= 5, decimal_places=3, default=65.000)
	grade_2_7 = models.DecimalField(max_digits= 5, decimal_places=3, default=70.000)
	grade_2_3 = models.DecimalField(max_digits= 5, decimal_places=3, default=75.000)
	grade_2_0 = models.DecimalField(max_digits= 5, decimal_places=3, default=80.000)
	grade_1_7 = models.DecimalField(max_digits= 5, decimal_places=3, default=85.000)
	grade_1_3 = models.DecimalField(max_digits= 5, decimal_places=3, default=90.000)
	grade_1_0 = models.DecimalField(max_digits= 5, decimal_places=3, default=95.000)
	grade_0_7 = models.DecimalField(max_digits= 6, decimal_places=3, default=99.000)


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
	allotedMarks = models.SmallIntegerField()
	threshold = models.DecimalField(max_digits=3, decimal_places=2)
	topLeftX = models.SmallIntegerField()
	topLeftY = models.SmallIntegerField()
	bottomRightX = models.SmallIntegerField()
	bottomRightY = models.SmallIntegerField()	
	questionText = models.TextField(max_length = 500)
	questionAns = models.TextField(max_length = 500)

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
		return str(self.exam.course_name)+'-'+ str(self.page)

# signal to delete image from file system if realted data from db is deleted
@receiver(post_delete, sender=UploadQuestion)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

class PageConfig(models.Model):
	"""
	Store all page level configuration data  like location of page number, matriculation number etc  
	"""
	upload_question = models.OneToOneField('UploadQuestion', on_delete=models.CASCADE, primary_key=True)
	# page = models.SmallIntegerField(null=True)
	# question_page = models.OneToOneField(UploadQuestion, on_delete= models.CASCADE)
	mat_digit_count = models.SmallIntegerField(null=True, blank=True, default=7)

	mat_digit_1_top_left_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_1_top_left_y = models.SmallIntegerField(null=True, blank=True)
	mat_digit_1_bottom_right_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_1_bottom_right_y = models.SmallIntegerField(null=True, blank=True)

	mat_digit_2_top_left_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_2_top_left_y = models.SmallIntegerField(null=True, blank=True)
	mat_digit_2_bottom_right_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_2_bottom_right_y = models.SmallIntegerField(null=True, blank=True)

	mat_digit_3_top_left_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_3_top_left_y = models.SmallIntegerField(null=True, blank=True)
	mat_digit_3_bottom_right_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_3_bottom_right_y = models.SmallIntegerField(null=True, blank=True)

	mat_digit_4_top_left_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_4_top_left_y = models.SmallIntegerField(null=True, blank=True)
	mat_digit_4_bottom_right_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_4_bottom_right_y = models.SmallIntegerField(null=True, blank=True)

	mat_digit_5_top_left_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_5_top_left_y = models.SmallIntegerField(null=True, blank=True)
	mat_digit_5_bottom_right_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_5_bottom_right_y = models.SmallIntegerField(null=True, blank=True)

	mat_digit_6_top_left_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_6_top_left_y = models.SmallIntegerField(null=True, blank=True)
	mat_digit_6_bottom_right_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_6_bottom_right_y = models.SmallIntegerField(null=True, blank=True)

	mat_digit_7_top_left_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_7_top_left_y = models.SmallIntegerField(null=True, blank=True)
	mat_digit_7_bottom_right_x = models.SmallIntegerField(null=True, blank=True)
	mat_digit_7_bottom_right_y = models.SmallIntegerField(null=True, blank=True)

	page_no_top_left_x = models.SmallIntegerField(null=True, blank=True)
	page_no_top_left_y = models.SmallIntegerField(null=True, blank=True)
	page_no_bottom_right_x = models.SmallIntegerField(null=True, blank=True)
	page_no_bottom_right_y = models.SmallIntegerField(null=True, blank=True)

	def __str__(self ):
		return 'page config id:'+str(self.upload_question)

		
# signal to create a page config object and save to db if a question image is uploaded
@receiver(post_save, sender=UploadQuestion)
def page_config_create(sender, instance, **kwargs):
	page_config_instance = PageConfig(upload_question=instance)
	page_config_instance.save()

	# print(page_config_instance)





	


 