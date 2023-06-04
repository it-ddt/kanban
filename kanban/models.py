from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Kanban(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Доски"


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    status = models.CharField(max_length=100, default="new", verbose_name="статус")
    kanban = models.ForeignKey(Kanban, related_name="tasks", on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now().date())
    created_time = models.TimeField(default=timezone.now().time())
    assigned_date = models.DateField(null=True, blank=True)
    assigned_time = models.TimeField(null=True, blank=True)
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="исполнитель"
    )
    deadline_date = models.DateField(null=True, blank=True, verbose_name="дедлайн дата")
    deadline_time = models.TimeField(null=True, blank=True, verbose_name="дедлайн время")
    completed_date = models.DateField(null=True, blank=True)
    completed_time = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Задачи"

    def __str__(self):
        return str(self.name)
