from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='todo_index'),
    path('taken/', views.tasks, name='todo_tasks'),
    path('taken/<int:taskgroup_id>', views.tasks, name='todo_tasks_parameter'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('taak/<int:id>', views.detail_task, name='todo_detail'),
    path('klaar/', views.finished, name='todo_done'),
    path('laat/', views.late, name='todo_late'),
    path('nieuw/<int:taskgroup_id>', views.create_task, name='todo_create'),
    path('nieuwe-groep/', views.create_taskgroup, name='todo_new_task_group'),
    path('finish/<int:id>', views.finish_task, name='todo_finish'),
    path('unfinish/<int:id>', views.unfinish_task, name='todo_unfinish'),
    path('delete/<int:id>', views.delete_task, name='todo_delete'),
    #AJAX REQUEST LINKS
    path('taskgroup-exist', views.validate_taskgroup_name, name='todo_ajax_taskgroup_exist')
]