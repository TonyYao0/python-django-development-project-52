from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from .models import Status
from django.shortcuts import redirect
from django.db.models import ProtectedError
from django.contrib import messages


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses")
    success_message = _("Статус успешно создан")


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    fields = ["name"]
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses")
    success_message = _("Статус успешно изменен")


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses")
    success_message = _("Статус успешно удален")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request, _("Невозможно удалить статус, потому что он используется")
            )
            return redirect("statuses")
