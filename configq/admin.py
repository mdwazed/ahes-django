from django.contrib import admin
from .models import Question, Exam, CourseName, Semester
# Register your models here.



admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(CourseName)
admin.site.register(Semester)

