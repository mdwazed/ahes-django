# grader.views
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, FormView

from .models import StudentAns
from .forms import UploadAnsScriptForm

from grader.src.preProcessAnsScript import ansScript

# Create your views here.

class UplaodAnsScriptView(FormView):
    form_class = UploadAnsScriptForm
    template_name = 'upload_ans_script.html'
    # success_url = reverse('grader:ans_list')  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def home(request):
	# data = test.test()
	if request.method == 'POST':
		ansc = ansScript()
		ansc.processAnsScript(request)
		ansc.readAns(request)
		context ={
			'success_message':'processing ans script complete',
		}
		return HttpResponseRedirect(reverse('grader:ans_list'))
	else:
		context={

		}
	
	return render(request, 'grader/grader_home.html', context)

def delete_ans(request):
    if request.method == 'POST':
        StudentAns.objects.all().delete()
        return HttpResponseRedirect(reverse('grader:ans_list'))

class StudentsAnsList(ListView):
    model = StudentAns

