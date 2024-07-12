from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'label',
        ]
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'label': _('Labels'),
        }
        widgets = {
            'label': forms.SelectMultiple,
        }
