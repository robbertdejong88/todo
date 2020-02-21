from django.contrib import admin
from .models import Priority, Task, TaskGroup

admin.site.register(Priority)
admin.site.register(Task)
admin.site.register(TaskGroup)

