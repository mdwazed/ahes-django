from django.urls import path

from . import views


app_name = 'grader'

urlpatterns = [
    path('', views.home, name='home'),
    path('ans_list/<str:order>/', views.StudentsAnsList.as_view(), name='ans_list_ordered'),  
    path('ans_list/', views.StudentsAnsList.as_view(), name='ans_list'),   
    path('delete_ans', views.delete_ans, name='delete_ans'), 
    path('upload', views.upload, name='upload_ans_script'),
    path('read_ans_script', views.read_ans_script, name='read_ans_script'),
    path('ans_details/<int:pk>', views.ans_details, name='ans_details'),
    path('ans_details/', views.ans_details, name='ans_details'),
    path('evaluate_ans_scripts/', views.evaluate_ans_scripts, name='evaluate_ans_scripts'),
]