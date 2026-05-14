from django.shortcuts import render
from .models import Task
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from .filters import TaskFilter
from django_filters.views import FilterView


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')
    def get_success_message(self, cleaned_data):
        return 'Задача успешно создана'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks')


    def get_success_message(self, cleaned_data):
        return 'Задача успешно изменена'


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')


    def get_success_message(self, cleaned_data):
        return 'Задача успешно удалена'


    def test_func(self):
        return self.get_object().author == self.request.user


    def handle_no_permission(self):
        messages.error(self.request, 'Задачу может удалить только ее автор')
        return redirect('tasks')
