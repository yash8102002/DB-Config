from django.db import models

from django.contrib.auth.models import User

class Client(models.Model):
    client_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    users = models.ManyToManyField(User)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name