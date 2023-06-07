from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Kanban(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="название",
        error_messages={
            'unique': "Доска с таким названием уже существует."
        }
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Доски"


class Task(models.Model):
    STATUS_CHOICES = [
        ('new', ('новая')),
        ('active', ('активная')),
        ('completed', ('завершенная')),
        ('overdue', ('просроченная')),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="название",
        unique=True,
        error_messages={
            'unique': "Задача с таким названием уже существует."
        }
    )
    description = models.TextField(verbose_name="описание")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new", verbose_name="статус")
    kanban = models.ForeignKey(Kanban, related_name="tasks", on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now, verbose_name="дата создания")
    created_time = models.TimeField(default=timezone.now, verbose_name="время создания")
    assigned_date = models.DateField(null=True, blank=True, verbose_name="дата назначения")
    assigned_time = models.TimeField(null=True, blank=True, verbose_name="время назначения")
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="исполнитель"
    )
    deadline_date = models.DateField(null=True, blank=True, verbose_name="дата дедлайна")
    deadline_time = models.TimeField(null=True, blank=True, verbose_name="время дедлайна")
    completed_date = models.DateField(null=True, blank=True, verbose_name="дата завершения")
    completed_time = models.TimeField(null=True, blank=True, verbose_name="время завершения")

    class Meta:
        verbose_name_plural = "Задачи"

    def __str__(self):
        return str(self.name)
    
    def get_status_display(self):
        status_display = dict(self.STATUS_CHOICES)
        return status_display.get(self.status, '')
