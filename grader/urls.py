from django.urls import path

from . import views


app_name = 'grader'

urlpatterns = [
    path('', views.home, name='home'), 
    path('ans_list', views.StudentsAnsList.as_view(), name='ans_list'),      
    path('delete_ans', views.delete_ans, name='delete_ans'), 
    path('upload_ans_script', views.UplaodAnsScriptView.as_view(), name='upload_ans_script'),
]