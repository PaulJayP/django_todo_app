from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('delete/<int:task_id>', views.delete_task, name='delete'),
    path('edit_form/<int:task_id>', views.edit_form, name='edit_form'),
    path('edit_task/<int:task_id>', views.edit_task, name='edit_task'),
    path('create/', views.create_task, name='create'),
    path('create_form/', views.create_form, name='create_form')
]