from django.contrib import admin
from .models import Kanban, Task

admin.site.register(Kanban)
admin.site.register(Task)