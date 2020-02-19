from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from todoproject.settings import BASE_DIR
from .models import Task
from .forms import CreateTaskForm
from datetime import datetime


# Create your views here.
def index(request):
	tasks = Task.objects.filter(finished=False).order_by('target_date')
	qs = {
		'tasks':tasks
	}

	return render(request, 'todo/index.html', qs)

def finished(request):
	tasks = Task.objects.filter(finished=True).order_by('target_date')
	qs = {
		'tasks':tasks
	}

	return render(request, 'todo/finished.html', qs)


def late(request):
	tasks = Task.objects.filter(target_date__lt=datetime.now())
	tasks = tasks.filter(finished=False)

	qs = {
		'tasks':tasks
	}

	return render(request, 'todo/late.html', qs)


def create_task(request):

	if request.method == 'POST':
		form = CreateTaskForm(request.POST)
		print(request.POST.get('target_date'))
		if form.is_valid():
			form.save()
			return redirect('todo_index')
		else:
			print(form.errors)


	form = CreateTaskForm()

	qs = {
		'form':form,
	}
	return render(request, 'todo/create.html', qs)


def detail_task(request, id):
	task = Task.objects.get(id=id)


	if request.method == 'POST':
		form = CreateTaskForm(request.POST, instance=task)
		form.save()
		return redirect('todo_index')

	form = CreateTaskForm(instance=task)

	qs = {
		'form':form,
	}

	return render(request, 'todo/detail.html', qs)

def finish_task(request, id):
	task = Task.objects.get(id=id)

	task.finished = True
	task.save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	# return redirect('todo_index')

def unfinish_task(request, id):
	task = Task.objects.get(id=id)

	task.finished = False
	task.save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_task(request, id):
	task = Task.objects.get(id=id)

	task.delete()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	