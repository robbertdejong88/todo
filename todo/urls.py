from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='todo_index'),
    path('taak/<int:id>', views.detail_task, name='todo_detail'),
    path('klaar/', views.finished, name='todo_done'),
    path('laat/', views.late, name='todo_late'),
    path('nieuw/', views.create_task, name='todo_create'),
    path('finish/<int:id>', views.finish_task, name='todo_finish'),
    path('unfinish/<int:id>', views.unfinish_task, name='todo_unfinish'),
    path('delete/<int:id>', views.delete_task, name='todo_delete'),
]