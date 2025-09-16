from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.utils.timezone import now


def get_task_list(request):
    tasks = Task.objects.all()    
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'today': now().date()})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_create.html', {'form': form})

def get_task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})

def generate_task_report(request):
    tasks = Task.objects.all()
    stats = {
        "pending": Task.objects.filter(status="pending").count(),
        "in_progress": Task.objects.filter(status="in_progress").count(),
        "on_hold": Task.objects.filter(status="on_hold").count(),
        "review": Task.objects.filter(status="review").count(),
        "completed": Task.objects.filter(status="completed").count(),
        "cancelled": Task.objects.filter(status="cancelled").count(),
        "overdue": Task.objects.filter(due_date__lt=now(), status__in=["pending", "in_progress", "on_hold"]).count(),
    }
        
    return render(request, 'tasks/task_report.html', {'stats': stats})



