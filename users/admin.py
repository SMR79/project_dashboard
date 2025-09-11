from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):    
    # Define the fields to be displayed in the admin interface
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')    
    # Add the 'role' field to the fieldsets and add_fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )


# Registration of the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)