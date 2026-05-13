from django.shortcuts import render
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserForm, UserUpdateForm

class UsersListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегистрирован')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('users')
    success_message = _('Пользователь успешно изменен')


    def test_func(self):
        return self.get_object() == self.request.user


    def handle_no_permission(self):
        messages.error(self.request, _('У вас нет прав для изменения другого пользователя'))
        return redirect('users')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = _('Пользователь успешно удален')


    def test_func(self):
        return self.get_object() == self.request.user


    def handle_no_permission(self):
        messages.error(self.request, _('У вас нет прав для изменения другого пользователя'))
        return redirect('users')


    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, _('Невозможно удалить пользователя, потому что он используется'))
            return redirect('users')