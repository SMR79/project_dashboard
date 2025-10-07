from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm, EditProjectForm


def get_project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_search')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_create.html', {'form': form})

def search_projects(request, id=None):
    if id == "active":
        projects = Project.objects.filter(status="in_progress")
    elif id == "completed":
        projects = Project.objects.filter(status="completed")
    elif id == "planned":
        projects = Project.objects.filter(status="planned")
    elif id == "my_projects":
        # tady předpokládám, že máš vazbu Project -> User (např. manager nebo owner)
        projects = Project.objects.filter(owner=request.user)
    else:
        projects = Project.objects.all()

    return render(request, "projects/project_search.html", {
        "id": id,
        "projects": projects,
    })

def project_report(request):
    stats = {
        'total_projects': Project.objects.count(),
        'active_projects': Project.objects.filter(status='in_progress').count(),
        'completed_projects': Project.objects.filter(status='completed').count(),
        'planned_projects': Project.objects.filter(status='planned').count(),
    }
    return render(request, 'projects/project_report.html', {'stats': stats})

def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = EditProjectForm(instance=project)
    return render(request, 'projects/edit_project.html', {'form': form, 'edit_project': project})

def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('project_search')
    return render(request, 'projects/confirm_delete.html', {'project': project})