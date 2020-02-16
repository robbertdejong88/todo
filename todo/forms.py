from django.forms import ModelForm, TextInput, Textarea, DateInput, Select
from .models import Task


class CreateTaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['short_description', 'description', 'target_date', 'priority']
		widgets = {
			'short_description': TextInput(attrs={'class':'form-control transparant'}),
			'description': Textarea(attrs={'class':'form-control transparant'}),
			'target_date': DateInput(format=('%Y-%m-%d') ,attrs={'class':'datepicker form-control transparant'}),
			'priority': Select(attrs={'class':'form-control transparant'}),

		}