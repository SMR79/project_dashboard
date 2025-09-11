from django.shortcuts import render
from .models import Project

def get_project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

def get_project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})