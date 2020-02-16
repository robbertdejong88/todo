from django.db import models
from todoproject import settings

# Create your models here.
class Priority(models.Model):
	name = models.CharField(max_length=20)

	def __str__(self):
		return self.name


class Task(models.Model):
	short_description = models.CharField(max_length=30)
	description = models.TextField()
	target_date = models.DateField()
	priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
	finished = models.BooleanField(default=False)

	def __str__(self):
		return self.short_description




