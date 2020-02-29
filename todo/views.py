from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from todoproject.settings import BASE_DIR
from .models import Task, TaskGroup
from .forms import CreateTaskForm, LoginForm, CreateTaskGroupForm
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
	groups = TaskGroup.objects.filter(user=request.user).filter(accepted=request.user)
	qs = {
		'groups':groups
	}

	return render(request, 'todo/index.html', qs)

@login_required
def tasks(request, taskgroup_id=None):
	if taskgroup_id == None:
		taskgroup_id = request.POST.get('selected_group')
		if permitted_user(request.user, taskgroup_id):
			taskgroup = TaskGroup.objects.get(id=taskgroup_id)

			tasks = Task.objects.filter(task_group=taskgroup).filter(finished=False)

			qs = {
				'tasks':tasks,
				'taskgroup':taskgroup
			}
		else:
			return HttpResponse('Je zit niet in deze groep')

		
	else:

		if permitted_user(request.user, taskgroup_id):

			taskgroup = TaskGroup.objects.get(id=taskgroup_id)

			tasks = Task.objects.filter(task_group=taskgroup).filter(finished=False)

			qs = {
				'tasks':tasks,
				'taskgroup':taskgroup
			}

		else:
			return HttpResponse('Je zit niet in deze groep')

	return render(request, 'todo/tasks.html', qs)


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
def create_task(request, taskgroup_id):
	if permitted_user(request.user, taskgroup_id):

		if request.method == 'POST':
			taskgroup = TaskGroup.objects.get(id=taskgroup_id)
			task = Task(task_group=taskgroup)
			form = CreateTaskForm(request.POST, instance=task)
			if form.is_valid():
				form.save()
				messages.success(request, f'Nieuwe taak opgeslagen')
				return redirect('todo_tasks_parameter', taskgroup.id)
			else:
				print(form.errors)


		form = CreateTaskForm()

		qs = {
			'form':form,
			'taskgroup_id': taskgroup_id,
		}
		return render(request, 'todo/create.html', qs)

	else:
		return HttpResponse('Je zit niet in deze groep')


@login_required
def detail_task(request, id):
	task = Task.objects.get(id=id)

	taskgroup_id = task.task_group.id

	if permitted_user(request.user, taskgroup_id):
		print('permitted')
		if request.method == 'POST':
			form = CreateTaskForm(request.POST, instance=task)
			form.save()
			messages.success(request, f'{task} aangepast')
			return redirect('todo_index')

		form = CreateTaskForm(instance=task)

		qs = {
			'form':form,
			'taskgroup_id': task.task_group.id,
		}

		return render(request, 'todo/detail.html', qs)
	else:
		print('not permitted')
		return HttpResponse('Je zit niet in deze groep')

@login_required
def finish_task(request, id):
	task = Task.objects.get(id=id)

	taskgroup_id = task.task_group.id
	
	if permitted_user(request.user, taskgroup_id):
		task.finished = True
		task.save()

		messages.success(request, f'"{task}" gereed gemeld')
		return redirect('todo_tasks_parameter', task.task_group.id)

	else:
		return HttpResponse('Je zit niet in deze groep')


@login_required
def unfinish_task(request, id):
	task = Task.objects.get(id=id)

	taskgroup_id = task.task_group.id
	
	if permitted_user(request.user, taskgroup_id):

		task.finished = False
		task.save()

		messages.success(request, f'"{task}" heropend')
		return redirect('todo_tasks_parameter', task.task_group.id)

	else:
		return HttpResponse('Je zit niet in deze groep')

@login_required
def delete_task(request, id):
	task = Task.objects.get(id=id)

	taskgroup_id = task.task_group.id
	
	if permitted_user(request.user, taskgroup_id):
		task.delete()
		messages.success(request, f'"{task}" verwijderd')
		return redirect('todo_tasks_parameter', task.task_group.id)
	else:
		return HttpResponse('Je zit niet in deze groep')


@login_required
def create_taskgroup(request):

	if request.method == 'POST':
		group = TaskGroup(owner=request.user)
		form = CreateTaskGroupForm(request.POST, instance=group)
		if form.is_valid():
			form.save()
			group.user.add(request.user)
			group.accepted.add(request.user)
			return redirect('todo_tasks_parameter', group.id)
		else:
			print(form.errors)

	else:
		form = CreateTaskGroupForm()

	
	qs = {
		'form':form,

		}	
	return render(request, 'todo/createtaskgroup.html', qs)

def permitted_user(user, task_group_id):
	taskgroup = TaskGroup.objects.get(id=task_group_id)
	if user in taskgroup.user.all():
		return True
	else:
		return False








# AJAX REQUESTS:

def validate_taskgroup_name(request):
	taskgroup_name = request.GET.get('taskgroup_name')

	data = {
		'is_taken': TaskGroup.objects.filter(name__iexact=taskgroup_name).exists()
	}

	return JsonResponse(data)