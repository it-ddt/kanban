"""
TODO:
detail для Task
оформление главной страницы
просрочка Task
выгрузка на сервер
регистрация пользователей по ивайтам
"""


from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Kanban, Task
from django.db.models import Q


class LoginView(views.LoginView):
    fields = "__all__"
    template_name = "kanban/login.html"


class LogoutView(views.LogoutView):
    next_page = reverse_lazy("kanban:index")


class KanbanListView(generic.ListView):
    model = Kanban
    template_name = "kanban/index.html"
    context_object_name = "kanbans"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Kanban.objects.none()

        # If the user is a kanban owner or executor of any task of kanban
        kanbans = Kanban.objects.filter(Q(owner=user) | Q(tasks__executor=user)).distinct()
        return kanbans


class KanbanCreateView(LoginRequiredMixin, generic.CreateView):
    model = Kanban
    template_name = "kanban/kanban_create.html"
    success_url = reverse_lazy("kanban:index")
    fields = ["name"]
    login_url = reverse_lazy("kanban:login")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class KanbanDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Kanban
    template_name = "kanban/kanban_delete.html"
    success_url = reverse_lazy("kanban:index")
    login_url = reverse_lazy("kanban:login")

    def handle_no_permission(self):
        return render(self.request, "kanban/403.html")

    def test_func(self) -> bool | None:
        kanban = get_object_or_404(Kanban, pk=self.kwargs.get("pk"))
        return kanban.owner == self.request.user


class KanbanDetailView(generic.DetailView):
    model = Kanban
    template_name = "kanban/kanban_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kanban = self.get_object()
        context["tasks_new"] = Task.objects.filter(kanban=kanban, status="new")
        context["tasks_active"] = Task.objects.filter(kanban=kanban, status="active")
        context["tasks_completed"] = Task.objects.filter(kanban=kanban, status="completed")
        context["tasks_overdue"] = Task.objects.filter(kanban=kanban, status="overdue")
        return context


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Task
    template_name = "kanban/task_create.html"
    success_url = reverse_lazy("kanban:index")
    fields = ["name", "description"]
    login_url = reverse_lazy("kanban:login")

    def test_func(self) -> bool | None:
        kanban = get_object_or_404(Kanban, pk=self.kwargs.get("pk"))
        return kanban.owner == self.request.user

    def handle_no_permission(self):
        return render(self.request, "kanban/403.html")

    def get_success_url(self):
        return reverse_lazy(
            "kanban:kanban_detail",
            kwargs={'pk': self.object.kanban.pk}
        )

    def form_valid(self, form):
        form.instance.kanban = Kanban.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Task
    template_name = "kanban/task_delete.html"
    login_url = reverse_lazy("kanban:login")

    def handle_no_permission(self):
        return render(self.request, "kanban/403.html")

    def test_func(self) -> bool | None:
        task = self.get_object()
        return task.kanban.owner == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "kanban:kanban_detail",
            kwargs = {'pk': self.object.kanban.pk}
        )


class TaskActivateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    template_name = "kanban/task_activate.html"
    fields = ["executor", "deadline_date", "deadline_time"]

    def get_success_url(self):
        return reverse_lazy(
            "kanban:kanban_detail",
            kwargs={'pk': self.object.kanban.pk}
        )

    def form_valid(self, form):
        if self.object.status == "new":
            if not form.cleaned_data["executor"]:
                form.add_error("executor", "Назначьте исполнителя!")
                return super().form_invalid(form)
            if not form.cleaned_data["deadline_date"]:
                form.add_error("deadline_date", "Назначьте дату дедлайна!")
                return super().form_invalid(form)
            if not form.cleaned_data["deadline_time"]:
                form.add_error("deadline_time", "Назначьте время дедлайна!")
                return super().form_invalid(form)
            self.object.status = "active"
            self.object.assigned_time = timezone.now().time()
            self.object.assigned_date = timezone.now().date()
        return super().form_valid(form)


class TaskCompleteView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    template_name = "kanban/task_complete.html"
    fields = []

    def get_success_url(self):
        return reverse_lazy(
            "kanban:kanban_detail",
            kwargs={'pk': self.object.kanban.pk}
        )

    def form_valid(self, form):
        if self.object.status == "active":
            self.object.status = "completed"
            self.object.completed_time = timezone.now().time()
            self.object.completed_date = timezone.now().date()
        return super().form_valid(form)
