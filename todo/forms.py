from django.forms import ModelForm, Form, TextInput, Textarea, DateInput, Select, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Task, TaskGroup



class LoginForm(AuthenticationForm):
	class Meta:
		model = User
		fields = ['username', 'password']
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget = TextInput(attrs={'class': 'form-control transparant', 'placeholder': 'Gebruikersnaam'})
		self.fields['username'].label = False
		self.fields['password'].widget = PasswordInput(attrs={'class': 'form-control transparant mt-2', 'placeholder':'Wachtwoord'}) 
		self.fields['password'].label = False


class CreateTaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['short_description', 'description', 'target_date', 'priority']
		widgets = {
			'short_description': TextInput(attrs={'class':'form-control transparant', 'autofocus':'autofocus'}),
			'description': Textarea(attrs={'class':'form-control transparant'}),
			'target_date': DateInput(format=('%Y-%m-%d') ,attrs={'class':'datepicker form-control transparant'}),
			'priority': Select(attrs={'class':'form-control transparant'})

		}
		labels = {
			'short_description': 'Korte Omschrijving',
			'description': 'Omschrijving',
			'target_date': 'Streef Datum',
			'priority': 'Prioriteit'
		}


class CreateTaskGroupForm(ModelForm):
	class Meta:
		model = TaskGroup
		fields= ['name']
		widgets = {
			'name': TextInput(attrs={'class': 'form-control transparant', 'autofocus':'autofocus'})
		}
		labels = {
			'name':'Groeps naam',
		}



class AddUserTaskGroupForm(ModelForm):
	class Meta:
		model = TaskGroup
		fields = ['user']
		widgets = {
			'user': TextInput(attrs={'class': 'form-control transparant', 'autofocus':'autofocus'})
		}
		labels = {
			'user': 'Gebruikersnaam'
		}