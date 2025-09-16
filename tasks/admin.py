from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'status', 'priority')
    list_filter = ('status', 'priority', 'project')

admin.site.register(Task, TaskAdmin)