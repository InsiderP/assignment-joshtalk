from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom user model with additional fields"""
    mobile = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

class Task(models.Model):
    """Task model representing a task in the system"""
    class TaskStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')

    class TaskType(models.TextChoices):
        FEATURE = 'FEATURE', _('Feature')
        BUG = 'BUG', _('Bug')
        ENHANCEMENT = 'ENHANCEMENT', _('Enhancement')

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.FEATURE
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    assigned_users = models.ManyToManyField(
        User,
        related_name='assigned_tasks',
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

# 11. tasks/serializers.py
from rest_framework import serializers
from .models import Task, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'first_name', 'last_name']
        read_only_fields = ['id']

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)
    assigned_user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'created_at', 'updated_at',
            'completed_at', 'task_type', 'status', 'assigned_users',
            'assigned_user_ids', 'created_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def create(self, validated_data):
        assigned_user_ids = validated_data.pop('assigned_user_ids', [])
        task = Task.objects.create(**validated_data)
        
        if assigned_user_ids:
            users = User.objects.filter(id__in=assigned_user_ids)
            task.assigned_users.set(users)
        
        return task

    def update(self, instance, validated_data):
        assigned_user_ids = validated_data.pop('assigned_user_ids', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if assigned_user_ids is not None:
            users = User.objects.filter(id__in=assigned_user_ids)
            instance.assigned_users.set(users)
        
        instance.save()
        return instance

# 12. tasks/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
