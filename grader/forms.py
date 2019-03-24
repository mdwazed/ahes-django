from django import forms

from configq.models import Exam

class UploadAnsScriptForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class ExamGradeUpdateForm(forms.ModelForm):
    grade_5_0 = forms.CharField(label='Grade 5.0 <',)
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
        fields = ['grade_0_7', 'grade_1_0', 'grade_1_3', 'grade_1_7', 'grade_2_0', 'grade_2_3', 'grade_2_7', 'grade_3_0',
            'grade_3_3', 'grade_3_7', 'grade_4_0', 'grade_5_0',]
