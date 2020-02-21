from django.db import models
from todoproject import settings
from django.contrib.auth.models import User

# Create your models here.
class Priority(models.Model):
	name = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return self.name


class TaskGroup(models.Model):
	name = models.CharField(max_length=30, unique=True)
	user = models.ManyToManyField(User)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='TaskGroupOwner')
	accepted = models.ManyToManyField(User, related_name='TaskGroupAccepted')

	def __str__(self):
		return self.name


class Task(models.Model):
	short_description = models.CharField(max_length=30)
	description = models.TextField()
	target_date = models.DateField()
	priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
	task_group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
	finished = models.BooleanField(default=False)

	def __str__(self):
		return self.short_description




