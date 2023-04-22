from django.urls import path
from .views import (
    KanbanCreateView,
    KanbanListView,
    KanbanDeleteView,
    KanbanDetailView,
    TaskCreateView,
    LoginView,
    LogoutView,
)

app_name = "kanban"

urlpatterns = [
    path("", KanbanListView.as_view(), name="index"),
    path("kanban_create", KanbanCreateView.as_view(), name="kanban_create"),
    path("kanban_delete/<int:pk>", KanbanDeleteView.as_view(), name="kanban_delete"),
    path("kanban_detail/<int:pk>", KanbanDetailView.as_view(), name="kanban_detail"),
    path("task_create", TaskCreateView.as_view(), name="task_create"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]