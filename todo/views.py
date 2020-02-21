from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from todoproject.settings import BASE_DIR
from .models import Task, TaskGroup
from .forms import CreateTaskForm, LoginForm
from datetime import datetime
from django.contrib import messages


def login_view(request):
	if request.method == 'POST':
		username = request.POST['username'].lower()
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			next_url = request.GET.get('next')
			if next_url:
				messages.success(request, f'welkom terug {request.user}')
				return redirect(request.GET.get('next'))
			else:
				messages.success(request, f'welkom terug {request.user}')
				return redirect('todo_index')
		else:
			messages.warning(request, 'Verkeerde gebruikersnaam of wachtwoord')
			return redirect('login')

	form = LoginForm()
	qs = {
	'form':form,
	}
	
	return render(request, 'todo/login.html', qs)


def logout_view(request):
	logout(request)
	return redirect('login')

@login_required
def index(request):
	tasks = Task.objects.filter(finished=False).order_by('target_date')
	groups = TaskGroup.objects.filter(user=request.user).filter(accepted=request.user)
	qs = {
		'tasks':tasks,
		'groups':groups
	}

	return render(request, 'todo/index.html', qs)

@login_required
def finished(request):
	tasks = Task.objects.filter(finished=True).order_by('target_date')
	qs = {
		'tasks':tasks
	}

	return render(request, 'todo/finished.html', qs)

@login_required
def late(request):
	tasks = Task.objects.filter(target_date__lt=datetime.now())
	tasks = tasks.filter(finished=False)

	qs = {
		'tasks':tasks
	}

	return render(request, 'todo/late.html', qs)

@login_required
def create_task(request):

	if request.method == 'POST':
		form = CreateTaskForm(request.POST)
		print(request.POST.get('target_date'))
		if form.is_valid():
			form.save()
			messages.success(request, f'Nieuwe taak opgeslagen')
			return redirect('todo_index')
		else:
			print(form.errors)


	form = CreateTaskForm()

	qs = {
		'form':form,
	}
	return render(request, 'todo/create.html', qs)

@login_required
def detail_task(request, id):
	task = Task.objects.get(id=id)


	if request.method == 'POST':
		form = CreateTaskForm(request.POST, instance=task)
		form.save()
		messages.success(request, f'{task} aangepast')
		return redirect('todo_index')

	form = CreateTaskForm(instance=task)

	qs = {
		'form':form,
	}

	return render(request, 'todo/detail.html', qs)

@login_required
def finish_task(request, id):
	task = Task.objects.get(id=id)

	task.finished = True
	task.save()

	messages.success(request, f'"{task}" gereed gemeld')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	# return redirect('todo_index')

@login_required
def unfinish_task(request, id):
	task = Task.objects.get(id=id)

	task.finished = False
	task.save()

	messages.success(request, f'"{task}" heropend')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_task(request, id):
	task = Task.objects.get(id=id)

	task.delete()
	messages.success(request, f'"{task}" verwijderd')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))