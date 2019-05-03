from django.db import models
from configq.models import UploadQuestion, PageConfig, Exam, Question

# Create your models here.

class PageParameter(PageConfig):

    class Meta:
        proxy = True

    def get_mat_no_boxes(self):
        pass

    def get_page_no_box(self):
        pass

class StudentAns(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    matriculation_num = models.CharField(max_length=10)
    question_num = models.CharField(max_length=5)
    students_ans = models.TextField(max_length=500, null=True, blank=True)
    matching_confidence = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    auto_grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    final_grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    manually_graded = models.BooleanField(default=False)

    class Meta:
        unique_together= ('exam', 'matriculation_num', 'question_num')


    def __str__(self):
        return('mat_no:'+self.matriculation_num+'--'+'Question_no'+self.question_num)
    @property
    def alloted_marks(self):
        question = Question.objects.get(exam=self.exam, question_number=self.question_num)
        # return question.allotedMarks
        return question.allotedMarks