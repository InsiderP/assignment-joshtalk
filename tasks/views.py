from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Task, User
from .serializers import TaskSerializer, UserSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling task-related operations
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned tasks to a given user,
        by filtering against a `user_id` query parameter in the URL.
        """
        queryset = Task.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(assigned_users__id=user_id)
        return queryset

    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def assign_users(self, request, pk=None):
        """
        Assign users to a task
        """
        task = self.get_object()
        user_ids = request.data.get('user_ids', [])
        
        try:
            users = User.objects.filter(id__in=user_ids)
            task.assigned_users.set(users)
            return Response({
                'status': 'success',
                'message': 'Users assigned successfully'
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """
        Get all tasks assigned to the current user
        """
        tasks = Task.objects.filter(assigned_users=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)