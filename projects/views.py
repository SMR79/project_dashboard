from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm


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
    pass