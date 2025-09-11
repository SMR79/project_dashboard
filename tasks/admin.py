from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'due_date', 'completed', 'project')
    list_filter = ('completed', 'project')

admin.site.register(Task, TaskAdmin)