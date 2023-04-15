from django.db import models


class Kanban(models.Model):
    name = models.CharField(max_length=100)

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
    assigned_date = models.DateField(auto_now_add=True)
    assigned_time = models.TimeField(auto_now_add=True)