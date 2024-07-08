from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Status


class StatusCreationForm(forms.ModelForm):
    status_name = _("Status name")
    name = forms.CharField(label=status_name, max_length=40, required=True)
    status_description = _("Status description")
    description = forms.CharField(
        label=status_description,
        max_length=255,
        required=False
    )

    class Meta:
        model = Status
        fields = [
            'name',
            'description',
        ]
