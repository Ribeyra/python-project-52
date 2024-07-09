from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'assignee',
            'tags',
        ]
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'status': _('Status'),
            'assignee': _('Assignee'),
            'tags': _('Tags'),
        }
        widgets = {
            'tags': forms.SelectMultiple,
        }
