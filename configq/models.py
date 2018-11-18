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


	def __str__(self):
		return str(self.course_name) + '-' + str(self.semester)

	class Meta:
		unique_together = ('course_name', 'semester')

class Question(models.Model):
	"""
	hold parameter like answer box location on image, question number, page number in actual exam script,
	instructor provided answer of the question with which students answer will be compared during evaluation.
	"""
	topLeftX = models.SmallIntegerField()
	topLeftY = models.SmallIntegerField()
	bottomRightX = models.SmallIntegerField()
	bottomRightY = models.SmallIntegerField()
	exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
	page = models.SmallIntegerField()
	questionText = models.TextField(max_length = 500,  blank=True)
	questionAns = models.TextField(max_length = 200, blank=True)

	def __str__(self):
		return self.questionText



	


 