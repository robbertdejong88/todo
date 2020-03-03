from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login, logout
from todoproject.settings import BASE_DIR
from .models import Task, TaskGroup
from .forms import CreateTaskForm, LoginForm, CreateTaskGroupForm, AddUserTaskGroupForm
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
		
		return redirect('todo_tasks_parameter', taskgroup_id)

		
	else:

		if permitted_user(request.user, taskgroup_id):

			taskgroup = TaskGroup.objects.get(id=taskgroup_id)

			tasks = Task.objects.filter(task_group=taskgroup).filter(finished=False).order_by('-target_date')

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


@csrf_exempt
@login_required
def add_user_taskgroup(request, taskgroup_id):

	if request.method == 'POST':
		value = request.body.decode("utf-8") #to decode from bytes to string
		user = User.objects.get(id=value)
		group = TaskGroup.objects.get(id=taskgroup_id)
		group.user.add(user)
		username = user.username

		data = {}

		data['result'] = username + ' uitgenodigd voor ' +group.name

		return HttpResponse(json.dumps(data), content_type="application/json")



	if perimitted_owner(request.user, taskgroup_id):
		form = AddUserTaskGroupForm()



	else:
		return HttpResponse('Je bent geen eigenaar van deze groep')

	qs = {
		'form': form,
		'taskgroup_id': taskgroup_id,
	}


	
	return render(request, 'todo/addusertaskgroup.html', qs)

@login_required
def invites_user_taskgroup(request):
	if request.method == 'POST':
		taskgroup_id = request.POST.get('taskgroupid')
		accepted = request.POST.get('accepted')
		user = request.user

		if accepted == "True":
			TaskGroup.objects.get(id=taskgroup_id).accepted.add(user)
		else:
			TaskGroup.objects.get(id=taskgroup_id).user.remove(user)

	taskgroups = []
	for taskgroup in TaskGroup.objects.all():
		if request.user in taskgroup.user.all() and request.user not in taskgroup.accepted.all():
			taskgroups.append(taskgroup)


	qs = {
		'taskgroups':taskgroups
	}

	return render(request, 'todo/invitestaskgroup.html', qs)




# Permitted tests
def permitted_user(user, task_group_id):
	taskgroup = TaskGroup.objects.get(id=task_group_id)
	if user in taskgroup.user.all():
		return True
	else:
		return False




def perimitted_owner(user, taskgroup_id):
	taskgroup = TaskGroup.objects.get(id=taskgroup_id)


	if taskgroup.owner == user:
		print(taskgroup.owner)
		return True
	else:
		return False





# AJAX REQUESTST
def validate_taskgroup_name(request):
	taskgroup_name = request.GET.get('taskgroup_name')
	data = {
		'is_taken': TaskGroup.objects.filter(name__iexact=taskgroup_name).exists()
	}
	return JsonResponse(data)

@login_required
def show_users(request):
	user = request.GET.get('user')
	users = User.objects.filter(username__icontains=user).order_by('username')
	data = serializers.serialize('json',users)

	return HttpResponse(data, content_type='application/json')