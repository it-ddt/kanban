from django.db import models
from django.contrib.auth.models import User


class Kanban(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Канбаны"


class Task(models.Model):
    STATUSES = (
        ("new", "new"),
        ("active", "active"),
        ("completed", "completed"),
        ("overdue", "overdue"),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=STATUSES)
    kanban = models.ForeignKey(Kanban, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    assigned_date = models.DateField(auto_now_add=True)
    assigned_time = models.TimeField(auto_now_add=True)
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    completed_date = models.DateField(auto_now_add=True)
    completed_time = models.TimeField(auto_now_add=True)
