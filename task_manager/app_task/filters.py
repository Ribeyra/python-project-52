import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.app_label.models import Label
from task_manager.app_status.models import Status
from task_manager.app_user.models import User
from .models import Task


class TaskFilter(django_filters.FilterSet):
    status__name = django_filters.ModelChoiceFilter(
        label=_('Status'),
        queryset=Status.objects.order_by('id'),
        empty_label=_('---------')
    )
    assignee__username = django_filters.ModelChoiceFilter(
        label=_('Assignee'),
        queryset=User.objects.order_by('id'),
        empty_label=_('---------')
    )
    labels = django_filters.ModelChoiceFilter(
        label=_('Labels'),
        queryset=Label.objects.order_by('id'),
        empty_label=_('---------')
    )
    my_tasks = django_filters.BooleanFilter(
        label=_('My tasks'),
        method='filter_my_tasks',
        widget=forms.CheckboxInput,
        required=False
    )

    class Meta:
        model = Task
        fields = {
            'status__name': ['exact'],
            'assignee__username': ['exact'],
            'labels': ['exact'],
        }

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
