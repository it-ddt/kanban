from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import views
from .models import Kanban, Task

class LoginView(views.LoginView):
    fields = "__all__"
    template_name = "kanban/login.html"

class LogoutView(views.LogoutView):
    next_page = reverse_lazy("kanban:index")

class KanbanListView(generic.ListView):
    model = Kanban
    template_name = "kanban/index.html"
    context_object_name = "kanbans"  # вместо object_list

class KanbanCreateView(generic.CreateView):
    model = Kanban
    template_name = "kanban/kanban_create.html"
    success_url = reverse_lazy("kanban:index")
    fields = ["name"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class KanbanDeleteView(generic.DeleteView):
    model = Kanban
    template_name = "kanban/kanban_delete.html"
    success_url = reverse_lazy("kanban:index")

class KanbanDetailView(generic.DetailView):
    model = Kanban
    template_name = "kanban/kanban_detail.html"
    context_object_name = "kanban"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Отфильтровать задачи с помощью querry_set
        context["new_tasks"] = "новые задачи"
        context["active_tasks"] = "новые задачи"
        context["completed_tasks"] = "новые задачи"
        return context

class TaskCreateView(generic.CreateView):
    model = Task
    template_name = "kanban/task_create.html"
    success_url = reverse_lazy("kanban:index")  # TODO: отпраить пользователя к тому канбану, для которого создана эта задача
    fields = ["name", "description", "kanban"]

    def get_success_url(self):
        return reverse_lazy(
            "kanban:kanban_detail",
            kwargs = {'pk': self.object.kanban.pk}
        )

class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "kanban/task_delete.html"
    
    def get_success_url(self):
        return reverse_lazy(
            "kanban:kanban_detail",
            kwargs = {'pk': self.object.kanban.pk}
        )


