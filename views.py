"""
TODO:
detail для Task
оформление главной страницы
просрочка Task
выгрузка на сервер
"""

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import date, time
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import views, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
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
        user = self.request.user
        name = form.cleaned_data['name']
        kanban_count = Kanban.objects.filter(owner=user).count()

        if Kanban.objects.filter(owner=user, name=name).exists():
            form.add_error(None, "У вас уже есть доска стаким именем! Подберите другое.")
            return self.form_invalid(form)
        
        if kanban_count >= 10:
            form.add_error(None, "Нельзя создать больше 10 досок!")
            return self.form_invalid(form)
        
        form.instance.owner = user
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

    def test_func(self):
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

    def test_func(self):
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
        kanban_id = self.kwargs['pk']
        kanban = get_object_or_404(Kanban, pk=kanban_id)
        task_count = Task.objects.filter(kanban=kanban).count()

        if kanban.tasks.filter(name=form.cleaned_data['name']).exists():
            form.add_error(None, 'Здадча с таким названием уже есть в этой доске!')
            return self.form_invalid(form)
        
        if task_count >= 100:
            form.add_error(None, "В одной доске нельзя создать больше 100 задач!")
            return self.form_invalid(form)
        
        form.instance.creator = self.request.user
        form.instance.kanban = kanban
        form.instance.created_time = timezone.localtime()
        form.instance.created_date = timezone.localtime().date()
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    context_object_name = "task"
    template_name = "kanban/task_detail.html"


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Task
    template_name = "kanban/task_delete.html"
    login_url = reverse_lazy("kanban:user_login")

    def handle_no_permission(self):
        return render(self.request, "kanban/403.html")

    def test_func(self):
        task = self.get_object()
        return task.kanban.owner == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "kanban:kanban_detail",
            kwargs = {'pk': self.object.kanban.pk}
        )


class TaskActivateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    template_name = "kanban/task_activate.html"
    fields = ["executor", "deadline_date", "deadline_time"]

    def get_success_url(self):
        return reverse_lazy(
            "kanban:kanban_detail",
            kwargs={'pk': self.object.kanban.pk}
        )
    
    def test_func(self):
        task = self.get_object()
        kanban = task.kanban
        return kanban.owner == self.request.user
    
    def handle_no_permission(self):
        return render(self.request, "kanban/403.html")

    def form_valid(self, form):
        task = form.instance
        current_datetime = timezone.localtime(timezone.now())
 
        if task.deadline_date and task.deadline_time:
            deadline_datetime = timezone.datetime.combine(task.deadline_date, task.deadline_time)
            deadline_datetime = timezone.make_aware(deadline_datetime)

            if deadline_datetime < current_datetime:
                form.add_error(None, "Дедлайн не может быть раньше, чем текущая дата и время!")
                return super().form_invalid(form)
        
        if self.object.status == "new":
            if not form.cleaned_data["executor"]:
                form.add_error(None, "Назначьте исполнителя!")
                return super().form_invalid(form)
            if not form.cleaned_data["deadline_date"]:
                form.add_error(None, "Назначьте дату дедлайна!")
                return super().form_invalid(form)
            if not form.cleaned_data["deadline_time"]:
                form.add_error(None, "Назначьте время дедлайна!")
                return super().form_invalid(form)
            self.object.status = "active"
            self.object.assigned_time = timezone.localtime()
            self.object.assigned_date = timezone.localtime().date()

        return super().form_valid(form)


class TaskCompleteView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    template_name = "kanban/task_complete.html"
    fields = []

    def test_func(self):
        task = self.get_object()
        kanban = task.kanban
        return kanban.owner == self.request.user
    
    def handle_no_permission(self):
        return render(self.request, "kanban/403.html")

    def get_success_url(self):
        return reverse_lazy(
            "kanban:kanban_detail",
            kwargs={'pk': self.object.kanban.pk}
        )

    def form_valid(self, form):
        if self.object.status == "active":
            self.object.status = "completed"
            self.object.completed_time = timezone.localtime()
            self.object.completed_date = timezone.localtime().date()
        return super().form_valid(form)


class TaskCancelView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Task
    template_name = "kanban/task_cancel.html"
    fields = []

    def test_func(self):
        task = self.get_object()
        kanban = task.kanban
        return kanban.owner == self.request.user
    
    def handle_no_permission(self):
        return render(self.request, "kanban/403.html")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(kanban__owner=self.request.user)

    def form_valid(self, form):
        form.instance.status = "new"
        form.instance.executor = None
        form.instance.deadline_date = None
        form.instance.deadline_time = None
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "kanban:kanban_detail",
            kwargs={'pk': self.object.kanban.pk}
        )


def about(request):
    return render(request, 'kanban/about.html')


@csrf_exempt
def tasks_overdue(request):
    current_datetime = timezone.localtime(timezone.now())
    current_date = current_datetime.date()
    current_time = current_datetime.time()

    overdue_tasks = Task.objects.filter(
        Q(status='active', deadline_date__lt=current_date, deadline_time__isnull=True) |
        Q(status='active', deadline_date__lt=current_date, deadline_time__lt=current_time) |
        Q(status='active', deadline_date=current_date, deadline_time__lt=current_time)
    )

    for task in overdue_tasks:
        task.status = 'overdue'
        task.save()

    return HttpResponse('Задачи с подошедшим делайном получили статус "overdue"')


def help(request):
    return render(request, 'kanban/help.html')
