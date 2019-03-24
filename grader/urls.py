
# urls of grader app

from django.urls import path, re_path

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
    path('change_threshold/', views.change_threshold, name='change_threshold'),
    path('change_final_grade/', views.change_final_grade, name='change_final_grade'),
    path('final_result', views.final_result, name='final_result'),
    path('finalize_result', views.finalize_result, name='finalize_result'),
    path('publish_result', views.publish_result, name='publish_result'),
    path('update_exam_grade_thresh', views.update_exam_grade_thresh, name='update_exam_grade_thresh'),
]