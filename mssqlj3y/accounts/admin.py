from django.contrib import admin
from .models import Profile, Department

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number']

admin.site.register(Profile, ProfileAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Department, DepartmentAdmin)