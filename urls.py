from django.urls import path
from .views import (
    KanbanCreateView,
    KanbanListView,
    KanbanDeleteView,
    KanbanDetailView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskActivateView,
    TaskCancelView,
    TaskCompleteView,
    LoginView,
    LogoutView,
    SignUpView,
)

app_name = "kanban"

urlpatterns = [
    path("", KanbanListView.as_view(), name="index"),
    path("kanban_create", KanbanCreateView.as_view(), name="kanban_create"),
    path("kanban_delete/<int:pk>", KanbanDeleteView.as_view(), name="kanban_delete"),
    path("kanban_detail/<int:pk>", KanbanDetailView.as_view(), name="kanban_detail"),
    path("task_create/<int:pk>", TaskCreateView.as_view(), name="task_create"),
    path("task_detail/<int:pk>", TaskDetailView.as_view(), name="task_detail"),
    path("task_delete/<int:pk>", TaskDeleteView.as_view(), name="task_delete"),
    path("task_activate/<int:pk>", TaskActivateView.as_view(), name="task_activate"),
    path("task_cancel/<int:pk>", TaskCancelView.as_view(), name="task_cancel"),
    path("task_complete/<int:pk>", TaskCompleteView.as_view(), name="task_complete"),
    path("user_login", LoginView.as_view(), name="user_login"),
    path("user_logout", LogoutView.as_view(), name="user_logout"),
    path("user_register", SignUpView.as_view(), name="user_register"),
]