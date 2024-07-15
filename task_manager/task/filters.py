import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.label.models import Label
from task_manager.status.models import Status
from task_manager.user.models import User
from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        label=_('Status'),
        queryset=Status.objects.order_by('id'),
        widget=forms.Select(attrs={'class': 'form-select mr-3 ml-2'})
    )
    executor = django_filters.ModelChoiceFilter(
        label=_('Executor'),
        queryset=User.objects.order_by('id'),
        widget=forms.Select(attrs={'class': 'form-select mr-3 ml-2'})
    )
    labels = django_filters.ModelChoiceFilter(
        label=_('Label'),
        queryset=Label.objects.order_by('id'),
        widget=forms.Select(attrs={'class': 'form-select mr-3 ml-2'})
    )
    self_tasks = django_filters.BooleanFilter(
        label=_('Only your tasks'),
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={'class': 'mr-3'}),
        required=False
    )

    class Meta:
        model = Task
        fields = {
            'status': ['exact'],
            'executor': ['exact'],
            'labels': ['exact'],
        }

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
