# grader.views
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, FormView
from django.core.files.storage import FileSystemStorage

from .models import StudentAns
from .forms import UploadAnsScriptForm

from grader.src.preProcessAnsScript import ansScript
from grader.src import ans_grader
from configq.misc_function import get_exam


# Create your views here.


def home(request):
	context={}    
	return render(request, 'grader/grader_home.html', context)

def upload(request):
	"""
	upload all scanned image to resized folder from where all further processing will be done.

	"""
	upload_file_count = 0
	if request.method == "POST":
		myfiles = request.FILES.getlist('myfile')
		# print(myfiles)
		exam = get_exam(request)
		for file in myfiles:
			fs = FileSystemStorage()
			fs.save('raw_image/'+ str(exam.id) +'_'+file.name, file)
			upload_file_count +=1
		context = {
		'upload_file_count' : upload_file_count
		}
		return render(request, 'grader/upload_ans_script.html', context)
	else:
		context = {

		}
		return render(request, 'grader/upload_ans_script.html', context)


def read_ans_script(request):
	if request.method == 'POST':
		ansc = ansScript()
		(readFileCount, unReadFileCount) = ansc.processAnsScript(request)
		ansc.readAns(request)
		ans_grader.grade_all_ans(request)
		
		context ={
			'success_message': 'image pre processing complete',
			'readFileCount': readFileCount,
			'unReadFileCount' : unReadFileCount,
		}
	else:
		context={

		}
	
	return render(request, 'grader/read_ans_script.html', context)

def delete_ans(request):
	if request.method == 'POST':
		StudentAns.objects.filter(exam= get_exam(request)).delete()
		return HttpResponseRedirect(reverse('grader:ans_list'))

class StudentsAnsList(ListView):
	model = StudentAns
	paginated_by = 10

	def get_queryset(self):
		return StudentAns.objects.filter(exam= get_exam(self.request))


