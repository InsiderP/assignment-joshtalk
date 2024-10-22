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
