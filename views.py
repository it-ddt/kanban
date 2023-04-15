from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .models import Kanban


class KanbanListView(generic.ListView):
    model = Kanban
    template_name = "kanban/index.html"
    context_object_name = "kanbans"  # вместо object_list


class KanbanCreateView(generic.CreateView):
    model = Kanban
    template_name = "kanban/kanban_create.html"
    success_url = reverse_lazy("kanban:index")
    fields = "__all__"


class KanbanDeleteView(generic.DeleteView):
    model = Kanban
    template_name = "kanban/kanban_delete.html"
    success_url = reverse_lazy("kanban:index")


class KanbanDetailView(generic.DetailView):
    model = Kanban
    template_name = "kanban/kanban_detail.html"