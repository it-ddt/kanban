"""
TODO:
detail для Task
оформление главной страницы
просрочка Task
выгрузка на сервер
"""
from __future__ import annotations
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import views, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Kanban, Task
from .forms import SignUpForm


class LoginView(views.LoginView):
    fields = "__all__"
    template_name = "kanban/user_login.html"
    success_url = reverse_lazy("kanban:index")

    def get_success_url(self):
        return self.success_url


class LogoutView(views.LogoutView):
    next_page = reverse_lazy("kanban:index")


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('kanban:index')
    template_name = 'kanban/user_signup.html'

    def form_valid(self, form):
        """ автоматически логинит удачно созданного юзера """
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return response


class KanbanListView(generic.ListView):
    model = Kanban
    template_name = 'kanban/index.html'
    context_object_name = 'kanbans'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context['login_required'] = True
        else:
            user = self.request.user
            my_kanbans = Kanban.objects.filter(owner=user)
            partner_kanbans = Kanban.objects.filter(tasks__executor=user).distinct()
            kanbans = my_kanbans.union(partner_kanbans)
            context['my_kanbans'] = my_kanbans
            context['partner_kanbans'] = partner_kanbans
            context['kanbans'] = kanbans
        return context


class KanbanCreateView(LoginRequiredMixin, generic.CreateView):
    model = Kanban
    template_name = "kanban/kanban_create.html"
    fields = ["name"]
    login_url = reverse_lazy("kanban:user_login")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.id
        return reverse('kanban:kanban_detail', kwargs={'pk': pk})


class KanbanDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Kanban
    template_name = "kanban/kanban_delete.html"
    success_url = reverse_lazy("kanban:index")
    login_url = reverse_lazy("kanban:user_login")

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
    login_url = reverse_lazy("kanban:user_login")

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


class TaskDetailView(LoginRequiredMixin, generic.DetailView):  # TODO: запретить просмотр, если я не owner
    model = Task
    context_object_name = "task"
    template_name = "kanban/task_detail.html"


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Task
    template_name = "kanban/task_delete.html"
    login_url = reverse_lazy("kanban:user_login")

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
