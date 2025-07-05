from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, UserSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        client = self.get_object()
        projects = client.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        client = get_object_or_404(Client, id=client_id)

        project_name = request.data.get('project_name')
        user_ids = [user['id'] for user in request.data.get('users', [])]
        users = User.objects.filter(id__in=user_ids)

        project = Project.objects.create(
            project_name=project_name,
            client=client,
            created_by=request.user
        )
        project.users.set(users)
        project.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)
