import django_filters
from django import forms
from .models import Task, Status
from labels.models import Label
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label=_("Статус")
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label=_("Исполнитель")
    )

    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(), field_name="labels", label=_("Метка")
    )

    self_tasks = django_filters.BooleanFilter(
        widget=forms.CheckboxInput,
        method="filter_self_tasks",
        label=_("Только свои задачи"),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "label", "self_tasks"]

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
