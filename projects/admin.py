from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date', 'status')
    search_fields = ('name', 'status')
    list_filter = ('status', 'start_date', 'end_date')


admin.site.register(Project, ProjectAdmin)