from django.urls import path

from . import views

app_name = 'configq'

urlpatterns = [
    path('', views.home, name='home'),
    path('exam/', views.exam_config, name='exam_config'),
    path('select_exam/', views.select_exam, name='select_exam'),
    path('question_image_upload/', views.question_image_upload, name='question_image_upload'),
    path('delete_question_image/', views.delete_question_image, name='delete_question_image'),
    path('page/', views.page_config, name='page_config'),
    path('edit_question/', views.edit_question, name='edit_question'),
    path('delete_question/', views.delete_question, name='delete_question'),
    path('question/', views.question_config, name='question_config'),
    path('pre_question/', views.pre_question_config, name='pre_question_config'),
    path('question_list/', views.question_list, name='question_list'),

    
  
    path('get_name/', views.get_name, name='get_name'),
    path('upload_file/', views.upload_file, name='upload_file'),      
]