from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Task

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'mobile', 'is_staff')
    search_fields = ('username', 'email', 'mobile')
    ordering = ('username',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'task_type', 'created_at')
    list_filter = ('status', 'task_type')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)