from django.urls import path

from . import views

app_name = 'configq'

urlpatterns = [
    path('', views.home, name='home'),
    path('exam/', views.exam_config, name='exam_config'),
    path('question/', views.question_config, name='question_config'),
    path('question_list/', views.question_list, name='question_list'),
    path('get_name/', views.get_name, name='get_name'),
    path('upload_file/', views.upload_file, name='upload_file'),      
]